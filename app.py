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
            filetype = filename[filename.find(".")+1:]
            file.save(os.path.join(app.config[filetype], filename))
            return redirect(url_for('view_log', file=filename[:filename.find(".")], type=filetype))
        else:
            message = request.form['log-text-field']
            return message
    return render_template('index.html')

@app.route('/loggersession/<file>.<type>', methods=['GET'])
def view_log(file, type:str):
    filename = f"{file}.{type}"
    with open(f"{filetype_paths[type]}/{filename}", 'r', encoding='utf-8') as opened_file:
        lines = opened_file.readlines()
        return render_template('logger-session.html', lines=lines)

if __name__ == '__main__':
    app.run(debug=True)