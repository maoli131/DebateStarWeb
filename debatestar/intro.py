# This file creates the blueprint for Introduction Page
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

bp = Blueprint('intro', __name__)

# View for Intro: show the static introduction page
@bp.route('/')
def index():
    return render_template('index.html')
    