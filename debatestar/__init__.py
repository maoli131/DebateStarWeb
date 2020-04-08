import os

from flask import Flask, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # DATABASE=os.path.join(app.instance_path, 'debatestar.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # register the intro blueprint
    from . import intro
    app.register_blueprint(intro.bp)
    app.add_url_rule('/', endpoint='index')

    # register the demo blueprint
    from . import demo
    app.register_blueprint(demo.bp)

    # register the team blueprint
    from . import team
    app.register_blueprint(team.bp)

    # error handler
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World! You find our Easter Egg. Willing to join us?'

    return app