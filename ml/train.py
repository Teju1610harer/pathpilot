import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

df = pd.read_csv("data/students.csv")

df["class"] = df["class"].map({"10th": 0, "12th": 1})

X = df.drop(columns=["career"])
y = df["career"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

joblib.dump({
    "model": model,
    "features": list(X.columns)
}, "ml/model.pkl")

print("Model saved to ml/model.pkl")