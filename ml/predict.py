import joblib

_bundle = joblib.load("ml/model.pkl")
_model = _bundle["model"]
_feature_order = _bundle["features"]

def predict_careers(features_dict, top_n=5):
    """
    features_dict: output of compute_features() from features.py
    Returns a list of (career_name, confidence_percent), sorted highest first.
    """
    row = dict(features_dict)
    row["class"] = 0 if row.get("class") == "10th" else 1
    row.pop("priority", None)

    ordered_values = [[row.get(f, 0) for f in _feature_order]]

    proba = _model.predict_proba(ordered_values)[0]
    classes = _model.classes_

    ranked = sorted(zip(classes, proba), key=lambda x: -x[1])[:top_n]
    return [(career, round(score * 100, 1)) for career, score in ranked]