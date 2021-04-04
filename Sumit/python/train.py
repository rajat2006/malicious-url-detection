import pandas as pd
import ipaddress as ip
import re
from create_FVector import extract_features
import numpy as np

# Dataset
print("-----Reading Dataset-----")
data = pd.read_csv("final_dataset.csv").sample(frac=1).reset_index(drop=True)
print("-----Dataset Read-----")

# FeatureSet
featureSet = pd.DataFrame(columns=('URL_Length', 'Dots_Count', 'Suspicious_TLD', 'Hyphen_Count', \
                                    'Subdir_Count', 'Domain_Length', 'IP_Present','Double_Slash_Count', \
                                    'URL_Shortening_Service', 'Count_SubDomain (Domain_Tokens)', 'Count_Queries', 'Count_At_Symbol', \
                                    'Presence of %20', 'digit/letter', 'special_characters'))

# Getting Features
print("-----Extracting Features-----")
for i in range(len(data)):
    featureSet.loc[i] = extract_features(data["url"].loc[i])
print("-----Features Extracted-----")

# Chart 
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
#apply SelectKBest class to extract top 10 best features
bestfeatures = SelectKBest(score_func=chi2, k=10)
X = featureSet
y = data['label']
fit = bestfeatures.fit(X,y)
dfscores = pd.DataFrame(fit.scores_)
dfcolumns = pd.DataFrame(X.columns)
#concat two dataframes for better visualization 
featureScores = pd.concat([dfcolumns,dfscores],axis=1)
featureScores.columns = ['Specs','Score']  #naming the dataframe columns
print(featureScores.nlargest(10,'Score'))  #print 10 best features


from sklearn.ensemble import ExtraTreesClassifier
import matplotlib.pyplot as plt
model = ExtraTreesClassifier()
model.fit(X,y)
#print(model.feature_importances_) #use inbuilt class feature_importances of tree based classifiers
#plot graph of feature importances for better visualization
feat_importances = pd.Series(model.feature_importances_, index=X.columns)
feat_importances.nlargest(10).plot(kind='barh')
plt.show()

# 75% malicious 25% benign (Based on Dataset %)
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
X = featureSet.values
y = data['label'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True, stratify=y,random_state=0)



# TRAINING

## SVM 
print("-----Training SVM Model-----")
model = SVC(kernel='linear')
model.fit(X_train, y_train)
score = model.score(X_test, y_test)
print("SVM Accuracy : ", score)

## Random Forest
print("-----Training Random Forest Model-----")
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics 
model = RandomForestClassifier(n_estimators = 100)  
# Training the model on the training dataset
# fit function is used to train the model using the training sets as parameters
model.fit(X_train, y_train)
# performing predictions on the test dataset
y_pred = model.predict(X_test)
# metrics are used to find accuracy or error
# using metrics module for accuracy calculation
print("Random Forest Accuracy: ", metrics.accuracy_score(y_test, y_pred))


# Saving the Model
from joblib import dump, load
print("-----Model Saved-----")
dump(model, 'version1_Lexical.pkl')
