import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# load dataset
data = pd.read_csv("data/gesture_dataset.csv")

X = data.iloc[:, :-1]
y = data.iloc[:, -1]

model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

joblib.dump(model, "models/gesture_model.pkl")

print("Model trained and saved!")