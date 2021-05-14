import pymongo
from bson.json_util import dumps
from joblib import load
from create_FVector_Improved import extract_features
import numpy as np

def class_predictor(url):
    model = load('version1_Lexical.pkl')
    feature = np.asarray(extract_features(url)).reshape(1,-1)
    return model.predict(feature)[0]

client = pymongo.MongoClient("mongodb://localhost:27017/")
try:
    client.server_info()
except:
    print("MongoDB server not online")
    raise
collection = client["db"]["UnChecked_URL"]
while(True):

    res = collection.find_one({"check":0})
    if res is None:
        continue
    
    
    result = class_predictor(res['_id'])
    collection.update_one({"_id":res['_id']},{"$set":{"check":1}})
    if result == 0:
        try:
            client["db"]["benign"].insert_one({"_id":res['_id']})
        except pymongo.errors.DuplicateKeyError:
            continue
    else:
        try:
            client["db"]["malicious"].insert_one({"_id":res['_id']})
        except pymongo.errors.DuplicateKeyError:
            continue
