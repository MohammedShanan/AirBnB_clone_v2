#!/usr/bin/python3
"""Start web application with two routings
"""

from models import storage
from models.state import State
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/states", strict_slashes=False)
@app.route("/states/<id>", strict_slashes=False)
def states_list(id=None):
    """Render template with states"""
    path = "9-states.html"
    states = storage.all(State)
    the_state = None
    if id:
        for state in states.values():
            if state.id == id:
                the_state = state
    if the_state:
        states = None
    return render_template(path, states=states, state=the_state)


@app.teardown_appcontext
def app_teardown(arg=None):
    """Clean-up session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
