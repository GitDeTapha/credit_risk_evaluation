import requests
# URL de base l'API 
url_base = 'http://127.0.0.1:8080/'

# Test du endpoint d'accueil
response = requests.get(f"{url_base}/")
print("\nRéponse du endpoint d'acceuil: \n", response.text)

# Données d'exemple pour la prédiction
input_data = {
    "Age": 30,
    "Sex": "male",
    "Job": 2,
    "Credit_amount": 1000,
    "Duration": 12,
    "Purpose": "radio/TV",
    "Housing": "own",
    "Saving_accounts": "little",
    "Checking_account": "moderate" 
}

response = requests.post(f"{url_base}/predict", json=input_data)
print("The prediction result is : ", response.json())


