# app.py
from flask import Flask, render_template, request, redirect, url_for, session
import os, json, time
import joblib
import pandas as pd

app = Flask(__name__)
app.secret_key = "replace_this_with_a_strong_secret"

MODELS_DIR = r"D:\Work_Directory\ML\ML\Campus placement predcition"

MODEL_FILE_MAP = {
    "LogisticRegression": "restaurent_sentimental_analysis_LogisticRegression",
    "svm": "restaurent_sentimental_analysis_svm",
    "DecisionTreeClassifier": "restaurent_sentimental_analysis_DecisionTreeClassifier",
    "KNeighborsClassifier": "restaurent_sentimental_analysis_KNeighborsClassifier",
    "RandomForestClassifier": "restaurent_sentimental_analysis_RandomForestClassifier",
    "Gradient Boost": "restaurent_sentimental_analysis_Gradient Boost",
}

PROVIDED_ACCURACIES = {
    "LogisticRegression": 88.37,
    "svm": 76.74,
    "DecisionTreeClassifier": 83.72,
    "KNeighborsClassifier": 79.07,
    "RandomForestClassifier": 81.40,
    "Gradient Boost": 81.40,
}

FEATURE_ORDER = [
    'gender', 'ssc_p', 'ssc_b', 'hsc_p', 'hsc_b', 'hsc_s',
    'degree_p', 'degree_t', 'workex', 'etest_p', 'specialisation', 'mba_p'
]

LOADED_MODELS = {}
MODEL_PATHS   = {}
MODEL_SCORES  = {}

def discover_models():
    MODEL_PATHS.clear()
    missing = []
    for display_name, filename in MODEL_FILE_MAP.items():
        full = os.path.join(MODELS_DIR, filename)
        if os.path.exists(full):
            MODEL_PATHS[display_name] = full
        else:
            missing.append((display_name, full))
    if missing:
        print("\n models were not found on disk:")
        for name, path in missing:
            print(f"  - {name}: {path}")

def load_accuracies():
    MODEL_SCORES.clear()
    for name in MODEL_PATHS:
        if name in PROVIDED_ACCURACIES:
            MODEL_SCORES[name] = round(float(PROVIDED_ACCURACIES[name]), 2)

def parse_form_to_features(form):
    def to_float(k):
        v = form.get(k, '')
        try: return float(v)
        except: return 0.0
    def to_int(k):
        v = form.get(k, '')
        try: return int(float(v))
        except: return 0
    int_fields = {'gender','ssc_b','hsc_b','hsc_s','degree_t','workex','specialisation'}
    row = []
    for f in FEATURE_ORDER:
        row.append(to_int(f) if f in int_fields else to_float(f))
    return pd.DataFrame([row], columns=FEATURE_ORDER)

def ensure_history():
    if 'history' not in session:
        session['history'] = []

def ensure_models_loaded():
    if not MODEL_PATHS:
        discover_models()
        load_accuracies()

@app.route("/", methods=["GET"])
def home():
    ensure_models_loaded()
    ensure_history()
    if not MODEL_PATHS:
        return "<h2>No models found.</h2><p>Check MODELS_DIR or MODEL_FILE_MAP in app.py.</p>"
    selected = max(MODEL_SCORES, key=MODEL_SCORES.get) if MODEL_SCORES else list(MODEL_PATHS.keys())[0]
    return render_template(
        "index.html",
        feature_order=FEATURE_ORDER,
        model_names=list(MODEL_PATHS.keys()),
        model_scores=MODEL_SCORES,
        selected_model=selected,
        history=session['history'],
        json_model_scores=json.dumps(MODEL_SCORES)
    )

@app.route("/predict", methods=["POST"])
def predict():
    ensure_models_loaded()
    ensure_history()
    selected_model = request.form.get("model_name")
    if not selected_model or selected_model not in MODEL_PATHS:
        return redirect(url_for("home"))
    if selected_model not in LOADED_MODELS:
        LOADED_MODELS[selected_model] = joblib.load(MODEL_PATHS[selected_model])
    model = LOADED_MODELS[selected_model]
    X_new = parse_form_to_features(request.form)
    pred = int(model.predict(X_new)[0])
    proba = None
    if hasattr(model, "predict_proba"):
        try:
            proba = float(model.predict_proba(X_new)[0][1])
        except Exception:
            proba = None
    record = {
        "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
        "model": selected_model,
        "prediction": "Placed" if pred == 1 else "Not Placed",
        "confidence": (round(proba * 100, 2) if proba is not None else None),
        "inputs": {k: request.form.get(k, "") for k in FEATURE_ORDER}
    }
    session['history'] = [record] + session.get('history', [])
    session.modified = True
    return redirect(url_for("home"))

@app.route("/reset_form", methods=["POST"])
def reset_form():
    return redirect(url_for("home"))

@app.route("/reset_history", methods=["POST"])
def reset_history():
    session['history'] = []
    session.modified = True
    return redirect(url_for("home"))

if __name__ == "__main__":
    discover_models()
    load_accuracies()
    app.run(host="0.0.0.0", port=5000, debug=True)
