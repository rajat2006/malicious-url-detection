from getFeaturesLexical import getLexicalFeatures
from getFeaturesHost import getHostFeatures
from getFeaturesContent import getContentFeatures
import csv
import pymongo

# client for accessing db
myclient1 = pymongo.MongoClient("mongodb://localhost:27017/")
myclient2 = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient1["url_list"]
mycol = mydb["host_based_features"]
cursor = mycol.find({})

finaldb = myclient2["feature_list"]
finalcol = finaldb["features"]


# function to get 3 types of features from the url
def getFeatures(url, label=None):
    lexical_features = getLexicalFeatures(url)
    # host_features = getHostFeatures(url)
    
    # getting host based features
    d = dict()
    dur = -1
    try:
        d = cursor.next()
    except:
        pass
    else:
        dur = int(d['duration'])
        
    host_features = [dur]
    content_features = getContentFeatures(url)
    all_features = lexical_features + host_features + content_features
    # print(all_features)

        
    return all_features

def store():
    count = 0
    countm = 0
    countb = 0
    with open('final_dataset.csv') as csv_file:
        reader = csv.reader(csv_file)
        next(csv_file)
        for row in reader:
            # print(row)
            # print("getting features")
            all_features = getFeatures(row[0])
            # print("got features")
            all_features.append(int(row[1]))
            all_features = [row[0]] + all_features

            if -1 not in all_features:
                # print("inside")
                

                count += 1
                if int(row[1]) == 1:
                    countm += 1
                else:
                    countb += 1

                

                # print(all_features)
                # break
                print(count)

            # print(len(all_features))
            store_db(all_features)
    print("malicious", countm)
    print("benign", countb)

def store_db(all_features):

    d = {
        'url' : all_features[0],
        'url_length' : all_features[1],
        'dots_count': all_features[2],
        'suspicious_tld': all_features[3],
        'hyphen_count': all_features[4],
        'subdir_count': all_features[5],
        'domain_length': all_features[6],
        'ip_present': all_features[7],
        'double_slash_count': all_features[8],
        'url_shortening_service': all_features[9],
        'count_subdomain_domain_tokens': all_features[10],
        'count_queries': all_features[11],
        'count_at_symbol': all_features[12],
        'presence_of_%20': all_features[13],
        'digit/letter': all_features[14],
        'special_char': all_features[15],
        'duration': all_features[16],
        'number_of_iframe_tags': all_features[17],
        'number_of_hidden_elements': all_features[18],
        'number_of_script_elements': all_features[19],
        'number_of_meta_refresh_tags': all_features[20],
        'number_of_object_tags': all_features[21],
        'number_of_urls': all_features[22],
        'presence_of_double_document': all_features[23],
        'label': all_features[24],
    }

    finalcol.insert_one(d)

