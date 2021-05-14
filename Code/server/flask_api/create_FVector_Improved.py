from urllib.parse import urlparse
import tldextract
import re
import ipaddress as ip




suspicious_TLD = ['country' , 'kim' , 'science', 'gq', 'work', 'ninja', 'xyz', 'date', 'faith', 'zip', 'racing', 'cricket', 'win','space','accountant','realtor','top','stream','christmas','gdn','mom','pro','men']


shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                      r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                      r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                      r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                      r"tr\.im|link\.zip\.net"
def is_ip(url):
    try:
        if ip.ip_address(url):
            return 1
    except:
            return 0
def count_subdomain(sub):
    if not sub:
        return 0
    else:
        return len(sub.split('.'))

def extract_features(url):
    vector = []
    path  = urlparse(url)
    ext = tldextract.extract(url)
    #print(path,ext)


    vector.append(len(url))
    vector.append(url.count('.'))
    vector.append(1 if ext.suffix in suspicious_TLD else 0)
    vector.append(url.count('-'))
    vector.append(path.path.count('/'))
    vector.append(len(path.netloc))
    vector.append(is_ip(url))
    vector.append(url.count('//'))
    vector.append(1 if re.search(shortening_services, url) else 0)
    vector.append(count_subdomain(ext.subdomain))
    vector.append(path.query.count('='))
    vector.append(url.count('@'))
    vector.append(0 if path.path.find('%20')==-1 else 1)
    d=l=spc=0
    for c in url:
        if c.isdigit():
            d=d+1
        elif c.isalpha():
            l=l+1
        else:
            pass
    for c in path.path:
        if c.isdigit():
            pass
        elif c.isalpha():
            pass
        else:
            spc+=1
    vector.append(d/(l if l!=0 else 1))
    vector.append(spc)
    ls = [0, 14, 4, 10, 3, 13, 9, 11, 1, 12]
    vector = [vector[i] for i in ls]
    return vector
