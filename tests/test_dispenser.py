import pytest

from dispenser import CashDispenser, DispenserError


@pytest.fixture
def dispenser():
    """Each test gets a fresh cassette with ten banknotes."""
    return CashDispenser(notes=10)


@pytest.mark.parametrize("amount, delivered, remaining", [(100, 1, 9), (300, 3, 7), (1000, 10, 0)])
def test_dispenses_requested_amount(dispenser, amount, delivered, remaining):
    assert dispenser.dispense(amount) == delivered
    assert dispenser.notes == remaining


@pytest.mark.parametrize("amount", [0, -100, 150, 100.0, "100", True, None])
def test_rejects_invalid_amount_without_losing_notes(dispenser, amount):
    with pytest.raises(ValueError, match="positive integer multiple of 100"):
        dispenser.dispense(amount)
    assert dispenser.notes == 10


def test_insufficient_cash_preserves_stock(dispenser):
    with pytest.raises(DispenserError, match="insufficient notes"):
        dispenser.dispense(1100)
    assert dispenser.notes == 10


def test_offline_device_preserves_stock(dispenser):
    dispenser.online = False
    with pytest.raises(DispenserError, match="device offline"):
        dispenser.dispense(100)
    assert dispenser.notes == 10


def test_jam_preserves_stock_and_device_recovers(dispenser):
    dispenser.jammed = True
    with pytest.raises(DispenserError, match="cash jam"):
        dispenser.dispense(300)
    assert dispenser.notes == 10
    dispenser.jammed = False
    assert dispenser.dispense(300) == 3
    assert dispenser.notes == 7


def test_empty_cassette_rejects_next_withdrawal(dispenser):
    assert dispenser.dispense(1000) == 10
    with pytest.raises(DispenserError, match="insufficient notes"):
        dispenser.dispense(100)
    assert dispenser.notes == 0


@pytest.mark.parametrize("notes", [-1, 1.5, True, "10", None])
def test_rejects_invalid_initial_stock(notes):
    with pytest.raises(ValueError, match="non-negative integer"):
        CashDispenser(notes=notes)
