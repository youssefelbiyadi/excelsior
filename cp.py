import logging
import functools

def no_logging(method):
    """Decorator to mark a method as excluded from logging."""
    method.__no_logging__ = True
    return method

class LoggingMixin:
    def __getattribute__(self, name):
        # Skip logging for private or protected methods
        if name.startswith('_'):
            return super().__getattribute__(name)
        
        # Get the attribute (method or property)
        attr = super().__getattribute__(name)
        
        # Check if the method is callable and if logging should be skipped
        if callable(attr) and not getattr(attr, '__no_logging__', False):
            @functools.wraps(attr)
            def logged_method(*args, **kwargs):
                logger = self.get_logger()  # Assuming the subclass provides a `get_logger` method
                logger.info(f"Calling method {name} with args: {args}, kwargs: {kwargs}")
                try:
                    result = attr(*args, **kwargs)
                    logger.info(f"Method {name} returned: {result}")
                    return result
                except Exception as e:
                    logger.error(f"Method {name} raised an exception: {e}", exc_info=True)
                    raise
            return logged_method
        else:
            return attr
