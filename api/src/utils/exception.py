class APIException(Exception):
    """
    Custom exception class for API-related errors.
    
    Args:
        message (str): Error message describing the issue
        code (int): HTTP status code or error code
    """
    def __init__(self, message: str, code: int):
        self.message = message
        self.code = code
        super().__init__(self.message)
    
    def __str__(self):
        return f"APIException({self.code}): {self.message}" 