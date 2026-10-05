import datetime
import hashlib


class BankAccount:
    """Represents a customer's bank account with secure balance operations."""
    
    def __init__(self, account_number: str, account_holder: str, initial_balance: float, pin: str):
        self.account_number = account_number
        self.account_holder = account_holder
        self._balance = initial_balance
        self._pin_hash = self._hash_pin(pin)
        self.transaction_history = []
        self._log_transaction("ACCOUNT_CREATED", initial_balance, "Initial account balance")

    def _hash_pin(self, pin: str) -> str:
        """Hashes the user's PIN for secure verification."""
        return hashlib.sha256(pin.encode()).hexdigest()

    def verify_pin(self, pin: str) -> bool:
        """Validates the provided PIN against the stored hash."""
        return self._pin_hash == self._hash_pin(pin)

    def _log_transaction(self, tx_type: str, amount: float, description: str):
        """Records a timestamped transaction in the account audit log."""
        record = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": tx_type,
            "amount": amount,
            "balance_after": self._balance,
            "description": description
        }
        self.transaction_history.append(record)

    def deposit(self, amount: float) -> bool:
        """Deposits funds into the account."""
        if amount <= 0:
            print("[ERROR] Deposit amount must be greater than zero.")
            return False
        
        self._balance += amount
        self._log_transaction("DEPOSIT", amount, "Funds deposited successfully")
        print(f"[SUCCESS] Deposited ₦{amount:,.2f}. New Balance: ₦{self._balance:,.2f}")
        return True

    def withdraw(self, amount: float, pin: str) -> bool:
        """Withdraws funds if the PIN is correct and funds are available."""
        if not self.verify_pin(pin):
            print("[SECURITY ERROR] Invalid PIN supplied.")
            return False
        
        if amount > self._balance:
            print("[ERROR] Insufficient funds for transaction.")
            return False

        self._balance -= amount
        self._log_transaction("WITHDRAWAL", amount, "Cash withdrawal")
        print(f"[SUCCESS] Withdrew ₦{amount:,.2f}. Remaining Balance: ₦{self._balance:,.2f}")
        return True

    def get_balance(self, pin: str):
        """Returns the current account balance after authentication."""
        if not self.verify_pin(pin):
            print("[SECURITY ERROR] Invalid PIN supplied.")
            return None
        return self._balance


class BankingService:
    """Manages multi-account transactions and inter-bank transfers."""
    
    def __init__(self):
        self.accounts = {}

    def create_account(self, account_number: str, holder_name: str, initial_deposit: float, pin: str):
        """Registers a new bank account."""
        if account_number in self.accounts:
            print(f"[ERROR] Account number {account_number} already exists.")
            return
        
        account = BankAccount(account_number, holder_name, initial_deposit, pin)
        self.accounts[account_number] = account
        print(f"[SUCCESS] Account {account_number} created for {holder_name}.")

    def transfer_funds(self, sender_acc_num: str, receiver_acc_num: str, amount: float, pin: str) -> bool:
        """Executes a secure transfer between two bank accounts."""
        if sender_acc_num not in self.accounts:
            print("[ERROR] Sender account not found.")
            return False
        
        if receiver_acc_num not in self.accounts:
            print("[ERROR] Recipient account not found.")
            return False

        sender = self.accounts[sender_acc_num]
        receiver = self.accounts[receiver_acc_num]

        # Authenticate sender and check funds
        if not sender.verify_pin(pin):
            print("[SECURITY ERROR] Transfer failed: Incorrect PIN.")
            return False

        if sender._balance < amount:
            print("[ERROR] Transfer failed: Insufficient funds.")
            return False

        # Execute atomic transfer
        sender._balance -= amount
        sender._log_transaction("TRANSFER_OUT", amount, f"Transfer to Acc: {receiver_acc_num}")
        
        receiver._balance += amount
        receiver._log_transaction("TRANSFER_IN", amount, f"Transfer from Acc: {sender_acc_num}")

        print(f"[SUCCESS] Transferred ₦{amount:,.2f} from {sender.account_holder} to {receiver.account_holder}.")
        return True


# --- Demonstration Run ---
if __name__ == "__main__":
    print("==================================================")
    print(" FINTECH BANKING BACKEND ENGINE (DEMO RUN)")
    print("==================================================\n")

    bank = BankingService()

    # 1. Create Accounts
    bank.create_account("0123456789", "Chisomeme Ezekakpu", 150000.00, "4321")
    bank.create_account("0987654321", "Babatunde Adeleke", 25000.00, "1234")

    # 2. Perform Fund Transfer
    print("\n--- Initiating Transfer ---")
    bank.transfer_funds(
        sender_acc_num="0123456789",
        receiver_acc_num="0987654321",
        amount=35000.00,
        pin="4321"
    )

    # 3. Verify Balances
    sender_account = bank.accounts["0123456789"]
    recipient_account = bank.accounts["0987654321"]

    print(f"\nSender New Balance: ₦{sender_account.get_balance('4321'):,.2f}")
    print(f"Recipient New Balance: ₦{recipient_account.get_balance('1234'):,.2f}")
