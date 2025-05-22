## Kyber Installation (Local Only)

To use the Kyber encryption scheme locally, you'll need to download it manually, as it's not included in this repo.

### Install Kyber Locally
Clone the official Kyber repository into the `kyber/` folder or run the helper script:

```bash
git clone https://github.com/pq-crystals/kyber.git kyber
# or
python scripts/download_kyber.py
```

This will place the Kyber reference implementation in the correct directory for local use, but it will not be tracked by Git.
