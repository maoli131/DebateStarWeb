# This file creates the blueprint for Team Page.
# It introduces our story and our mission.
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

bp = Blueprint('team', __name__)

# View for the team: show the persuasivenss of given debate
@bp.route('/team')
def team():
    return render_template('team.html')