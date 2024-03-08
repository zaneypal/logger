from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import os, csv

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///txtfiles.db'
#db = SQLAlchemy(app)

txt = 'static/txt'
app.config['txt'] = txt

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        file = request.files['loggerfile']
        if 'loggerfile' not in request.files:
            return "Upload unsuccessful"
        else:
            file.save(os.path.join(app.config['txt'], filename:=file.filename))
            return redirect(url_for('view_log', file=filename))
    return render_template('index.html')

@app.route('/loggerfile/<file>', methods=['GET'])
def view_log(file):
    if file.endswith('.txt'):
        with open(f"{txt}/{file}", 'r', encoding='utf-8') as txt_file:
            entries = txt_file.readlines()
            return entries
    else:
        return "Page not found"


if __name__ == '__main__':
    app.run(debug=True)