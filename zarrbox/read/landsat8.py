"""
Reader implementation for Landsat 8 data.

This module should:
- Implement Landsat 8-specific file parsing
- Handle band structure and metadata
- Use configuration from source-data/landsat8/config.json

Responsibilities:
- Map band names to files
- Apply scaling factors if needed
- Handle Landsat-specific quirks
"""
from base import BaseReader

class Landsat8Reader(BaseReader):

    def read_data(self):
        """(Source Specific: Reads data from source-specific data/file format to unified)"""
        raise NotImplementedError #for now as TBD

    def read_metadata(self):
        """(Source Specific: Reads metadata from source-specific metadata format to unified)"""
        raise NotImplementedError #for now as TBD
