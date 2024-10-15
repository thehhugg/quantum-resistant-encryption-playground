# quantum/grovers_simulation.py

import numpy as np
from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.visualization import plot_histogram
from qiskit.providers.aer import AerSimulator

def grovers_algorithm():
    """Runs a simple Grover's algorithm simulation."""

    # Create quantum circuit with 2 qubits
    circuit = QuantumCircuit(2)
    
    # Apply Hadamard gates to initialize superposition
    circuit.h([0, 1])
    
    # Oracle (black-box) gate for marking solution
    circuit.cz(0, 1)
    
    # Apply Hadamard gates again
    circuit.h([0, 1])

    # Measure qubits
    circuit.measure_all()

    # Use simulator to run circuit
    simulator = AerSimulator()
    compiled_circuit = transpile(circuit, simulator)
    qobj = assemble(compiled_circuit)
    result = simulator.run(qobj).result()
    
    # Get counts and display results
    counts = result.get_counts(circuit)
    plot_histogram(counts)
    
    return counts

if __name__ == "__main__":
    result = grovers_algorithm()
    print(f"Grover's Algorithm Result: {result}")
