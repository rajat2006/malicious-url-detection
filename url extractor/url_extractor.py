from urllib.parse import urlparse
import urllib.request
import validators
from bs4 import BeautifulSoup
from collections import deque
import sys 

q = deque()
url_taken = set()
seed_url = sys.argv[1]
q.append(seed_url)

while q:
    cur_link = q.popleft()
    url_taken.add(cur_link)
    try :
        code = urllib.request.urlopen(cur_link)
    except : 
        continue
    soup = BeautifulSoup(code.read(),'html.parser')
    for x in soup.find_all("a" , href = True) :
        extracted_link = x['href']
        if validators.url(extracted_link) and extracted_link not in url_taken :
            q.append(extracted_link)
    if(len(q)>1000):
        break

    
file = open('url_to_check.txt','w')
file.write(str(q))