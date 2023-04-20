from app.catalog import blueprint

@blueprint.route("/")
def index():
    return "Hello World !"
