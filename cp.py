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

import unittest
from unittest.mock import MagicMock, patch
import logging

import pytest
import logging
from unittest.mock import MagicMock, patch
from your_module import LoggingMixin, ExampleOperations, no_logging

@pytest.fixture
def mock_logger():
    with patch.object(ExampleOperations, 'get_logger') as mock_get_logger:
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        yield mock_logger

@pytest.fixture
def example_operations():
    return ExampleOperations("SampleObject")

def test_create_method_logged(mock_logger, example_operations):
    # Call the create method
    result = example_operations.create()

    # Assert the method returned the correct value
    assert result == "Creating SampleObject"

    # Assert that logging was called correctly
    mock_logger.info.assert_any_call("Calling method create with args: (), kwargs: {}")
    mock_logger.info.assert_any_call("Method create returned: Creating SampleObject")

def test_delete_method_not_logged(mock_logger, example_operations):
    # Call the delete method
    result = example_operations.delete()

    # Assert the method returned the correct value
    assert result == "Deleting SampleObject"

    # Assert that logging was not called
    mock_logger.info.assert_not_called()

def test_private_method_not_logged(mock_logger, example_operations):
    # Call the private method
    result = example_operations._private_method()

    # Assert the method returned the correct value
    assert result == "This is a private method"

    # Assert that logging was not called
    mock_logger.info.assert_not_called()

def test_update_method_logged(mock_logger, example_operations):
    # Call the update method
    result = example_operations.update()

    # Assert the method returned the correct value
    assert result == "Updating SampleObject"

    # Assert that logging was called correctly
    mock_logger.info.assert_any_call("Calling method update with args: (), kwargs: {}")
    mock_logger.info.assert_any_call("Method update returned: Updating SampleObject")
