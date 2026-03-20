"""
Download the Kyber C Reference Implementation (Advanced / Optional)
===================================================================

This script clones the official pq-crystals/kyber C repository into the
``kyber/`` directory. This is the **reference C implementation** of Kyber
and requires a C compiler plus OpenSSL headers to build.

For most users of this playground, you do NOT need this script. The
playground's examples use `kyber-py`, a pure-Python educational
implementation that is installed automatically via ``pip install -r
requirements.txt``.

Use this script only if you want to:
- Read or study the official C reference code
- Run the C benchmarks or test vectors
- Compare the C and Python implementations

Prerequisites
-------------
- Git must be installed and available on PATH
- Network connectivity to github.com
- (To build) A C compiler and OpenSSL development headers

Usage
-----
    python scripts/download_kyber.py
"""

import os
import subprocess
import sys

REPO_URL = "https://github.com/pq-crystals/kyber.git"
TARGET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kyber")


def kyber_present() -> bool:
    """Check if the Kyber repository is already present."""
    return os.path.isfile(os.path.join(TARGET_DIR, "Makefile"))


def clone_kyber() -> None:
    """Clone the official Kyber repository into the kyber/ directory."""
    if kyber_present():
        print("Kyber C reference repository already present in 'kyber/'.")
        return

    print("NOTE: This downloads the C reference implementation of Kyber.")
    print("For the Python examples in this playground, you only need kyber-py,")
    print("which is already listed in requirements.txt.\n")

    if not os.path.isdir(TARGET_DIR):
        os.makedirs(TARGET_DIR)

    try:
        subprocess.check_call(["git", "clone", REPO_URL, TARGET_DIR])
        print("\nKyber C reference cloned successfully.")
        print("To build it, cd into kyber/ref/ and run 'make'.")
        print("See kyber/README.md for build prerequisites.")
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print("Failed to clone Kyber repository:", exc)
        print("Please ensure Git is installed and that you have network connectivity.")
        sys.exit(1)


if __name__ == "__main__":
    clone_kyber()
