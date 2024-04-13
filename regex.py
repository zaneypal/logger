import re

patterns = {
    'hostname': re.compile(r"(?=.{1,255}$)[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?(?:\.[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?)*\.?"),
    'username': re.compile(r""),
    'ip_address': re.compile(r"(?:25[0-5]|(?:2[0-4]|1[0-9]|[1-9]|)[0-9]\.){3}(?:25[0-5]|(?:2[0-4]|1[0-9]|[1-9]|)[0-9])"),
    'date': re.compile(r""),
    'time': re.compile(r""),
    'request': re.compile(r""),
    'command': re.compile(r""),
    'protocol': re.compile(r""),
    'status_code': re.compile(r""),
    'data_in': re.compile(r""),
    'data_out': re.compile(r""),
    'file_size': re.compile(r""),
    'operating_system': re.compile(r"")
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