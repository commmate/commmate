"""Tests module."""

import flask


def create_test_app() -> flask.Flask:
    """Create webapi testing application."""
    test_app = create_flask_app('testing', config.Testing())
    io.init_app(test_app)
    return test_app


app = create_test_app()
