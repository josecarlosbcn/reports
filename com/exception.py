from constants import URL


class Error(Exception):
    """Base class for exceptions in this module."""
    def __init__(self, object, function, exception, message):
        self.object = object
        self.function = function
        self.exception = exception
        # f = FileWriter(URL.LOG)
        # f.writeFile(
        #     object + "::" + function + "::Exception" + "\n"
        #     + "Exception: " + str(exception) + "\n"
        #     + "Message: " + message
        # )

class TagException(Error):
    def __init__(self, object, function, ex, message):
        super().__init__(object, function, ex, message)
        self.message = message

class DocException(Error):
    def __init__(self, object, function, ex, message):
        super().__init__(object, function, ex, message)
        self.message = message

class DDBBException(Error):
    def __init__(self, object, function, ex, message):
        super().__init__(object, function, ex, message)
        self.message = message

class NamePlayerException(Error):
    def __init__(self, object, function, ex, message):
        super().__init__(object, function, ex, message)
        self.message = message

class URLException(Error):
    def __init__(self, object, function, ex, message):
        super().__init__(object, function, ex, message)
        self.message = message

class TeamException(Error):
    def __init__(self, object, function, ex, message):
        super().__init__(object, function, ex, message)
        self.message = message

class PlayerException(Error):
    def __init__(self, object, function, ex, message):
        super().__init__(object, function, ex, message)
        self.message = message

class KeyActionException(Error):
    def __init__(self, object, function, ex, message):
        super().__init__(object, function, ex, message)
        self.message = message
