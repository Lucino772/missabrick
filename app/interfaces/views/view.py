import typing as t


class IView(t.Protocol):
    def render(self, template: str, **context):
        ...

    def send_file(self, filename: str, source: str, type: str, fd: int = None):
        ...
