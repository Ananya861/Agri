from flask import Flask, render_template, request
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

app = Flask(__name__)

# Load dataset
data = pd.read_csv("crop_prices.csv")

# Features and target
X = data[['Month', 'Rainfall', 'Temperature']]
y = data['Price']

# Train model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

@app.route('/', methods=['GET', 'POST'])
def home():

    prediction = None
    decision = None
    msp = None
    rainfall = None
    temperature = None

    if request.method == 'POST':

        month = int(request.form['month'])

        # Validation
        if month < 1 or month > 12:

            prediction = "Invalid Month"
            decision = "Please enter month between 1 and 12"

        else:

            # Get rainfall and temperature from dataset
            row = data[data['Month'] == month]

            rainfall = int(row['Rainfall'].values[0])
            temperature = int(row['Temperature'].values[0])

            # Prediction input
            future_data = [[month, rainfall, temperature]]

            predicted_price = model.predict(future_data)

            prediction = round(predicted_price[0], 2)

            # Get MSP
            msp = int(row['MSP'].values[0])

            # Decision support
            if prediction > msp:
                decision = "Wait and Sell Later"
            else:
                decision = "Sell Now"

    return render_template(
        'index.html',
        prediction=prediction,
        decision=decision,
        msp=msp,
        rainfall=rainfall,
        temperature=temperature
    )

if __name__ == '__main__':
    app.run(debug=True)