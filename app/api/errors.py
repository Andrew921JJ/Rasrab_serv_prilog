# app/domain/errors.py (ваши доменные ошибки)
class DomainError(Exception): pass
class ErrNotFound(DomainError): pass
class ErrAlreadyExists(DomainError): pass
class ErrConflict(DomainError): pass
class ErrInvalidInput(DomainError): pass