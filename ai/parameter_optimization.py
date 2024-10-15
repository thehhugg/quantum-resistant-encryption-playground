# ai/parameter_optimization.py

import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Sample data: lattice sizes and corresponding encryption times (in seconds)
# Replace this with actual data from the speed tests later.
lattice_sizes = np.array([[256], [512], [768], [1024]])  
encryption_times = np.array([0.1, 0.25, 0.5, 0.75])     

# Train a linear regression model to predict encryption time based on lattice size
model = LinearRegression().fit(lattice_sizes, encryption_times)

def predict_encryption_time(lattice_size):
    """ Predicts the encryption time for a given lattice size. """
    return model.predict([[lattice_size]])[0]

def visualize_data():
    """ Plot lattice size vs. encryption time and model prediction. """
    plt.scatter(lattice_sizes, encryption_times, color='blue', label='Actual')
    plt.plot(lattice_sizes, model.predict(lattice_sizes), color='red', label='Model')
    plt.xlabel('Lattice Size')
    plt.ylabel('Encryption Time (seconds)')
    plt.title('Lattice Size vs. Encryption Time')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # Example usage: Predict encryption time for a lattice size of 640
    lattice_size_to_predict = 640
    predicted_time = predict_encryption_time(lattice_size_to_predict)
    print(f"Predicted encryption time for lattice size {lattice_size_to_predict}: {predicted_time:.4f} seconds")

    # Visualize data and regression model
    visualize_data()
