import re
from datetime import datetime

def format_date(date_str):
    formats = [
        '%B %d, %Y',
        '%m/%d/%Y',
        '%m/%d/%y',
        '%m.%d.%Y',
        '%m.%d.%y',
        '%m-%d-%Y',
        '%m-%d-%y',
        '%m%d%Y',
        '%m%d%y',
        '%Y/%m/%d',
        '%y/%m/%d',
        '%Y.%m.%d',
        '%y.%m.%d',
        '%Y-%m-%d',
        '%y-%m-%d',
        '%Y%m%d',
        '%y%m%d',
    ]
    for format in formats:
        try:
            date = datetime.strptime(date_str, format)
        except:
            date = False
        if date != False:
            break
    if date == False:
        date = None
    return f"{date.year}-{date.month}-{date.day}"

patterns = {
    'hostname': [1, re.compile(r"(?=.{1,255}$)[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?(?:\.[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?)*\.?")],
    'username': [1, re.compile(r"[a-z]{4,}\w+")],
    'ip_address': [1, re.compile(r"(?:25[0-5]|(?:2[0-4]|1[0-9]|[1-9]|)[0-9]\.){3}(?:25[0-5]|(?:2[0-4]|1[0-9]|[1-9]|)[0-9])")],
    'date': [2, re.compile(r"(?:[JFMASOND][a-z]{2,8} (?:(?:30|31)|[0-2]?[0-9]), \d{4})|(?:(?:\d{1,2}(?:\/|\.|-| |)){2}\d{2,4})")],
    'time': [1, re.compile(r"(?:(?:1[0-2]|0?[0-9])(?::[0-5][0-9]){1,2} ?(?:AM|PM)?)|(?:(?:2[0-3]|1[0-9]|0?[0-9])(?::[0-5][0-9]){1,2})", re.IGNORECASE)],
    'request': [1, re.compile(r"(?:GET|HEAD|POST|PUT|DELETE|CONNECT|OPTIONS|TRACE|PATCH)", re.IGNORECASE)],
    'command': [1, re.compile(r"")],
    'protocol': [1, re.compile(r"(?:TCP/IP|SMTP|PPP|FTP|SFTP|HTTPS?|TELNET|POP3|IPV[46]|ICMP|UDP|IMAP|SSH|Gopher)", re.IGNORECASE)],
    'status_code': [1, re.compile(r"[1-5][0-9]{2}")],
    'data_in': [1, re.compile(r"\d+[kmgtpezyKMGTPEZY][bB](?: |)in")],
    'data_out': [1, re.compile(r"\d+[kmgtpezyKMGTPEZY][bB](?: |)out")],
    'file_size': [1, re.compile(r"\d+[kmgtpezyKMGTPEZY][bB](?: |)")],
    'operating_system': [1, re.compile(r"(?:windows|mac|linux|ubuntu|fedora|freebsd|android|solaris|ms-dos)", re.IGNORECASE)]
}

# Finds the index (character start and end positions) of all substrings matching the regex queried by user
def multiregex(pattern, msg, indexes=[], index_offset=0, new_session=True):
    try:
        if new_session == True:
            indexes = []
        result = str(re.search(pattern,msg))
        index = (int(result[result.find("(")+1:result.find(",")])+index_offset,int(result[result.find(",")+2:result.find(")")])+index_offset)
        indexes.append(index)

        current_endpoint = indexes[len(indexes)-1][1]
        new_string = msg[current_endpoint-index_offset:]
        multiregex(pattern, new_string, indexes, current_endpoint, new_session=False)
    except ValueError:
        pass
    return indexes

# Inserts the desired HTML element tag into the corresponding indexes
def html_insert(charlist, indexlist, tag):
    charlist = list(charlist)
    for start, end in reversed(indexlist):
        if tag == "br":
            for ch in "<br />"[::-1]:
                charlist.insert(end, ch)
        else:
            for ch in f"</{tag}>"[::-1]:
                charlist.insert(end, ch)
            for ch in f"<{tag}>"[::-1]:
                charlist.insert(start, ch)
    return "".join(charlist)
