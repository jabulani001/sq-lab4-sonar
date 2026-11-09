import os

def readFromFile(filename):
    if not os.path.exists(filename):
        raise Exception("Bad File")
    infile = open(filename, "r")
    try:
        line = infile.readline()
    except IOError as e:
        raise Exception("Error reading file") from e
    finally:
        infile.close()  #hier war der Fehler dass die Datei nie geschlossen wurde, close() hat gefehlt
    return line





