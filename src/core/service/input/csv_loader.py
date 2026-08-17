"""CSV 로더."""

from core.service.input.base import FileLoader


class CsvLoader(FileLoader):
    def supports(self, path):
        ...

    def parse(self, text):
        ...
