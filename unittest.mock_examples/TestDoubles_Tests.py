import pytest
from pytest import raises
from unittest.mock import MagicMock
from LineReader import readFromFile

@pytest.fixture()
def mock_open(monkeypatch):
    mock_file = MagicMock()
    mock_file.readline = MagicMock(return_value="test line")
    mock_open = MagicMock(return_value=mock_file)
    monkeypatch.setattr("builtins.open", mock_open)
    return mock_open

def test_returnsCorrectString(mock_open, monkeypatch):
    mock_exists = MagicMock(return_value=True)
    monkeypatch.setattr("os.path.exists", mock_exists)
    result = readFromFile("blah")
    mock_open.assert_called_once_with("blah", "r")
    assert result == "test line"

def test_throwsExceptionWithBadFile(mock_open, monkeypatch):
    mock_exists = MagicMock(return_value=False)
    monkeypatch.setattr("os.path.exists", mock_exists)
    with raises(Exception):
        result = readFromFile("blah")


# ---------- Part B: erweiterte Mock-Bedingungen (Alban) ----------

# Datei fehlt -> open() darf gar nicht erst aufgerufen werden
def test_openNotCalledWithBadFile(mock_open, monkeypatch):
    monkeypatch.setattr("os.path.exists", MagicMock(return_value=False))
    with raises(Exception):
        readFromFile("blah")
    mock_open.assert_not_called()

# Prueft, dass genau einmal mit dem richtigen Dateinamen nach der Datei geschaut wird
def test_existsCheckedOnceWithFilename(mock_open, monkeypatch):
    mock_exists = MagicMock(return_value=True)
    monkeypatch.setattr("os.path.exists", mock_exists)
    readFromFile("blah")
    mock_exists.assert_called_once_with("blah")

# Mock spielt einen Lesefehler vor -> Code muss einen eigenen Fehler melden
def test_throwsExceptionOnReadError(mock_open, monkeypatch):
    monkeypatch.setattr("os.path.exists", MagicMock(return_value=True))
    mock_open.return_value.readline.side_effect = IOError("disk error")
    with raises(Exception, match="Error reading file"):
        readFromFile("blah")

# Nach dem Lesen muss die Datei geschlossen werden (hat den close Fehler gefunden)
def test_fileIsClosedAfterReading(mock_open, monkeypatch):
    monkeypatch.setattr("os.path.exists", MagicMock(return_value=True))
    readFromFile("blah")
    mock_open.return_value.close.assert_called_once()

# Auch bei einem Lesefehler muss die Datei geschlossen werden
def test_fileIsClosedEvenOnReadError(mock_open, monkeypatch):
    monkeypatch.setattr("os.path.exists", MagicMock(return_value=True))
    mock_open.return_value.readline.side_effect = IOError("disk error")
    with raises(Exception):
        readFromFile("blah")
    mock_open.return_value.close.assert_called_once()
