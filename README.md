# BlockChain

# Blockchain-Based Encrypted File Storage System

This project is a decentralized file storage system that uses blockchain principles to provide secure, tamper-proof file management. It supports file uploads with AES encryption, RSA key protection, and records each transaction on a custom-built blockchain. The goal was to create a lightweight, serverless solution that ensures confidentiality, integrity, and controlled access to files.

## Features

- Upload and download files through a user-friendly web interface
- Files are encrypted using AES; the AES key is encrypted with RSA
- Each file upload is recorded as a transaction in a custom Python blockchain
- Mining logic validates and adds blocks to the chain
- “Request to Mine” flow to trigger mining after upload
- Visual feedback for upload status and transaction confirmation
- Local file verification using hash comparison
- No centralized storage or IPFS; blockchain is implemented from scratch

## Tech Stack

- Python
- Flask (for backend APIs and routing)
- HTML, CSS, Bootstrap (for frontend)
- JavaScript (for basic interactions)
- AES and RSA encryption (using `pycryptodome`)
- Custom blockchain logic (written in Python)

## How It Works

1. The user selects a file and uploads it via the frontend.
2. The file is encrypted using AES; the AES key is encrypted with RSA.
3. Metadata and the file hash are sent to the backend.
4. A new transaction is created and added to the pending pool.
5. When the user triggers "Request to Mine", the pending transaction is mined and added to the blockchain.
6. The file, its encrypted key, and the block hash are stored locally.
7. The user can later download and decrypt the file after verifying block integrity.

## Project Structure

- `frontend/` – static HTML/CSS/JS files and UI logic
- `blockchain.py` – core blockchain implementation
- `encryption.py` – encryption and decryption functions (AES + RSA)
- `server.py` – Flask server handling file routes, mining, and logic
- `storage/` – local encrypted files and blockchain data

# Notes

This system does not use IPFS or cloud storage — all blocks and files are handled locally

Key pairs are generated at runtime and stored temporarily

The blockchain is built with simplified consensus and proof-of-work logic for demo purposes
