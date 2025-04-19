from flask import Flask, render_template, request
import math

app = Flask(__name__)

def calculate_emi(principal, years, rate=10.0):
    monthly_rate = rate / (12 * 100)
    months = years * 12
    emi = (principal * monthly_rate * pow(1 + monthly_rate, months)) / (pow(1 + monthly_rate, months) - 1)
    return round(emi, 2)

def suggest_strategies(data):
    strategies = []

    # Basic EMI
    emi = calculate_emi(data['loan_amount'], data['loan_duration'])

    if data['income'] < 300000:
        strategies.append("🔁 Income-Based Repayment: Keep your EMI flexible based on current income.")
        strategies.append("🎓 Apply for Central Sector Interest Subsidy (CSIS) Scheme if family income < ₹4.5 lakh.")
    if data['family_income'] < 250000 and data['academic_score'] > 75:
        strategies.append("💡 You're eligible for Dr. Ambedkar Interest Subsidy Scheme.")
    if data['preferred_payment'] and data['preferred_payment'] > emi:
        strategies.append(f"🚀 You can prepay your loan faster by paying ₹{data['preferred_payment']} instead of the regular EMI ₹{emi}.")

    if data['income'] > 500000:
        strategies.append("📈 Consider Fixed or Graduated EMI strategy for faster payoff.")

    strategies.append("🔍 Check Vidya Lakshmi Portal for personalized education loan subsidies and info.")
    strategies.append(f"🧮 Your estimated EMI is ₹{emi}/month for {data['loan_duration']} years.")

    return strategies

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'loan_amount': float(request.form['loan_amount']),
            'loan_duration': int(request.form['loan_duration']),
            'income': float(request.form['income']),
            'family_income': float(request.form['family_income']),
            'academic_score': float(request.form['academic_score']),
            'preferred_payment': float(request.form['preferred_payment']) if request.form['preferred_payment'] else None
        }
        strategy = suggest_strategies(data)
        return render_template('index.html', strategy=strategy, form_data=data)
    return render_template('index.html', strategy=None)

if __name__ == '__main__':
    app.run(debug=True)
