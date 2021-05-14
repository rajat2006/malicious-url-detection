import whois
import tldextract
import datetime

def get_features(url , label):
    result = []
    url = str(url)
    result.append(url)
    # url = "http://royalmail.reschedule-missed-parcel.com/"
    ext = tldextract.extract(url)
    domain = '.'.join(ext[1:])
    
    try:
        whois.query(domain)
    except:
        result.append('-1')
        result.append(str(label))
        return result
    else:
        w = whois.query(domain)
    
    if w is None:
        return result
    
    avg_month_time=365.2425/12.0
    
    #calculate creation age in months
    
    create_date = -1
    if w.creation_date == None or type(w.creation_date) is str :
        create_date = -1
    else:
        if(type(w.creation_date) is list): 
            create_date=w.creation_date[-1]
        else:
            create_date=w.creation_date
    
    #calculate expiry age in months
    
    expiry_date = -1
    if(w.expiration_date==None or type(w.expiration_date) is str):
        expiry_date = -1
    else:
        if(type(w.expiration_date) is list):
            expiry_date=w.expiration_date[-1]
        else:
            expiry_date=w.expiration_date

    if create_date == -1 or expiry_date == -1:
        result.append('-1')
    else:
        duration = round(((expiry_date - create_date).days)/avg_month_time)
        result.append(str(duration))
    result.append(str(label))
    return result