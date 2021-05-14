import pandas
import ipaddress as ip
from urllib.parse import urlparse
import urllib.request
import tldextract
from bs4 import BeautifulSoup
import validators
import re

def getContentFeatures(url, label=None): 
    result = []
    try:
        code = urllib.request.urlopen(url)
        soup = BeautifulSoup(code.read(),'html.parser')
    except:

        if not validators.url(url):
            url = "https://www."+str(url)
            
        try:
            code = urllib.request.urlopen(url)
            soup = BeautifulSoup(code.read(),'html.parser')
        except:
            return [-1,-1,-1,-1,-1,-1,-1]

    #add the url to feature set
    # result.append(url)
    
    #no of iframe tags
    result.append(len(soup.find_all('iframe')))
    
    #no of hidden elements
    result.append(len(soup.find_all(hidden=True)))
    
    #elements with small area 
    
    #no of script element
    result.append(len(soup.find_all('script')))
    
    
    #script with wrong file extension
    
    #% of scripting content
    
    #% of unknown tags
    
    #no of elements containing suspicious elements
    
    #no of suspicious object
    
    #% of white space in page 
    
    # presene of meta refreash tag
    result.append(int(int(len(soup.find_all(attrs={'http-equiv':'refresh'})))>0))
    
    
    #no of embed and objects  
    result.append(len(soup.find_all('object')))
    
    
    #elements whose source is on external domain
    
    
    #out of place elements
    
    #no. of urls 
    result.append(len(soup.find_all('script'))+len(soup.find_all('iframe'))+len(soup.find_all('frame'))+len(soup.find_all('embed'))+len(soup.find_all('form'))+len(soup.find_all('object')))
  
  
    #presence of double documents
    result.append(int((int(len(soup.find_all('html'))) > 1 or int(len(soup.find_all('head'))) > 1 or int(len(soup.find_all('body'))) > 1 or int(len(soup.find_all('title')) > 1 ))))
    
    
    #no. of known malicious patterns 
    
    #no. of charaters in page 
    
    # result.append(str(label))

    # returns a list of 7
    return result

