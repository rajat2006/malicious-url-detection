import pandas as pd
from get_host_based_features import get features
from sklearn import svm
from sklearn.model_selection import cross_val_score, train_test_split
# from sklearn import cross_validation
from sklearn.metrics import confusion_matrix

df= pd.read_csv("final_dataset.csv")

feature_set = pd.DataFrame(columns=('url', 'duration', 'label'))

for i in range(len(df)):
    features = get_features(df["url"].loc[i], df["label"].loc[i]) 
    if(len(features) == 3):
        # print(features)
        feature_set.loc[i] = features
#     feature_set.loc[i] = features
    # if i%100 == 0:
        # print(len(feature_set.index))

indexes = feature_set[feature_set['duration']== '-1'].index
feature_set.drop(indexes, inplace=True)
feature_set.groupby(feature_set['label']).size()

X = feature_set.drop(['url','label'],axis=1).values
y = feature_set['label'].values

X_train, X_test, y_train, y_test = train_test_split(X, y ,test_size=0.2)

svm_model = svm.SVC()
svm_model.fit(X_train,y_train)
score = svm_model.score(X_test,y_test)
print(score)

res = svm_model.predict(X)
mt = confusion_matrix(y, res)
print(mt)
print("False positive rate : %f %%" % ((mt[0][1] / float(sum(mt[0])))*100))
print('False negative rate : %f %%' % ( (mt[1][0] / float(sum(mt[1]))*100)))