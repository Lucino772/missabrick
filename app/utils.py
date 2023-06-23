import os

from flask import make_response


def _stream_file_and_remove(filename: str, fd: int = None):
    open_path = filename if fd is None else fd

    with open(open_path, "rb", closefd=True) as fp:
        yield from fp

    os.remove(filename)


def send_file(filename: str, source: str, type: str, fd: int = None):
    nbytes = os.stat(source).st_size
    resp = make_response(_stream_file_and_remove(source, fd))
    resp.headers["Content-Disposition"] = f"inline; filename={filename}"
    resp.headers["Content-Length"] = nbytes
    resp.headers["Content-Type"] = type
    resp.headers["filename"] = filename
    return resp


def getenv(key: str, default=None, prefix: str = "MISSABRICK"):
    return os.getenv(f"{prefix}_{key}", default)
