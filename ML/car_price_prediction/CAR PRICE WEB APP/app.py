from flask import Flask, request, render_template, jsonify, redirect, url_for
import pandas as pd
import joblib
import os
from collections import deque
from datetime import datetime

app = Flask(__name__, template_folder="templates", static_folder="static")

# Model path 
MODEL_PATH = r"D:\Work_Directory\ML\car_price_prediction\car_price_prediction_gbModel"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")

# Load trained model
model = joblib.load(MODEL_PATH)


def get_model_display_name(m):
    try:
        # scikit-learn Pipeline style
        from sklearn.pipeline import Pipeline
        if isinstance(m, Pipeline):
            final_est = m.steps[-1][1]
            return type(final_est).__name__
    except Exception:
        pass
    return type(m).__name__

MODEL_DISPLAY_NAME = get_model_display_name(model)

# -Mappings 
FUEL_MAP = {'Petrol': 0, 'Diesel': 1, 'CNG': 2}
SELLER_MAP = {'Dealer': 0, 'Individual': 1}
TRANSMISSION_MAP = {'Manual': 0, 'Automatic': 1}

#  Store previous predictions 
PREV_RESULTS = deque(maxlen=20)  # increased for more history

def build_dataframe(form_dict):
    """Convert form input to model-ready DataFrame."""
    
    def to_float(v, default=0.0):
        try:
            return float(v)
        except Exception:
            return default

    def to_int(v, default=0):
        try:
            return int(float(v))
        except Exception:
            return default

    present_price = to_float(form_dict.get("Present_Price", ""))
    kms_driven    = to_int(form_dict.get("Kms_Driven", ""))
    owner         = to_int(form_dict.get("Owner", ""))
    age           = to_int(form_dict.get("Age", ""))

    fuel_label         = (form_dict.get("Fuel_Type") or "").strip() or "Petrol"
    seller_label       = (form_dict.get("Seller_Type") or "").strip() or "Dealer"
    transmission_label = (form_dict.get("Transmission") or "").strip() or "Manual"

    df = pd.DataFrame({
        "Present_Price": [present_price],
        "Kms_Driven": [kms_driven],
        "Fuel_Type": [FUEL_MAP.get(fuel_label, 0)],
        "Seller_Type": [SELLER_MAP.get(seller_label, 0)],
        "Transmission": [TRANSMISSION_MAP.get(transmission_label, 0)],
        "Owner": [owner],
        "Age": [age],
    })
    return df

@app.route("/", methods=["GET", "POST"])
def index():
    #  placeholders only
    form_empty = {
        "Present_Price": "",
        "Kms_Driven": "",
        "Fuel_Type": "",
        "Seller_Type": "",
        "Transmission": "",
        "Owner": "",
        "Age": "",
    }

    prediction = None
    form_values = form_empty.copy()

    if request.method == "POST":
        # Collect submitted values 
        form_values = {k: request.form.get(k, "").strip() for k in form_empty.keys()}

        # Only predict if required numeric fields are provided
        required_fields = ["Present_Price", "Kms_Driven", "Owner", "Age",
                           "Fuel_Type", "Seller_Type", "Transmission"]
        if all(form_values.get(f) for f in required_fields):
            df = build_dataframe(form_values)
            try:
                y_pred = model.predict(df)[0]
                prediction = round(float(y_pred), 4)
            except Exception as e:
                prediction = f"Prediction error: {e}"

            # Save latest result in memory
            PREV_RESULTS.appendleft({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "inputs": form_values.copy(),
                "prediction": prediction
            })
       

    return render_template(
        "index.html",
        form=form_values,
        prediction=prediction,
        fuel_options=list(FUEL_MAP.keys()),
        seller_options=list(SELLER_MAP.keys()),
        transmission_options=list(TRANSMISSION_MAP.keys()),
        model_name=MODEL_DISPLAY_NAME,
        prev_results=list(PREV_RESULTS)
    )

@app.route("/clear_history", methods=["POST"])
def clear_history():
    PREV_RESULTS.clear()
    return redirect(url_for("index"))

#  JSON endpoint 
@app.route("/predict", methods=["POST"])
def predict_api():
    payload = request.get_json(force=True)
    df = build_dataframe(payload)
    y_pred = model.predict(df)[0]
    return jsonify({"prediction": float(y_pred)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
