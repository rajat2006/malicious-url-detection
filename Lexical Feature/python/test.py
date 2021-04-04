from joblib import load
from create_FVector import extract_features
import numpy as np

Url = ""
model = load('version1_Lexical.pkl')
feature = np.asarray(extract_features(Url)).reshape(1,-1)
model.predict(feature)