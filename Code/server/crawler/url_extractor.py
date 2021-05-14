from urllib.parse import urlparse
from urllib.request import Request, urlopen
import validators
from bs4 import BeautifulSoup
from collections import deque
import sys 
import pymongo



client = pymongo.MongoClient("mongodb://localhost:27017/")
try:
    client.server_info()
except:
    print("MongoDB not online")
    raise
    
collection = client["db"]["UnChecked_URL"]


q = deque()
url_taken = set()
seed_url = sys.argv[1]
q.append(seed_url)
try:
    collection.insert_one({"_id":seed_url, "check":0})
except pymongo.errors.DuplicateKeyError:
    None


while q:
    cur_link = q.popleft()
    url_taken.add(cur_link)
    try :
    # code = urllib.request.urlopen(cur_link)
        req = Request(cur_link, headers={'User-Agent': 'Mozilla/5.0'})
        code = urlopen(req)
    except:
        print('errr')
        continue
    

    soup = BeautifulSoup(code.read(),'html.parser')
    for x in soup.find_all("a" , href = True) :
        extracted_link = x['href']
        if validators.url(extracted_link) and extracted_link not in url_taken :
            q.append(extracted_link)
            try:
                collection.insert_one({"_id":extracted_link, "check":0})
                print(extracted_link)
            except pymongo.errors.DuplicateKeyError:
                continue
    if(len(q)>1000):
        break
