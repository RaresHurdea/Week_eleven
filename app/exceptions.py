class PenguinDataException(Exception):
    """Base exception for penguin data operations"""
    pass

class FileNotLoadedException(PenguinDataException):
    pass

class InvalidColumnException(PenguinDataException):
    pass

class InvalidSortOrderException(PenguinDataException):
    pass

class NonNumericAttributeException(PenguinDataException):
    pass

class InvalidFilterException(PenguinDataException):
    pass