from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from markupsafe import Markup
from regex import multiregex, html_insert, patterns
import os, csv, re

app = Flask(__name__)
# Two lines below are not used in this phase but may need to be used later on.
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///txtfiles.db'
#db = SQLAlchemy(app)

# Stores the pathnames of the directories that hold user-uploaded files
filetype_paths = {
    'txt': None,
    'csv': None
}

# Locates the paths of needed directories from the static folder
for filetype in filetype_paths:
    for dir in os.listdir("static"):
        if dir.__contains__(filetype):
            filetype_paths[filetype] = f"static/{dir}"

# Applying the configurations made necessary by Flask
app.config['txt'] = filetype_paths['txt']
app.config['csv'] = filetype_paths['csv']

# Redirects user to homepage when visting the site
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # Deletes all recently uploaded files from history
        if 'clear-recent' in request.form:
            with open("static/cache/recent.txt", 'w') as delete_data:
                delete_data.close()
            for filetype in filetype_paths:
                for file in os.listdir(filetype_paths[filetype]):
                    os.remove(os.path.join(filetype_paths[filetype], file))
        else:
            # User can upload logs as a file with this code
            if 'loggerfile' in request.files:
                file = request.files['loggerfile']
                filename = file.filename
                filetype = filename[filename.find(".")+1:]
                file.save(os.path.join(app.config[filetype], filename))

                with open("static/cache/recent.txt", 'a+') as save_data:
                    save_data.write(filename+'\n')

            # Allows user to also upload logs by pasting text
            else:
                message = request.form['log-text-field']
                with open("static/txt-files/newfile.txt", 'w+') as save_data:
                    save_data.write(message)
                filename='newfile.txt'
                filetype='txt'
            
            return redirect(url_for('view_log', file=filename[:filename.find(".")], type=filetype))

    # Debug Needed    # # #
    # Goal is to display names of recently uploaded files on homepage screen
    recent, recent_files = False, None
    storage = []
    with open("static/cache/recent.txt", 'r', encoding='utf-8') as read_data:
        if read_data.readlines():
            recent = True
            for line in read_data.readlines():
                storage.append(line)
            recent_files = str(storage)

    return render_template('index.html', turnOn=recent, recent_files=recent_files)
    # Debug Needed    # # #

# Lets user view uploaded file on page
@app.route('/loggersession/<file>.<type>', methods=['GET', 'POST'])
def view_log(file, type:str):
    filename = f"{file}.{type}"
    abs_filepath = f"{filetype_paths[type]}/{filename}"

    if request.method == 'POST':
        if 'regex-query' in request.form:
            pattern = request.form['regex-query']
            return redirect(url_for('query_log', file=filename, pattern=pattern))
    else:
        with open(abs_filepath, 'r', encoding='utf-8') as opened_file:
            lines = opened_file.readlines()
            return render_template('logger-session.html', lines=lines)

# Lets user find regex matches of uploaded log file
@app.route('/loggerquery/<file>/query=<pattern>', methods=['GET', 'POST'])
def query_log(file, pattern):
    type = file[file.find(".")+1:]
    abs_filepath = f"{filetype_paths[type]}/{file}"

    with open(abs_filepath, 'r', encoding='utf-8') as read_data:
        log = str(read_data.read())
        indexes = multiregex(pattern, log)
        result = html_insert(html_insert(log, indexes, "mark"), multiregex("\n", html_insert(log, indexes, "mark")), "br")
        result = Markup(result)

    if request.method == 'POST':
        if 'regex-query' in request.form:
            pattern = request.form['regex-query']
            return redirect(url_for('query_log', file=file, pattern=pattern))
        
    return render_template('logger-query.html', result=result, pattern=f"'{pattern}'") 

if __name__ == '__main__':
    app.run(debug=True)