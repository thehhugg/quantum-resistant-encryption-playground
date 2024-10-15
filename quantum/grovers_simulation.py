# quantum/grovers_simulation.py

from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator  # Use Operator to calculate unitary matrix

def grovers_algorithm():
    """Runs a simple Grover's algorithm simulation and calculates the unitary matrix."""

    # Create quantum circuit with 2 qubits
    circuit = QuantumCircuit(2)
    
    # Apply Hadamard gates to initialize superposition
    circuit.h([0, 1])
    
    # Oracle (black-box) gate for marking solution
    circuit.cz(0, 1)
    
    # Apply Hadamard gates again
    circuit.h([0, 1])

    # Calculate unitary matrix using the Operator class
    unitary = Operator(circuit)
    
    # Print unitary matrix
    print("Unitary matrix:\n", unitary.data)

if __name__ == "__main__":
    grovers_algorithm()
