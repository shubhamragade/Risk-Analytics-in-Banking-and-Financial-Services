from flask import Flask, render_template, request
import numpy as np
import joblib

app = Flask(__name__)
model = joblib.load('model/loan_model.pkl')  # Your trained model path

# Mapping functions
def encode_occupation(value):
    return {
        "I": [1, 0, 0, 0],
        "II": [0, 1, 0, 0],
        "III": [0, 0, 1, 0],
        "IV": [0, 0, 0, 1]
    }.get(value, [0, 0, 0, 0])

def encode_fee(value):
    return {
        "Low": [1, 0],
        "Mid": [0, 1]
    }.get(value, [0, 0])

def encode_loyalty(value):
    return {
        "Jade": [1, 0, 0],
        "Platinum": [0, 1, 0],
        "Silver": [0, 0, 1]
    }.get(value, [0, 0, 0])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Numeric features from form
        age = float(request.form['Age'])
        location_id = float(request.form['Location ID'])
        income = float(request.form['Estimated Income'])
        super_savings = float(request.form['Superannuation Savings'])
        credit_cards = float(request.form['Amount of Credit Cards'])
        cc_balance = float(request.form['Credit Card Balance'])
        bank_loans = float(request.form['Bank Loans'])
        bank_deposits = float(request.form['Bank Deposits'])
        checking_acc = float(request.form['Checking Accounts'])
        saving_acc = float(request.form['Saving Accounts'])

        # Encoded features
        occupation = encode_occupation(request.form['Occupation'])
        fee = encode_fee(request.form['Fee Structure'])
        loyalty = encode_loyalty(request.form['Loyalty'])

        # Final feature array
        final_features = [age, location_id, income, super_savings, credit_cards,
                          cc_balance, bank_loans, bank_deposits, checking_acc, saving_acc] + \
                         occupation + fee + loyalty

        prediction = model.predict([final_features])[0]
        result = "🔴 Not Pay (Default)" if prediction == 1 else "🟢 Pay (Good)"
        return render_template('index.html', prediction_text=result)

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
