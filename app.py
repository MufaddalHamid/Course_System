import uuid
from flask import Flask, jsonify, render_template, request
import os
from Logic.AppHelper import ActiveSession

app = Flask(__name__, template_folder='Views', static_url_path='/static/')

# region Index
@app.route("/")
def home():
    return render_template('Forms/index.html')
# endregion

# region Login
@app.route("/login", methods=['GET', 'POST'])
def Login():
    if (request.method == "POST"):
        email = request.form.get("email")
        password = request.form.get("password")
        rememberMe = request.form.get("remember")
    return render_template('Forms/Login.html')
# endregion

if __name__ == "__main__":
    app.run(debug=True)