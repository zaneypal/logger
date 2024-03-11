import re

patterns = {
    'ip_address': re.compile(r"^((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])(\.(?!$)|$)){4}$"),
    'hostname': re.compile(r"^(?=.{1,255}$)[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?(?:\.[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?)*\.?$") 
}

def regex(pattern, text, exact=True):
    if exact==False:
        if re.search(pattern, text):
            result = str(re.search(pattern, text))
            print(f"Match Found: {result[result.find("'"):-1]}")
        else:
            print("No match found")
    else:
        if re.match(pattern, text):
            result = str(re.match(pattern, text))
            print(f"Match Found: {result[result.find("'"):-1]}")
        else:
            print("No match found")


message = 'word...this word is a word'
pattern = re.compile("word")

indexes = []
def multiregex(pattern, string, index_offset=0):
    try:
        result = str(re.search(pattern,string))
        #print(f"result: {result}\n")
        index = (int(result[result.find("(")+1:result.find(",")])+index_offset,int(result[result.find(",")+2:result.find(")")])+index_offset)
        #print(f"index: {index}\n")
        indexes.append(index)
        #print(f"indexes: {indexes}\n")

        current_endpoint = indexes[len(indexes)-1][1]
        #print(f"current_endpoint: {current_endpoint}\n")
        new_string = string[current_endpoint-index_offset:]
        #print(f"new_string: {new_string}\n")
        multiregex(pattern, new_string, current_endpoint)
    except ValueError:
        pass
    
multiregex(pattern, message)
for index in indexes:
    print(message[index[0]:index[1]])

#regex(pattern['ip_address'], "192.168.1.55")
#regex(pattern['ip_address'], "funny")
#regex(pattern['ip_address'], "255.255.255.256")
#regex(pattern['ip_address'], "255.255.255.255")
#
#regex(pattern['ip_address'], "192.168.1.55", False)
#regex(pattern['ip_address'], "funny", False)
#regex(pattern['ip_address'], "255.255.255.256", False)
#regex(pattern['ip_address'], "255.255.255.255", False)