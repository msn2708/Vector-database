from initlog import Loggers

"""Custom exception class for text processing errors."""

class TextProcessingError(Exception):
    
    def __init__(self, message, severity):
        super().__init__(message)
        self.severity = severity
        self.message = message
        # Get the logger for this namespace
        self.logger = Loggers().get_logger()
                
        # Log the error message using the logger in the TextProcessing namespace
        self.logger.log(severity, message, exc_info=True)
        
            