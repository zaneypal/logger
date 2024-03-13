import re
from debug import debug

patterns = {
    'ip_address': re.compile(r"^((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])(\.(?!$)|$)){4}$"),
    'hostname': re.compile(r"^(?=.{1,255}$)[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?(?:\.[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?)*\.?$") 
}

message2 = """random message
in here mtttts
mmmhhusssmsyuuh
283628:)!"""
pattern = r"m.{4}s"

def multiregex(pattern, msg, indexes, index_offset=0, new_session=True):
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

indexes = multiregex(pattern, message2, indexes=[])
message = list(message2)

def html_insert(start, end, list, tag):
    if tag == "br":
        for ch in "<br />"[::-1]:
            list.insert(end, ch)
    else:
        for ch in f"</{tag}>"[::-1]:
            list.insert(end, ch)
        for ch in f"<{tag}>"[::-1]:
            list.insert(start, ch)

for start, end in reversed(indexes):
    html_insert(start, end, message, "mark")

new_string = "".join(message)

for start, end in reversed(multiregex("\n", new_string, indexes=[])):
    html_insert(start, end, message, "br")

print(newer_string := "".join(message))
