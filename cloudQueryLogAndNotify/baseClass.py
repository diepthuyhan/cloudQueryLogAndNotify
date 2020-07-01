from .customExceptions import IgnoreMessage


class BaseFormatMessage:
    def validate(self, message):
        return True
    
    def ignore_message(self):
        raise IgnoreMessage("ignore_message")
    
    def format(self, message):
        if self.validate(message):
            return self.format_message(message)
        return None

class BaseSlackFormartMessage(BaseFormatMessage):
    pass
