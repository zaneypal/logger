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
        if 'clear-recent' in request.form:
            with open("static/cache/recent.txt", 'w') as delete_data:
                delete_data.close()
            for filetype in filetype_paths:
                for file in os.listdir(filetype_paths[filetype]):
                    os.remove(os.path.join(filetype_paths[filetype], file))
        else:
            if 'loggerfile' in request.files:
                file = request.files['loggerfile']
                filename = file.filename
                filetype = filename[filename.find(".")+1:]
                file.save(os.path.join(app.config[filetype], filename))

                with open("static/cache/recent.txt", 'a+') as save_data:
                    save_data.write(filename+'\n')
                    #save_data.close()

            else:
                message = request.form['log-text-field']
                with open("static/txt-files/newfile.txt", 'w+') as save_data:
                    save_data.write(message)
                filename='newfile.txt'
                filetype='txt'
            
            return redirect(url_for('view_log', file=filename[:filename.find(".")], type=filetype))

    # Debug Needed    # # #
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

@app.route('/loggersession/<file>.<type>', methods=['GET'])
def view_log(file, type:str):
    filename = f"{file}.{type}"

    with open(f"{filetype_paths[type]}/{filename}", 'r', encoding='utf-8') as opened_file:
        lines = opened_file.readlines()
        return render_template('logger-session.html', lines=lines)

if __name__ == '__main__':
    app.run(debug=True)