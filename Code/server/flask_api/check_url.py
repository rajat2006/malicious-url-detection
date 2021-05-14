from flask import Flask, jsonify,  request, make_response
from joblib import load
from create_FVector_Improved import extract_features
import numpy as np
import json
import pymongo

import time
import threading


app = Flask(__name__)
class URL():
    def __init(self, url):
        self.URL = url
def class_predictor(url):
    model = load('version1_Lexical.pkl')
    feature = np.asarray(extract_features(url)).reshape(1,-1)
    return model.predict(feature)[0]

@app.route('/', methods = ['GET', 'POST'])
def testfn():

    if request.method == 'GET':
        return 'Success', 200
    if request.method == 'POST':
        Url = request.get_json()
        if client["db"]["benign"].find_one({"_id":Url}) is not None:
            print("Found in Benign DB")
            return jsonify('0')
        elif client["db"]["malicious"].find_one({"_id":Url}) is not None:
            print("Found in Malicious DB")
            return jsonify('1')  
        else:
            print("Predicting ... ")  
            result = class_predictor(Url) # 0 moved to function
            #print('ML predicted : ', result, type(result))
            print("ML Predicted :", result, type(result))
            if result==0:
                print(URL, "Added to Benign")
                try:
                    client["db"]["benign"].insert_one({"_id":Url})
                except pymongo.errors.DuplicateKeyError:
                    None
            else:
                print(URL, "Added to Malicious")
                try:
                    client["db"]["malicious"].insert_one({"_id":Url})
                except pymongo.errors.DuplicateKeyError:
                    None
            return jsonify(str(result))   

client = pymongo.MongoClient("mongodb://localhost:27017/")
try:
    client.server_info()
except:
    print("MongoDB server not online")
    raise
app.run(debug=True)