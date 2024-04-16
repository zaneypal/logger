from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import and_, or_
from markupsafe import Markup
from regex import multiregex, html_insert, patterns, format_date
import os, csv, re, json, datetime

def get_exact_datetime():
    date = str(datetime.datetime.now()).replace("-", "").replace(":", "").replace(" ", "")
    return date[:date.find(".")]

class Base(DeclarativeBase):
    pass

app = Flask(__name__)
app.jinja_env.globals.update(len=len)
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
    config: Mapped[bool]
    data: Mapped[str]

with app.app_context():
    db.create_all() 

app.app_context().push()

logger_config = "hostname,username,ip_address,date,time,request,command,protocol,status_code,data_in,data_out,file_size,operating_system"

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
        loggerSession.query.delete()
        db.session.add(loggerSession(config=True, data=logger_config))
        db.session.commit()
        
        logs_result = db.session.execute(db.select(recentFile).where(and_(recentFile.name == file, recentFile.upload_date == tag))).scalar()
        logs = logs_result.content.decode().split('\n')

        logger_data = {}
        logger_fields = logger_config.split(',')
        for field in logger_fields:
            logger_data[field] = ""

        for line in logs:
            logger_data_str = ""
            for field in logger_data.keys():
                if match:= re.search(patterns[field][1], line):
                    if patterns[field][0] == 1:
                        logger_data[field]=match.group()
                    elif patterns[field][0] == 2:    
                        logger_data[field]=format_date(match.group())
                if field == list(logger_data.keys())[-1]:
                    logger_data_str += logger_data[field]
                else:
                    logger_data_str += f"{logger_data[field]},"
            db.session.add(loggerSession(config=False, data=logger_data_str))     
            db.session.commit()

        logger_result = loggerSession.query.filter(loggerSession.config == False).all()
        header_result = loggerSession.query.filter(loggerSession.config == True).scalar()
        
        temp = []
        field_data = []
        for res in logger_result:
            temp.append(res.data)
        for data in temp:
            field_data.append(data.split(','))

        temp = str()
        temp += header_result.data
        temp = temp.split(",")
        header_data = []
        for data in temp:
            header_data.append(data.replace("_", " ").title())

        no_empty_lines = []
        for line in logs:
            if line.isspace():
                pass
            else:
                no_empty_lines.append(line)
        
        return render_template('logger-session.html', logs=logs, headers=header_data, fields=field_data, no_empty_lines=no_empty_lines)

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
        results = html_insert(html_insert(log, indexes, "mark"), multiregex("\n", html_insert(log, indexes, "mark")), "br")
        results = Markup(results)
        
        # Testing something out to see if I can get data to display line by line instead of in a clump
        results = results.split("<br />")
        matches_only = []
        for result in results:
            if re.search(r"<mark>.*</mark>", result):
                matches_only.append(result)
        no_empty_lines = []
        for line in results:
            if line.isspace():
                pass
            else:
                no_empty_lines.append(line)
        
    return render_template('logger-query.html', results=results, matches_only=matches_only, no_empty_lines=no_empty_lines, pattern=f"'{pattern}'")

@app.route('/test')
def test():
    return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True)