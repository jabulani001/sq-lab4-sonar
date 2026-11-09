# Software Quality Lab 4: SonarQube Cloud

Code aus Lab 1 (TDD-Katas in Python), hier nur als Analyseobjekt für SonarQube Cloud.

| Ordner | Inhalt |
|---|---|
| `checkout_kata/` | Supermarket Checkout: Preise, Artikel, Rabatte |
| `fizzbuzz_kata/` | FizzBuzz, erstes TDD-Beispiel |
| `unittest.mock_examples/` | `readFromFile` mit gemocktem `open` |

## Tests

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/pytest -v
```
