from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import and_, or_
from markupsafe import Markup
from regex import multiregex, html_insert, patterns
import os, csv, re, json, datetime

def get_exact_datetime():
    date = str(datetime.datetime.now()).replace("-", "").replace(":", "").replace(" ", "")
    return date[:date.find(".")]

class Base(DeclarativeBase):
    pass

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logger.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class recentFile(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    upload_date: Mapped[str] = mapped_column(nullable=False)

class loggerSession(db.Model):
    line: Mapped[int] = mapped_column(primary_key=True)
    hostname: Mapped[str]
    username: Mapped[str]
    ip_address: Mapped[str]
    date: Mapped[str]
    time: Mapped[str]
    request: Mapped[str]
    command: Mapped[str]
    protocol: Mapped[str]
    status_code: Mapped[str]
    data_in: Mapped[str]
    data_out: Mapped[str]
    file_size: Mapped[str]
    operating_system: Mapped[str]


with app.app_context():
    db.create_all() 

app.app_context().push()

# Redirects user to homepage when visting the site
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # Deletes all recently uploaded files from database
        if 'clear-recent' in request.form:
            recentFile.query.delete()
            db.session.commit()

        else:
            # User can upload logs as a file with this code
            if 'loggerfile' in request.files:
                file = request.files['loggerfile']
                filename = file.filename
                data = file.read()

            # Allows user to also upload logs by pasting text
            else:
                data = request.form['log-text-field'].encode()
                filename = 'Pasted Log'
            
            current_datetime = get_exact_datetime()
            db.session.add(recentFile(name=filename, content=data, upload_date=current_datetime))
            db.session.commit()
            tag = db.session.execute(db.select(recentFile.upload_date).where(recentFile.upload_date == current_datetime)).scalar()

            return redirect(url_for('view_log', file=filename, tag=tag))

    # Shows recently uploaded files
    recent = False
    recent_files = None
    if db.session.query(recentFile).count() > 0:
        recent = True
        recent_files = db.session.execute(db.select(recentFile).order_by(recentFile.upload_date.desc())).scalars()
    return render_template('index.html', turnOn=recent, recent_files=recent_files)


# Lets user view uploaded file on page
@app.route('/loggersession/<file>?tag=<tag>', methods=['GET', 'POST'])
def view_log(file, tag):
    if request.method == 'POST':
        if 'regex-query' in request.form:
            pattern = request.form['regex-query']
            return redirect(url_for('query_log', file=file, tag=tag, pattern=pattern))
    else:
        result_row = db.session.execute(db.select(recentFile).where(and_(recentFile.name == file, recentFile.upload_date == tag))).scalar()
        logs = result_row.content.decode().split('\n')
        return render_template('logger-session.html', logs=logs)

# Lets user find regex matches of uploaded log file
@app.route('/loggerquery/<file>?tag=<tag>?query=<pattern>', methods=['GET', 'POST'])
def query_log(file, tag, pattern):
    if request.method == 'POST':
        if 'regex-query' in request.form:
            pattern = request.form['regex-query']
            return redirect(url_for('query_log', file=file, tag=tag, pattern=pattern))

    else:
        result_row = db.session.execute(db.select(recentFile).where(and_(recentFile.name == file, recentFile.upload_date == tag))).scalar()
        log = result_row.content.decode()
        indexes = multiregex(pattern, log)
        result = html_insert(html_insert(log, indexes, "mark"), multiregex("\n", html_insert(log, indexes, "mark")), "br")
        result = Markup(result)
        
    return render_template('logger-query.html', result=result, pattern=f"'{pattern}'") 

if __name__ == '__main__':
    app.run(debug=True)