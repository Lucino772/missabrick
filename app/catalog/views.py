from flask import render_template
from app.catalog import blueprint

@blueprint.route("/")
def index():
    return render_template("index.html")

@blueprint.route("/explore")
def explore():
    return render_template("explore.html")

@blueprint.route("/report")
def report():
    return render_template("report.html")
