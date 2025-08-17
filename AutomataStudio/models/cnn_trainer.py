# (imports and header are the same)
import numpy as np
import xarray as xr
import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.metrics import classification_report
import itertools
from matplotlib.gridspec import GridSpec



def visualize_learned_rule_heatmap(model, processed_ds_path, output_filename="rule_heatmap.png"):
    """
    Generates a heatmap showing the model's exact learned rule by testing all 512 possible neighborhoods.
    """
    print("\n✨ Visualizing exact learned rule as a heatmap...")

    # 1. Get normalization stats from the processed dataset file
    processed_ds = xr.open_dataset(processed_ds_path)
    train_mean = processed_ds.attrs['train_mean']
    train_std = processed_ds.attrs['train_std']

    # 2. Generate all 512 possible 3x3 binary neighborhoods
    all_patterns_flat = itertools.product([0, 1], repeat=9)
    all_neighborhoods = np.array(list(all_patterns_flat), dtype=np.float32).reshape(-1, 3, 3)

    # 3. Prepare patterns for the model and get predictions
    X_patterns = all_neighborhoods.reshape(-1, 3, 3, 1)
    X_patterns_norm = (X_patterns - train_mean) / train_std
    predictions = (model.predict(X_patterns_norm, batch_size=512, verbose=0) > 0.5).astype(int)

    # 4. Aggregate the results based on center cell state (xc) and neighbor count (n)
    #   Rows: xc=0, xc=1 | Cols: n=0, n=1, ..., n=8
    rule_matrix = np.zeros((2, 9))
    count_matrix = np.zeros((2, 9), dtype=int)

    for i, hood in enumerate(all_neighborhoods):
        center_cell_xc = int(hood[1, 1])
        neighbor_count_n = int(np.sum(hood) - center_cell_xc)
        
        rule_matrix[center_cell_xc, neighbor_count_n] += predictions[i][0]
        count_matrix[center_cell_xc, neighbor_count_n] += 1
    
    # Calculate the proportion of "Alive" predictions for each case
    proportion_matrix = np.divide(rule_matrix, count_matrix, out=np.zeros_like(rule_matrix, dtype=float), where=count_matrix != 0)

    # 5. Plot the heatmap
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.heatmap(proportion_matrix, annot=True, fmt=".2f", cmap="viridis", ax=ax, linewidths=.5, vmin=0, vmax=1)

    # Overlay green circles on the TRUE Game of Life rules for easy comparison
    # Rule: Birth (if xc=0, n=3 -> 1)
    ax.add_patch(plt.Circle((3.5, 0.5), 0.45, color='lime', fill=False, lw=3, label='Correct GoL Rule'))
    # Rule: Survival (if xc=1, n=2 or n=3 -> 1)
    ax.add_patch(plt.Circle((2.5, 1.5), 0.45, color='lime', fill=False, lw=3))
    ax.add_patch(plt.Circle((3.5, 1.5), 0.45, color='lime', fill=False, lw=3))

    ax.set_xlabel("Neighbor Count (n)", fontsize=12)
    ax.set_ylabel("Center Cell State (xc)", fontsize=12)
    ax.set_yticklabels(['Dead (0)', 'Alive (1)'], rotation=0)
    ax.set_title('Heatmap of Learned Rule (Proportion of "Alive" Predictions)', fontsize=14)
    plt.tight_layout()
    plt.savefig(output_filename)
    plt.show()

def build_cnn_model(kernel_size=(3, 3), num_filters=1):
    """
    Builds and compiles the CNN model with a flexible architecture.

    Args:
        kernel_size (tuple): The (height, width) of the convolutional kernel.
        num_filters (int): The number of kernels (filters) in the Conv2D layer.

    Returns:
        A compiled Keras model.
    """
    model = keras.Sequential([
        keras.Input(shape=(3, 3, 1)),
        layers.Conv2D(filters=num_filters, kernel_size=kernel_size, activation='relu', name="convolution_layer"),
        layers.Flatten(),
        layers.Dense(1, activation='sigmoid')
    ])
    
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    model.summary()
    return model
def visualize_learned_rule(model, output_filename="rule_visualization.png"):
    """
    Visualizes the difference between the true GoL rule and the model's learned linear rule.
    """
    print("\n✨ Visualizing learned rule vs. ground truth...")
    conv_layer = model.get_layer('convolution_layer')
    weights, biases = conv_layer.get_weights()
    kernel = weights[:, :, 0, 0]
    # The bias was correctly extracted into this variable
    bias = biases[0]

    wc = kernel[1, 1]
    wn = (np.sum(kernel) - wc) / 8.0

    true_rule = {
        'n': [3, 2, 3], # Neighbor counts
        'xc': [0, 1, 1]  # Center cell states (0=Dead, 1=Alive)
    }

    fig, ax = plt.subplots(figsize=(10, 6))

    # THE FIX: Changed the variable name from 'b' to 'bias' in the line below
    ax.axvspan(*sorted(((-bias / wn), (-bias - wc) / wn)), alpha=0.2, color='orange', label='Model Predicts "Alive"')

    ax.plot(true_rule['n'], true_rule['xc'], 'o', color='green', markersize=15, alpha=0.7, label='True "Alive" Rule')

    ax.set_yticks([0, 1])
    ax.set_yticklabels(['Dead', 'Alive'])
    ax.set_xlabel('Neighbor Count (n)')
    ax.set_ylabel('Center Cell State (xc)')
    ax.set_title('Game of Life Rule vs. Learned Linear Approximation')
    ax.set_xlim(-0.5, 8.5)
    ax.set_ylim(-0.5, 1.5)
    ax.grid(True, axis='x', linestyle='--')
    ax.legend()
    
    plt.savefig(output_filename)
    plt.show()
    print(f"✅ Rule visualization saved to {output_filename}")



def create_simulation_animation(model, original_nc_path, processed_ds_path, output_filename="simulation_comparison.gif", steps=100):
    """Generates a side-by-side animation with a live error plot."""
    print(f"\n🎬 Creating predictive animation up to {steps} steps...")
    
    # --- Data Loading and Prediction (Unchanged) ---
    original_ds = xr.open_dataset(original_nc_path)
    variable_name = list(original_ds.data_vars)[0]
    ground_truth_sequence = original_ds[variable_name].isel(time=slice(0, steps)).values
    processed_ds = xr.open_dataset(processed_ds_path)
    train_mean, train_std = processed_ds.attrs['train_mean'], processed_ds.attrs['train_std']
    
    predicted_sequence = []
    current_grid = ground_truth_sequence[0].copy()
    for _ in range(steps):
        predicted_sequence.append(current_grid)
        padded_grid = np.pad(current_grid, pad_width=1, mode='wrap')
        neighborhoods = [padded_grid[y:y+3, x:x+3] for y in range(current_grid.shape[0]) for x in range(current_grid.shape[1])]
        X_live = np.array(neighborhoods, dtype=np.float32).reshape(-1, 3, 3, 1)
        X_live_norm = (X_live - train_mean) / train_std
        predictions = model.predict(X_live_norm, verbose=0)
        current_grid = (predictions > 0.5).astype(np.uint8).reshape(current_grid.shape)
    predicted_sequence = np.array(predicted_sequence)

    # --- FIX: Setup a proper 2x2 plot layout ---
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 12))
    fig.suptitle('Simulation Comparison', fontsize=20)

    # Panel 1: Ground Truth
    im1 = ax1.imshow(ground_truth_sequence[0], cmap='binary')
    ax1.set_title("Ground Truth")
    
    # Panel 2: CNN Prediction
    im2 = ax2.imshow(predicted_sequence[0], cmap='binary')
    ax2.set_title("CNN Prediction")

    # Panel 3: Difference Grid
    initial_diff = ground_truth_sequence[0] - predicted_sequence[0]
    im3 = ax3.imshow(initial_diff, cmap='coolwarm', vmin=-1, vmax=1)
    ax3.set_title("Difference (Errors)")

    # Panel 4: Error Timeline
    error_history = []
    line, = ax4.plot([], [], 'r-')
    ax4.set_xlim(0, steps)
    ax4.set_ylim(0, 1) # Will adjust dynamically
    ax4.set_title("Incorrect Cells Over Time")
    ax4.set_xlabel("Time Step")
    ax4.set_ylabel("Error Count")
    ax4.grid(True)

    for ax in [ax1, ax2, ax3]: ax.set_axis_off()

    def update(frame):
        # Update all three image panels
        im1.set_array(ground_truth_sequence[frame])
        im2.set_array(predicted_sequence[frame])
        difference = ground_truth_sequence[frame] - predicted_sequence[frame]
        im3.set_array(difference)
        
        # Update the error timeline plot
        error_count = np.sum(difference != 0)
        error_history.append(error_count)
        line.set_data(range(len(error_history)), error_history)
        if error_history: # Avoid error on empty list
            ax4.set_ylim(0, max(1, max(error_history) * 1.1))

        fig.suptitle(f'Simulation Comparison - Time Step: {frame}', fontsize=20)
        return im1, im2, im3, line

    ani = animation.FuncAnimation(fig, update, frames=steps, blit=False, interval=100)
    plt.tight_layout(rect=[0, 0, 1, 0.96]) # Adjust for suptitle
    ani.save(output_filename, writer='pillow', fps=10)
    plt.close()
    print(f"✅ Animation saved to {output_filename}")

def train_gol_model(dataset_path: str, model_save_path: str = "gol_cnn.keras", kernel_size=(3,3), num_filters=1):
    """
    Loads a dataset, trains a CNN model, and saves it.
    """
    print("💾 Loading dataset...")
    processed_ds = xr.open_dataset(dataset_path)
    X_train, y_train = processed_ds['X_train'].values, processed_ds['y_train'].values
    X_val, y_val = processed_ds['X_val'].values, processed_ds['y_val'].values
    
    # MODIFICATION: Call the new model builder function
    model = build_cnn_model(kernel_size=kernel_size, num_filters=num_filters)
    
    print("\n🔥 Training model...")
    history = model.fit(X_train, y_train, epochs=5, validation_data=(X_val, y_val), batch_size=256)
    
    print(f"\n💾 Saving trained model to {model_save_path}...")
    model.save(model_save_path)
    print("✅ Model saved successfully.")

    # REPLACED: Call the new, more accurate heatmap visualization
    visualize_learned_rule_heatmap(model, processed_ds_path=dataset_path)

    # CHANGE THIS LINE:
    return model_save_path # Return the path, not the model object


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Train a CNN and generate a predictive animation.")
    parser.add_argument("processed_dataset_path", type=str, help="Path to the preprocessed .nc dataset file.")
    parser.add_argument("original_sim_path", type=str, help="Path to the original simulation .nc file for visualization.")
    args = parser.parse_args()

    # Step 1: Train the model and get the path where it was saved.
    saved_model_path = train_gol_model(dataset_path=args.processed_dataset_path)

    # Step 2: Explicitly load the model from the saved file.
    # This ensures we are working with a model OBJECT, not a string.
    print(f"\n✅ Loading trained model from {saved_model_path} for animation...")
    loaded_model = keras.models.load_model(saved_model_path)

    # Step 3: Generate the comparison animation using the loaded model.
    create_simulation_animation(
        loaded_model, # Pass the correct model object here
        original_nc_path=args.original_sim_path,
        processed_ds_path=args.processed_dataset_path
    )