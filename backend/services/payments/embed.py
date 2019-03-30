from flask import send_file
from webargs.fields import *
from webargs.flaskparser import use_args

from backend.services.payments import bp

theme_map = {"hollow": "h", "solid": "b", "minimal": "u"}


def get_name(price=50, theme="minimal"):
    if not theme in theme_map.keys():
        theme = "minimal"
    return "static/embed/{}_{}.png".format(theme_map[theme], price)


@bp.route("/embed", methods=["GET"])
@use_args(
    {
        "price": Int(missing=50, validate=lambda p: p in [10, 20, 25, 50, 75, 100]),
        "theme": Str(missing="minimal"),
    }
)
def embed_img(args):
    theme = args["theme"]
    filename = get_name(args["price"], theme)
    return send_file(filename, mimetype="image/png")
