import re
import numpy as np
import pandas as pd
from sklearn.svm import LinearSVC
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
df = pd.read_csv("claim_classifier.csv")
def clean(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    return text
df["Claim"] = df["Claim"].apply(clean)
X = df["Claim"].values
y = df["label"].values
tfidf = TfidfVectorizer(max_features=5000,ngram_range=(1,2))
y_encoder = LabelEncoder()
X_encoded = tfidf.fit_transform(X)
y_encoded = y_encoder.fit_transform(y)
splitter = StratifiedShuffleSplit(n_splits=1,test_size=0.3)
for train_idx,test_idx in splitter.split(X,y):
    X_train, X_test = X_encoded[train_idx],X_encoded[test_idx]
    y_train, y_test = y_encoded[train_idx],y_encoded[test_idx]
reg = LinearSVC(C=1.0)
reg.fit(X_train,y_train)
print(reg.score(X_test,y_test))
while True:
    ui = input("You: ")
    ui = tfidf.transform([ui])
    print(f"Classification: {y_encoder.inverse_transform(reg.predict(ui))[0]}")