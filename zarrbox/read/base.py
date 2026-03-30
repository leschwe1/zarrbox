"""
Base classes and shared logic for all data readers.

This module should:
- Define an abstract base class (e.g. BaseReader)
- Standardize the interface for all readers

Typical methods:
- load()
- validate()
- get_metadata()
- read_bands()

All sensor-specific readers must inherit from this class.
"""