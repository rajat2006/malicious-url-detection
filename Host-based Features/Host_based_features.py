#!/usr/bin/env python
# coding: utf-8

# In[1]:


import whois
import pandas as pd
import tldextract
import datetime


# In[2]:


df= pd.read_csv("final_dataset.csv")


# In[3]:


df.head(10)


# In[4]:


len(df)


# In[5]:


feature_set = pd.DataFrame(columns=('url', 'duration', 'label'))


# In[6]:


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


# In[7]:


for i in range(len(df)):
    features = get_features(df["url"].loc[i], df["label"].loc[i]) 
    if(len(features) == 3):
        print(features)
        feature_set.loc[i] = features
#     feature_set.loc[i] = features
    if i%100 == 0:
        print(len(feature_set.index))
print(feature_set.head())
print(len(feature_set.index))


# In[8]:


feature_set.to_csv("host_based_dataset.csv")


# In[16]:


from sklearn import svm
from sklearn.model_selection import cross_val_score, train_test_split
# from sklearn import cross_validation
from sklearn.metrics import confusion_matrix


# In[22]:


indexes = feature_set[feature_set['duration']== '-1'].index
feature_set.drop(indexes, inplace=True)
feature_set.groupby(feature_set['label']).size()


# In[23]:


X = feature_set.drop(['url','label'],axis=1).values
y = feature_set['label'].values


# In[24]:


X_train, X_test, y_train, y_test = train_test_split(X, y ,test_size=0.2)


# In[25]:


svm_model = svm.SVC()
svm_model.fit(X_train,y_train)
score = svm_model.score(X_test,y_test)
print(score)


# In[26]:


res = svm_model.predict(X)
mt = confusion_matrix(y, res)
print(mt)
print("False positive rate : %f %%" % ((mt[0][1] / float(sum(mt[0])))*100))
print('False negative rate : %f %%' % ( (mt[1][0] / float(sum(mt[1]))*100)))


# In[ ]:





# In[ ]:





# In[ ]:




