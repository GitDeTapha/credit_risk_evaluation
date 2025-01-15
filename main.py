from flask import Flask, render_template, request
import numpy as np
from pydantic import BaseModel
import pandas as pd
import joblib
import sklearn.preprocessing as preprocessing


model = joblib.load('./models/rf_model_0_1.pkl')
#print("Feature names used during training:", model.feature_names_in_)

app = Flask(__name__)
class InputData(BaseModel):
    Age: int
    Sex: str
    Job: int
    Housing: str
    Saving_accounts: str
    Checking_account: str
    Credit_amount: int
    Duration: int
    Purpose: str

def preprocess_input(data: InputData):
    try:
        df = pd.DataFrame([data.dict()])
        
        df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})
        df['Purpose'] = df['Purpose'].map({
            'car': 0,
            'radio/TV': 1,
            'furniture/equipment': 2,
            'business': 3,
            'education': 4,
            'repairs': 5,
            'domestic appliances': 6,
            'vacation/others': 7
        })

        df.rename(columns={
            'Saving_accounts': 'Saving accounts',
            'Checking_account': 'Checking account',
            'Credit_amount': 'Credit amount'
        }, inplace=True)

        df = pd.get_dummies(df, columns=[
            'Housing', 'Saving accounts', 'Checking account', 'Purpose'
        ], drop_first=True)

        for col in model.feature_names_in_:
            if col not in df.columns:
                df[col] = 0  # Remplir avec des zéros pour les colonnes manquantes

        df = df[model.feature_names_in_]
        return df
    except Exception as e:
        raise ValueError(f"Erreur dans le prétraitement des données : {e}")


@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        input_data = InputData(**request.form)
        processed_data = preprocess_input(input_data)
        prediction = model.predict(processed_data)
        result = prediction[0]

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True, port=8080)

