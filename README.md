# Pytest Hardware Demo - ATM Cash Dispenser

A small, runnable example of equipment-oriented testing with Python and pytest. It uses a simulated ATM cash dispenser, so you can explore normal operation and device failures without physical hardware.

## What this project demonstrates

The simulator contains one cassette with ten banknotes, each worth 100 units. Calling `dispense(300)` returns three banknotes and leaves seven in stock.

Pytest is a general-purpose Python testing framework. It can test equipment through device drivers and interfaces. This project demonstrates the test structure using a software model; it is not a Hardware-in-the-Loop (HIL) test bench.

## Quick start

Requires Python 3.10 or later.

```bash
git clone https://github.com/devmeto5/pytest-hardware-demo.git
cd pytest-hardware-demo
python -m venv .venv
```

Activate the virtual environment:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# Linux / macOS
source .venv/bin/activate
```

Install the dependency and run the tests:

```bash
python -m pip install -r requirements.txt
python -m pytest -v
```

Expected result: **19 passed**.

## A simple test

```python
from dispenser import CashDispenser

def test_dispenses_three_notes():
    device = CashDispenser(notes=10)
    assert device.dispense(300) == 3
    assert device.notes == 7
```

The first assertion checks how many banknotes were delivered. The second checks the remaining stock. Pytest reports a failure if the actual behavior differs from either expectation.

## Test scenarios

| Scenario | Expected behavior |
| --- | --- |
| Withdraw 100, 300, or 1000 | Deliver the correct number of notes and update stock |
| Zero, negative, non-multiple amount, or invalid type | Reject the request without changing stock |
| Insufficient banknotes | Raise `insufficient notes` and preserve stock |
| Device offline | Raise `device offline` and preserve stock |
| Cash jam | Raise `cash jam` and preserve stock |
| Jam cleared | Allow the next withdrawal |
| Empty cassette | Reject the next withdrawal |
| Invalid initial stock | Reject simulator construction |

There are 19 test cases, including parameterized inputs. A pytest fixture creates a fresh dispenser for each test, keeping the scenarios independent of execution order.

## Project structure

```text
dispenser.py             # Device simulator and error type
tests/test_dispenser.py  # Tests, fixture, and parameterized inputs
requirements.txt        # Pinned pytest dependency
pytest.ini              # Test discovery settings
```

To generate a JUnit XML report:

```bash
python -m pytest --junitxml=test-results.xml
```

## Connecting real equipment

A physical device needs an adapter for its manufacturer's documented interface, such as USB, serial, or TCP. A real test bench must control device states and independently verify sensor readings, responses, and timeouts instead of setting the simulator's `online` and `jammed` flags.

This simulator deliberately assumes that failures leave stock unchanged. A real dispenser may partially deliver or retain banknotes; those outcomes need additional scenarios. The example does not model customer accounts, financial transactions, a communication protocol, or medical devices. Passing these tests validates the educational model only, not physical equipment or regulatory compliance.
