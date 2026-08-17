"""터미널 출력."""

from core.service.output.base import Reporter


class ConsoleReporter(Reporter):
    def format(self, result):
        ...
