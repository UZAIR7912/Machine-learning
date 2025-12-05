import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("expanded_output.csv")
encoder_word = OrdinalEncoder()
encoder_label = OrdinalEncoder()
df["Word_encoded"] = encoder_word.fit_transform(df[["Word"]])
df["Label_encoded"] = encoder_label.fit_transform(df[["Label"]])
X = np.array(df[["Word_encoded"]].values)
y = np.array(df["Label_encoded"])
split = StratifiedShuffleSplit(n_splits=1,test_size=0.2)
for train_idx,test_idx in split.split(X,y):
    X_train , X_test = X[train_idx],X[test_idx]
    y_train , y_test = y[train_idx],y[test_idx]
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
classifier = RandomForestClassifier()
classifier.fit(X_train_scaled,y_train)
print(classifier.score(X_test_scaled,y_test))
while True:
    ui = input("Enter a word: ")
    temp_df = pd.DataFrame([[ui]], columns=["Word"])
    try:
        temp_encoded = encoder_word.transform(temp_df)
    except ValueError:
        temp_encoded = encoder_word.fit_transform(pd.concat([df[["Word"]], temp_df], ignore_index=True))[-1:]
    temp_scaled = scaler.transform(temp_encoded)
    
    # Predict
    pred_encoded = classifier.predict(temp_scaled)
    pred_label = encoder_label.inverse_transform(pred_encoded.reshape(-1,1))[0][0]
    if pred_label == 0:
        print(f"Prediction: Incorrect Spellings")
    elif pred_label == 1:
        print(f"Prediction: Correct Spellings")