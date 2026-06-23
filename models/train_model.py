import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

data = pd.read_csv("gesture_dataset.csv", header=None)

X = data.iloc[:, 1:]
y = data.iloc[:, 0]

model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

joblib.dump(model, "models/gesture_model.pkl")

print("Model trained and saved!")