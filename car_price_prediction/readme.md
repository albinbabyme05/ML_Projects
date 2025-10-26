echo "# 🚗 Car Price Prediction Web App

This is a Flask-based web application that predicts the **selling price of a car** based on input features such as present price, kilometers driven, fuel type, seller type, transmission, owner count, and vehicle age.

It provides a modern, colorful UI with a car background, previous-results history, and model information display.

---

## 🧰 Features

- 🎨 **Modern gradient UI** with Bootstrap and custom CSS (`static/style.css`)
- 🧠 **ML model integration** using a pre-trained `joblib` model
- 📋 **Form-based input** with placeholders (no prefilled values)
- 🔁 **Reset Form** and **Clear History** buttons
- 📜 **Previous Results** table with colorful, tag-styled entries
- 🧾 **Model Used** tab showing only the model name
- 🖼️ **Car image background** for a stylish hero section

---



2️⃣ **Install dependencies**

pip install flask pandas joblib scikit-learn


---

## 🧠 How It Works

1. **User fills out form**
   - Inputs numeric & categorical features.
2. **Server converts form data**
   - Mapped into numeric format expected by the ML model.
3. **Prediction**
   - The trained model loaded via `joblib` generates a predicted selling price.
4. **Display**
   - The prediction appears immediately in the interface.
5. **History**
   - Previous predictions are saved in memory and shown in a colorful results table.

---

## 📦 API Endpoint (Optional)

A simple REST endpoint is also available for programmatic predictions:

**POST /predict**


---



## 📸 Screenshot 
<img width="1562" height="1065" alt="1" src="https://github.com/user-attachments/assets/33bedc59-3b9a-4ece-b6f5-54a1a1c23413" />

<img width="1607" height="1032" alt="2" src="https://github.com/user-attachments/assets/d113551b-f256-4a87-8d76-5f616290106e" />

---


## 📜 License
This project is for educational and demonstration purposes only.
" > README.md
