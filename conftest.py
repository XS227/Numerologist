"""Pytest configuration for initializing Django."""

import os

import django


def pytest_configure() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tall_project.settings")
    django.setup()
