from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import os, csv

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///txtfiles.db'
#db = SQLAlchemy(app)

filetype_paths = {
    'txt': None,
    'csv': None
}

for filetype in filetype_paths:
    for dir in os.listdir("static"):
        if dir.__contains__(filetype):
            filetype_paths[filetype] = f"static/{dir}"

app.config['txt'] = filetype_paths['txt']
app.config['csv'] = filetype_paths['csv']

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if 'loggerfile' in request.files:
            file = request.files['loggerfile']
            filename = file.filename
            file.save(os.path.join(app.config[filename[filename.find(".")+1:]], filename))
            return redirect(url_for('view_log', file=filename))
        else:
            message = request.form['log-text-field']
            return message
    return render_template('index.html')

@app.route('/loggerfile/<file>', methods=['GET'])
def view_log(file):
    if file.endswith('.txt'):
        with open(f"{filetype_paths['txt']}/{file}", 'r', encoding='utf-8') as txt_file:
            entries = txt_file.readlines()
            return entries
    #elif file.endswith('.csv'):
    #    with open(f"{filetype_paths['csv']}/{file}")
    else:
        return "Page not found"


if __name__ == '__main__':
    app.run(debug=True)