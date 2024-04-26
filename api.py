import requests
import streamlit as st

def fetch_tutors():
    try:
        response = requests.get("https://mongo-backend-production.up.railway.app/sheets")
        response.raise_for_status()  
        return response.json()
    except requests.RequestException as e:
        st.error(f"Ocurrion un error trayendo los tutores: {e}")
        return [] 

def fetch_tutor_username(email):
    try:
        response = requests.get(f"https://mongo-backend-production.up.railway.app/users/search?email={email}")
        response.raise_for_status()  
        tutor = response.json()
        return tutor["username"]
    except requests.RequestException as e:
        st.error(f"Ocurrio un error trayendo el nombre de usuario del tutor: {e}")
        return "ERROR"
    
def send_api_key(api_key):
    url = "https://mongo-backend-production.up.railway.app/apikey"
    headers = {"Content-Type": "application/json"}
    payload = {"apiKey": api_key}

    # Make a POST request to the server
    response = requests.post(url, json=payload, headers=headers)
    return response.json()