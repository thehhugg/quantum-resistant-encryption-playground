import os
import subprocess
import sys

REPO_URL = "https://github.com/pq-crystals/kyber.git"
TARGET_DIR = os.path.join(os.path.dirname(__file__), "..", "kyber")


def kyber_present() -> bool:
    """Check if the Kyber repository is already present."""
    return os.path.isfile(os.path.join(TARGET_DIR, "Makefile"))


def clone_kyber():
    """Clone the official Kyber repository into the kyber/ directory."""
    if kyber_present():
        print("Kyber repository already present in 'kyber/'.")
        return

    if not os.path.isdir(TARGET_DIR):
        os.makedirs(TARGET_DIR)

    try:
        subprocess.check_call(["git", "clone", REPO_URL, TARGET_DIR])
        print("Kyber cloned successfully.")
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print("Failed to clone Kyber repository:", exc)
        print("Please ensure Git is installed and that you have network connectivity.")
        sys.exit(1)


if __name__ == "__main__":
    clone_kyber()
