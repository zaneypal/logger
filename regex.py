import re

pattern = {
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


#regex(pattern['ip_address'], "192.168.1.55")
#regex(pattern['ip_address'], "funny")
#regex(pattern['ip_address'], "255.255.255.256")
#regex(pattern['ip_address'], "255.255.255.255")
#
#regex(pattern['ip_address'], "192.168.1.55", False)
#regex(pattern['ip_address'], "funny", False)
#regex(pattern['ip_address'], "255.255.255.256", False)
#regex(pattern['ip_address'], "255.255.255.255", False)