from scrimme import scrimme
from flask import render_template


@scrimme.route('/home')
def home():
    return render_template('index.html')

@scrimme.route('/')
def index():
    return render_template('onboard.html')