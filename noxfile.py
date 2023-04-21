import os

import nox


@nox.session
def lint(session: nox.Session):
    session.install("pre-commit")
    session.run("pre-commit", "run", *session.posargs)

@nox.session
def upload(session: nox.Session):
    session.install("twine")
    upload_cmd = []
    if os.path.exists(".env.deploy"):
        session.install("python-dotenv[cli]")
        upload_cmd = ["dotenv", "-f", ".env.deploy", "run", "--"]

    upload_cmd.extend(["twine", "upload", "dist/*"])
    session.run(*upload_cmd)
