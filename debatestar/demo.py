# This file creates the blueprint for Demo Page.
# It utilizes backend module of our trained NLP model
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

bp = Blueprint('demo', __name__)

# In-memory store of user input debate or the default one.
# Warning: this is very dangerous and vulnerable to many attacks
# debate = None

# View for the Demo: show the persuasivenss of given debate video
@bp.route('/demo')
def demo():
    return render_template('demo.html')

# View for the text: show the persuasivenss rating for user input debate script
@bp.route('/text', methods=['POST', 'GET'])
def text():

    # use the global debate dict
    # global debate
    
    if request.method == "POST":    
        # Gather user input. TODO validate user input
        title = request.form['topic']
        fortext = request.form['for-text']
        againsttext = request.form['against-text']
        debate = {
            'topic': title,
            'fortext': fortext,
            'againsttext': againsttext
        }
        # Call our model to compute the results. 
        forrate, againstrate = compute_score(title, fortext, againsttext)
        rate = {
            'for': forrate,
            'against': againstrate
        }
        # Render the results
        return render_template('result.html', debate=debate, rate=rate)
    
    # input boxes with default texts
    from .testmodel import capitalism, parent
    #if debate is None:
    debate = parent
    return render_template('text.html', debate=debate)


# Helper function to connect backend code with our model
# 
def compute_score(title, fortext, againsttext):
    from .model.run import predict
    result = predict(
        title=title,
        for_script=fortext,
        against_script=againsttext
    )
    return str(round(result * 100, 2)), str(round((1 - result) * 100, 2))