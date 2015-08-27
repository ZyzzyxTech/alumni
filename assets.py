# -*- coding: utf-8 -*-
__author__ = 'Ken'

from flask_assets import Bundle, Environment

css = Bundle(
    "css/normalize.css",
    "css/foundation.css",
    "css/styles.css",
    filters="cssmin",
    output="public/css/common.css"
)

js = Bundle(
    "js/deleteme.js",
    filters="jsmin",
    output="public/js/common.js"
)

assets = Environment()

assets.register("js_all", js)
assets.register("css_all", css)
