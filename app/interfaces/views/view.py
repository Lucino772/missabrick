import typing as t


class IView(t.Protocol):
    def render(self, template: str, **context):
        ...
