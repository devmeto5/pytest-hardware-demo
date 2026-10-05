"""Small deterministic simulator of a single-cassette ATM dispenser."""


class DispenserError(RuntimeError):
    """The dispenser cannot complete the requested operation."""


class CashDispenser:
    """Model whole banknotes only; no bank accounts or real hardware I/O."""

    denomination = 100

    def __init__(self, notes: int = 10):
        if type(notes) is not int or notes < 0:
            raise ValueError("notes must be a non-negative integer")
        self.notes = notes
        self.online = True
        self.jammed = False

    def dispense(self, amount: int) -> int:
        """Return the number of delivered notes, or fail without changing stock."""
        if type(amount) is not int or amount <= 0 or amount % self.denomination:
            raise ValueError("amount must be a positive integer multiple of 100")
        if not self.online:
            raise DispenserError("device offline")
        if self.jammed:
            raise DispenserError("cash jam")
        requested_notes = amount // self.denomination
        if requested_notes > self.notes:
            raise DispenserError("insufficient notes")
        self.notes -= requested_notes
        return requested_notes
