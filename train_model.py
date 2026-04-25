import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier

from utils.feature_extraction import extract_features

df = pd.read_csv("dataset/final_url_dataset.csv")

urls = df['url']
labels = df['label']

features = []
valid_labels = []

print("Extracting features...")

for i in range(len(urls)):
    try:
        feat = extract_features(urls[i])
        features.append(feat)
        valid_labels.append(labels[i])
    except:
        continue

X = np.array(features)
y = np.array(valid_labels)

print("Feature length:", len(X[0]))

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = XGBClassifier(eval_metric='logloss')
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

joblib.dump(model, "model/model.pkl")

print(" Model trained!")