CAMPUS PLACEMENT PREDICTION
===========================

A web-based machine learning application built with Flask that predicts 
whether a student is likely to be placed or not placed based on academic 
and personal details.

------------------------------------------------------------
PROJECT STRUCTURE
------------------------------------------------------------
app.py                  - Flask web application
static/style.css        - CSS for the frontend design
templates/index.html     - HTML form for user input
Campus_placement_predcition.ipynb - Model training notebook
models/                  - Folder containing trained joblib models

------------------------------------------------------------
FEATURES
------------------------------------------------------------
- Web interface built using Flask
- Supports multiple ML models (Logistic Regression, SVM, Decision Tree, 
  KNN, Random Forest, Gradient Boost)
- Displays prediction result ("Placed" or "Not Placed")
- Shows model accuracy and stores prediction history
- Clean modern UI using CSS

------------------------------------------------------------
REQUIREMENTS
------------------------------------------------------------
Python 3.9+
Flask
pandas
joblib
scikit-learn

------------------------------------------------------------
USAGE
------------------------------------------------------------
1. Clone or download this repository.
2. Ensure all model files are inside the MODELS_DIR path defined in app.py.
3. Install dependencies:
      pip install flask pandas joblib scikit-learn
4. Run the Flask app:
      python app.py
5. Open your browser and go to:
      http://127.0.0.1:5000/

------------------------------------------------------------


------------------------------------------------------------
OUTPUT
------------------------------------------------------------
<img width="1643" height="1066" alt="placement_predcition" src="https://github.com/user-attachments/assets/744aab04-e03e-4a73-a4fe-f350dbbb1c42" />
<img width="1855" height="1047" alt="2" src="https://github.com/user-attachments/assets/63e58e29-199c-4ec4-b760-daee542caba7" />


------------------------------------------------------------
AUTHOR
------------------------------------------------------------
Developed by Albin Baby
