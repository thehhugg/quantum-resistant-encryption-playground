# ai/lattice_optimizer.py

import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pandas as pd

# Load data from CSV file, assuming real performance data is stored there
# CSV should contain lattice_size, encryption_time, keygen_time, decryption_time
data = pd.read_csv('../data/encryption_times.csv')

# Extract features and target
features = data[['lattice_size', 'keygen_time', 'decryption_time']].values
encryption_times = data['encryption_time'].values

# Train more advanced Linear Regression model
model = LinearRegression().fit(features, encryption_times)

def predict_encryption_time(lattice_size, keygen_time, decryption_time):
    """ Predicts the encryption time for given input parameters. """
    return model.predict([[lattice_size, keygen_time, decryption_time]])[0]

def visualize_model():
    """ Visualizes the actual data and model prediction. """
    plt.scatter(data['lattice_size'], encryption_times, color='blue', label='Actual')
    plt.plot(data['lattice_size'], model.predict(features), color='red', label='Model Prediction')
    plt.xlabel('Lattice Size')
    plt.ylabel('Encryption Time (seconds)')
    plt.legend()
    plt.title('Lattice Size vs Encryption Time')
    plt.show()

if __name__ == "__main__":
    lattice_size = 768
    keygen_time = 0.03
    decryption_time = 0.20

    predicted_time = predict_encryption_time(lattice_size, keygen_time, decryption_time)
    print(f"Predicted encryption time for lattice size {lattice_size}: {predicted_time:.4f} seconds")

    # Visualize model performance
    visualize_model()
