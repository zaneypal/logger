import re
from debug import debug

patterns = {
    'ip_address': re.compile(r"^((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])(\.(?!$)|$)){4}$"),
    'hostname': re.compile(r"^(?=.{1,255}$)[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?(?:\.[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?)*\.?$") 
}

message = 'word...this word is a word'
message2= "not a word, so no, not a word."
pattern = re.compile("word")
indexes = []

def multiregex(pattern, string, indexes, index_offset=0, new_session=True, inverse=False):
    try:
        if new_session == True:
            indexes = []
            
        result = str(re.search(pattern,string))
        index = (int(result[result.find("(")+1:result.find(",")])+index_offset,int(result[result.find(",")+2:result.find(")")])+index_offset)
        indexes.append(index)

        current_endpoint = indexes[len(indexes)-1][1]
        new_string = string[current_endpoint-index_offset:]
        multiregex(pattern, new_string, indexes, current_endpoint, new_session=False)
    except ValueError:
        pass

    if inverse == True:
        inverse_indexes = []
        counter = 0
        for index in indexes:
            if counter == 0: 
                if index[0] != 0:
                    inverse_indexes.append((0, index[0]))
                else:
                    inverse_indexes.append((indexes[counter][1], indexes[counter+1][0]))
            else:
                inverse_indexes.append((indexes[counter-1][1], indexes[counter][0]))
            if (indexes[-1][1] < len(string)) and index == indexes[-1]:
                inverse_indexes.append((indexes[counter][1], len(string)))
            counter += 1
        indexes = inverse_indexes
    return indexes

print(multiregex(pattern, message2, indexes))
print(multiregex(pattern, message2, indexes, inverse=True))

#for index in multiregex(pattern, message, indexes):
#    print(message[index[0]:index[1]])
