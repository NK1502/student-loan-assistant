import os
import pickle
import pandas as pd
from flask import Flask, render_template, request
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Load the ML model
model_path = os.path.join('model', 'loan_strategy_model.pkl')
with open(model_path, 'rb') as model_file:
    model = pickle.load(model_file)

# Standard Scaler for input normalization
scaler = StandardScaler()

# Route for home page
@app.route("/", methods=["GET", "POST"])
def home():
    strategy = None
    if request.method == "POST":
        # Get user inputs
        loan_amount = float(request.form['loan_amount'])
        loan_duration = float(request.form['loan_duration'])
        income = float(request.form['income'])
        expenses = float(request.form['expenses'])
        
        # Create input dataframe
        user_data = pd.DataFrame([[loan_amount, loan_duration, income, expenses]], columns=['loan_amount', 'loan_duration', 'income', 'expenses'])
        
        # Scale the input data (important for most ML models)
        user_data_scaled = scaler.fit_transform(user_data)
        
        # Get prediction from the model
        prediction = model.predict(user_data_scaled)
        
        # Return repayment strategy based on prediction
        strategy = get_strategy(prediction)
    
    return render_template("index.html", strategy=strategy)

def get_strategy(prediction):
    # Example of different repayment strategies (use your actual model predictions here)
    if prediction == 0:
        return "Strategy 1: Choose the 'Income-based Repayment Plan' based on your financial situation."
    elif prediction == 1:
        return "Strategy 2: Opt for 'Standard Repayment Plan' to pay off the loan in fixed payments."
    elif prediction == 2:
        return "Strategy 3: Consider 'Graduated Repayment Plan' with lower initial payments that increase over time."
    else:
        return "Strategy 4: Explore 'Extended Repayment Plan' if you need a longer term to repay."

if __name__ == "__main__":
    app.run(debug=True)
