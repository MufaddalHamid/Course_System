import uuid
import requests
from flask import Flask, jsonify, render_template
import os

import os
app = Flask(__name__, template_folder='Views', static_url_path='/static/')

# region Index
@app.route("/")
def home():
    if 'Login' == 'Student':
     return render_template('Forms/index.html')
# endregion

# region Login
@app.route("/Login")
def Login():
    return render_template('Forms/Login.html')
# endregion

if __name__ == "__main__":
    app.run(debug=True)