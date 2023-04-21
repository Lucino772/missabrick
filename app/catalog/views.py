from flask import render_template, request
from app.catalog import blueprint

from app.catalog.utils import search_sets

@blueprint.route("/")
def index():
    return render_template("index.html")

@blueprint.route("/explore")
def explore():
    page = int(request.args.get('page', 1))
    search = request.args.get('search', '')
    page_size = int(request.args.get('page_size', 20))

    pagination = search_sets(search, page, page_size)
    return render_template("explore.html", search=search, pagination=pagination)

@blueprint.route("/download/<set_number>")
def download(set_number: int):
    pass

@blueprint.route("/report")
def report():
    return render_template("report.html")
