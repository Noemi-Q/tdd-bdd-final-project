"""
Module for testing error handlers in the Product Demo Service.
"""

import unittest
from service import app
from service.common import error_handlers
from service.common import status
from service.models import DataValidationError


class TestErrorHandlers(unittest.TestCase):
    """Unit tests for Flask error handlers."""

    def setUp(self):
        """Setup the test client and app context."""
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Pop the app context after tests."""
        self.app_context.pop()

    def test_bad_request_handler(self):
        """Test HTTP 400 handler."""
        response, code = error_handlers.bad_request("Bad Request Test")
        self.assertEqual(code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Bad Request Test", response.json["message"])

    def test_not_found_handler(self):
        """Test HTTP 404 handler."""
        response, code = error_handlers.not_found("Not Found Test")
        self.assertEqual(code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Not Found Test", response.json["message"])

    def test_method_not_supported_handler(self):
        """Test HTTP 405 handler."""
        response, code = error_handlers.method_not_supported("Method Not Allowed Test")
        self.assertEqual(code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertIn("Method Not Allowed Test", response.json["message"])

    def test_media_type_not_supported_handler(self):
        """Test HTTP 415 handler."""
        response, code = error_handlers.mediatype_not_supported("Unsupported Media Test")
        self.assertEqual(code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        self.assertIn("Unsupported Media Test", response.json["message"])

    def test_internal_server_error_handler(self):
        """Test HTTP 500 handler."""
        response, code = error_handlers.internal_server_error("Internal Error Test")
        self.assertEqual(code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("Internal Error Test", response.json["message"])

    def test_data_validation_error_handler(self):
        """Test DataValidationError handling via Flask decorator."""
        error = DataValidationError("Invalid Data")
        response, code = error_handlers.request_validation_error(error)
        self.assertEqual(code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid Data", response.json["message"])
