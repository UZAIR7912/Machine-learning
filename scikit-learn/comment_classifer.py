import re
import pandas as pd
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
df = pd.read_csv("comment_classifier.csv")
df = df.drop(["CommentId","VideoId","IsSexist"],axis=1)
def clean(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z!?'.\s]", "", text)
    return text
df["Text"] = df["Text"].apply(clean)
X = df["Text"].values
y = df[['IsToxic', 'IsAbusive', 'IsThreat', 'IsProvocative',
        'IsObscene', 'IsHatespeech', 'IsRacist', 'IsNationalist',
        'IsHomophobic', 'IsReligiousHate', 'IsRadicalism']].values

X_encoder = TfidfVectorizer(max_features=100000, ngram_range=(1,2))
X_encoded = X_encoder.fit_transform(X)
X_train,x_test,y_train,y_test = train_test_split(X_encoded,y,test_size=0.2)
model = OneVsRestClassifier(LinearSVC())
model.fit(X_train,y_train)
print(model.score(x_test,y_test))
labels = ["Toxic","Abusive","Threat","Provocative",
    "Obscene","Hate Speech","Racist","Nationalist",
    "Homophobic","Religious Hate","Radicalism"]

while True:
    ui = input("You: ")
    cleaned = clean(ui)
    ui_vec = X_encoder.transform([cleaned])
    prediction = model.predict(ui_vec)[0]
    detected = [labels[i] for i, val in enumerate(prediction) if val == 1]
    if detected:
        print("Model: This comment is classified as →", ", ".join(detected))
    else:
        print("Model: This comment seems clean / non-toxic")