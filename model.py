import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression , LinearRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, mean_squared_error, classification_report
import joblib

# Data Loading function
def load_data(filepath: str):
    """Load and Clean the Dataset"""
    df=pd.read_csv(filepath)
    df = df.dropna(subset=["doctor_note","risk_label","risk_score"])
    return df

# Model Training Function
def train_models(df: pd.DataFrame):
    """ Train the Classification and Regression models from datasets."""

    # split for classifcation
    X_train_c, X_test_c, y_train_c,y_test_c = train_test_split(df["doctor_note"],df["risk_label"],test_size=0.2, random_state=42)

    # split for regression
    X_train_r, X_test_r, y_train_r ,y_test_r = train_test_split(df["doctor_note"],df["risk_score"], test_size=0.2, random_state=42)
    
    # TF-IDF Vectorization (converts text to numerical features)
    vectorizer = TfidfVectorizer(max_features=5000 ,stop_words='english')
    X_train_c_vec = vectorizer.fit_transform(X_train_c)
    X_test_c_vec = vectorizer.transform(X_test_c)

    X_train_r_vec = vectorizer.fit_transform(X_train_r)
    X_test_r_vec = vectorizer.transform(X_test_r)

    # Classification Model
    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train_c_vec, y_train_c)
    y_pred_c = clf.predict(X_test_c_vec)
    clf_report = classification_report(y_test_c, y_pred_c)
    print("Classification Model Trained.")
    print("Classification Report:\n", clf_report)
    print("Classification Accuracy:", accuracy_score(y_test_c, y_pred_c))

    # Regression Model
    reg = LinearRegression()
    reg.fit(X_train_r_vec, y_train_r)
    y_pred_r = reg.predict(X_test_r_vec)
    mse = mean_squared_error(y_test_r,y_pred_r)
    rmse = np.sqrt(mse)
    print("Regression Model Trained.")
    print("Regression RMSE:", rmse)
    print("Regression Mean Squared Error:", mse)

    return vectorizer, clf, reg

# Model Saving and Loading functions
def save_models(vectorizer, clf, reg):
    """ So this function will save the trained models in Pkl format and 
    can be loaded later for inference which will help in faster predictions.
    it stores all the vectors and models in the disk."""
    joblib.dump(vectorizer, 'vectorizer.pkl')
    joblib.dump(clf, 'classification_model.pkl')
    joblib.dump(reg, 'regression_model.pkl')

    print("Models saved to disk.")

def load_models():
    """ This function will load the trained models from the pkl files or disk and return them."""
    vectorizer = joblib.load('vectorizer.pkl')
    clf = joblib.load('classification_model.pkl')
    reg = joblib.load('regression_model.pkl')
    
    return vectorizer, clf, reg

# Prediciton Function 

def predict_health_risk(note: str, vectorizer, clf, reg):
    """ Predict Both risk label and risk score for a new note."""
    note_vec = vectorizer.transform([note])
    risk_label = clf.predict(note_vec)[0]
    risk_score = reg.predict(note_vec)[0]
    score_pred = np.clip(risk_score, 0, 100)  # Ensure score is between 0 and 100%

    return risk_label, round(score_pred, 2)

# =========================================================
#  5. Run Training or Prediction (Optional Main Block)
# =========================================================
if __name__ == "__main__":
    # Load data
    df = load_data("doctor_notes.csv")

    # Train models
    vectorizer, clf_model, reg_model = train_models(df)

    # Save models
    save_models(vectorizer, clf_model, reg_model)

    # Example prediction
    example_note = "Patient have high fever and shortness of breath."
    label, score = predict_health_risk(example_note, vectorizer, clf_model, reg_model)
    print(f"\n Example Note: {example_note}")
    print(f"Predicted Risk Label: {label}")
    print(f"Predicted Risk Score: {score}%")