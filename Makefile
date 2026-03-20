.PHONY: help install install-dev test lint demo-kem demo-dsa demo-grovers demo-shors demo-compare demo-all clean

PYTHON ?= python3

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies from requirements.txt
	$(PYTHON) -m pip install -r requirements.txt

install-dev: ## Install with dev dependencies (pytest, ruff)
	$(PYTHON) -m pip install -e ".[dev]"

test: ## Run the test suite
	$(PYTHON) -m pytest tests/ -v

lint: ## Lint code with ruff
	ruff check . --select E,F,I --ignore E501

demo-kem: ## Run the ML-KEM (Kyber) key encapsulation demo
	$(PYTHON) examples/01_ml_kem_keygen.py

demo-dsa: ## Run the ML-DSA (Dilithium) digital signature demo
	$(PYTHON) examples/02_ml_dsa_signatures.py

demo-compare: ## Run the classical-vs-PQC comparison
	$(PYTHON) examples/03_classical_vs_pqc.py

demo-grovers: ## Run Grover's search algorithm simulation
	$(PYTHON) quantum/grovers_simulation.py

demo-shors: ## Run Shor's factoring algorithm simulation
	$(PYTHON) quantum/shors_simulation.py

demo-all: demo-kem demo-dsa demo-compare demo-grovers demo-shors ## Run all demos

clean: ## Remove generated files and caches
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf .pytest_cache tests/.pytest_cache
	rm -rf *.egg-info build dist
	rm -f grovers_result.png parameter_optimization.png lattice_optimizer.png
