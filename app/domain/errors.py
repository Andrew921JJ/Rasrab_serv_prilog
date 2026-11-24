class DomainError(Exception):
    """Базовый класс"""
    pass

class ErrNotFound(DomainError):
    pass

class ErrAlreadyExists(DomainError):
    pass

class ErrConflict(DomainError):
    pass

class ErrInvalidInput(DomainError):
    pass