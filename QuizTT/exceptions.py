class BaseAppException(Exception):
    pass

class LogicError(BaseAppException):
    pass

class InvalidQuizData(BaseAppException):
    pass