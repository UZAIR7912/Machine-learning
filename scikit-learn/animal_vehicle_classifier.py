import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
# Data
import random

# Base unique items
vehicles = [
    "bus","train","car","motorcycle","airplane","helicopter","boat","bicycle",
    "truck","van","scooter","ship","tram","submarine","jeep","taxi",
    "ferry","rocket","minibus","hovercraft","skateboard","rollerblades",
    "bulldozer","forklift","ambulance","firetruck","policecar","tractor",
    "golfcart","segway"
]

animals = [
    "dog","cat","lion","tiger","elephant","horse","sheep","goat","wolf","bear",
    "monkey","giraffe","zebra","kangaroo","panda","fox","rabbit","mouse",
    "cow","buffalo","camel","donkey","leopard","cheetah","hippo","rhino",
    "squirrel","bat","owl","eagle"
]

# Expand to ~1000 items by random sampling with replacement
expanded_data = {}

while len(expanded_data) < 1000:
    # Randomly pick a vehicle or animal
    if random.random() < 0.5:
        item = random.choice(vehicles)
        expanded_data[f"{item}_{len(expanded_data)}"] = "vehicle"
    else:
        item = random.choice(animals)
        expanded_data[f"{item}_{len(expanded_data)}"] = "animal"
df = pd.DataFrame(list(expanded_data.items()), columns=["Name", "Type"])

# Encode Name (X)
name_encoder = OrdinalEncoder()
df["Name_encoded"] = name_encoder.fit_transform(df[["Name"]])

# Encode Type (y)
type_encoder = OrdinalEncoder(categories=[["vehicle", "animal"]])
df["Type_encoded"] = type_encoder.fit_transform(df[["Type"]])

# X and y as arrays
X = df[["Name_encoded"]].values
y = df["Type_encoded"].values

# Train/test split
split = StratifiedShuffleSplit(n_splits=1, test_size=0.2)
for train_idx, test_idx in split.split(X, y): #type:ignore
    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]

# Scale (only after split)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
clasiffier = RandomForestClassifier()
clasiffier.fit(X_train_scaled,y_train)
print(clasiffier.score(X_test_scaled,y_test))
while True:
    user_input = input("Enter a name (or type 'exit' to quit): ").strip()
    if user_input.lower() == "exit":
        break
    
    # Encode the input like training data
    # Add a temporary dataframe for consistent encoding
    temp_df = pd.DataFrame([[user_input]], columns=["Name"])
    try:
        temp_encoded = name_encoder.transform(temp_df)
    except ValueError:
        # If new/unseen name, add it temporarily to fit_transform
        temp_encoded = name_encoder.fit_transform(pd.concat([df[["Name"]], temp_df], ignore_index=True))[-1:]
    
    # Scale
    temp_scaled = scaler.transform(temp_encoded)
    
    # Predict
    pred_encoded = clasiffier.predict(temp_scaled)
    pred_label = type_encoder.inverse_transform(pred_encoded.reshape(-1,1))[0][0]
    
    print(f"Prediction: {pred_label}")