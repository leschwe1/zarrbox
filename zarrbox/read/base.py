from abc import ABC, abstractmethod
from pathlib import Path
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

class BaseReader(ABC):
    def __init__(self, path):
        self.path = Path(path)

    @abstractmethod
    def read_data(self):
        """(Source Specific: Reads data from source-specific data/file format to unified)"""
        pass

    @abstractmethod
    def read_metadata(self):
        """(Source Specific: Reads metadata from source-specific metadata format to unified)"""
        pass

    def to_zarr(self, path):
        """Writes data out to .zarr file"""
        raise NotImplementedError #for now as TBD

    def to_dataset(self):
        """keeps Data as lazy loaded dataset for further processing"""
        raise NotImplementedError #for now as TBD

