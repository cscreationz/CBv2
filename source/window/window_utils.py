import pickle

def readbinary(file: str) -> str:
    """Returns binary data from a given file as a string"""
    with open(file, 'rb') as f:
        data: str = pickle.load(f)
    return data