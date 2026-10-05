# Fintech Mobile Banking Backend Engine

A lightweight, secure Python implementation of a core mobile banking service API. It demonstrates atomic fund transfers, PIN hashing, account auditing, and transaction logging.

## Core Features

- **PIN Security:** User PINs are never stored in plain text; all authentication uses SHA-256 hashing.
- **Atomic Fund Transfers:** Ensures money is only deducted from the sender if the transfer to the recipient successfully completes.
- **Audit Logging:** Automatically logs all transactions with timestamps and balance tracking.
- **Role & Access Controls:** Account balances can only be accessed with valid authentication credentials.

## How to Run

1. Clone this repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/fintech-banking-backend.git](https://github.com/YOUR_USERNAME/fintech-banking-backend.git)
