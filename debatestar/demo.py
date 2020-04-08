# This file creates the blueprint for Demo Page.
# It utilizes backend module of our trained NLP model
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

bp = Blueprint('demo', __name__)

# View for the Demo: show the persuasivenss of given debate video
@bp.route('/demo')
def demo():
    return render_template('demo.html')

# View for the text: show the persuasivenss rating for user input debate script
@bp.route('/text')
def text():
    return render_template('text.html')