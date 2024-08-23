from flask import Flask, request, render_template
import numpy as np
import joblib
import os

app = Flask(__name__, template_folder="Template")
app.secret_key = os.getenv('SECRET_KEY', 'BBCMASTER03')

# DEPLOY MODEL
model = joblib.load("Tesla_Stock_Model")

# BUILD APP
@app.route("/", methods=["GET", "POST"])
def Main():
    if request.method == "POST":
        try:
            Open = float(request.form.get("Open"))
            High = float(request.form.get("High"))
            Low = float(request.form.get("Low"))
            input_data = np.array([[Open, High, Low]])
            rounded_data = np.round(input_data, 2)
            not_rounded_data = input_data != rounded_data
            if np.any(not_rounded_data):
                prediction = model.predict(rounded_data)
                result = f"Predicted Closing Price: {prediction[0]:.2f}"
            else:
                prediction = model.predict(input_data)
                result = f"Predicted Closing Price: {prediction[0]:.2f}"
        except (ValueError, TypeError):
            result = "Invalid input. Please enter valid numbers."
    else:
        result = None
        
    return render_template("Main.html", result=result)   
    
if __name__ == "__main__":
    app.run(debug=True)
    
# NOTE TO SELF: FIX THE SPLASH SCREEN. MAKE IT TO WHERE THE SPLASH SCREEN ISNT SHOWING EVRY TIME YOU CLICK "Get Prediction".
# UPLOAD THIS TO YOUR GIT HUB REPOSITORY TOMMOROW. THE WEB APP IS BUILT IOT JUST NEEEDS TO BE PUBLISHED. SO GOODJOB.