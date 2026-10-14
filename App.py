import streamlit as st
import json
import os
from google import genai

# Configuration de la page de l'application
st.set_page_title("JARVIS — Assistant Personnel")
st.title("🤖 JARVIS — Assistant")

# Gestion de la mémoire (les souvenirs)
FICHIER_MEMOIRE = "memoire.json"

def charger_memoire():
    if os.path.exists(FICHIER_MEMOIRE):
        with open(FICHIER_MEMOIRE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"souvenirs": ["Mon créateur construit son assistant personnel JARVIS."]}

memoire = charger_memoire()

# Récupération sécurisée de la clé API Gemini
# (On la configurera juste après dans les secrets de l'application)
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    client = genai.Client(api_key=api_key)
    
    # Initialisation de la discussion avec Gemini Flash
    if "chat" not in st.session_state:
        st.session_state.chat = client.chats.create(model="gemini-3.5-flash-lite")
    
    # Affichage d'un message d'accueil
    st.write("Je t'écoute, chef ! 🫡")

    # Zone de texte pour parler à JARVIS
    user_input = st.chat_input("Écris ou dis ta commande à JARVIS...")
    
    if user_input:
        # Afficher ce que tu as écrit
        with st.chat_message("user"):
            st.write(user_input)
            
        # Gérer les souvenirs si tu lui demandes de mémoriser quelque chose
        if user_input.lower().startswith("mémorise que "):
            souvenir = user_input[len("mémorise que "):].strip()
            memoire["souvenirs"].append(souvenir)
            with open(FICHIER_MEMOIRE, "w", encoding="utf-8") as f:
                json.dump(memoire, f, ensure_ascii=False, indent=2)
            reponse_texte = f"C'est noté chef, souvenir enregistré : {souvenir}"
        elif user_input.lower() == "souvenirs":
            reponse_texte = "Voici vos souvenirs : " + "; ".join(memoire["souvenirs"])
        else:
            # Envoyer le message à Gemini avec le contexte des souvenirs
            contexte = f"Souvenirs enregistrés : {json.dumps(memoire['souvenirs'], ensure_ascii=False)}"
            reponse = st.session_state.chat.send_message(contexte + f"\nChef : {user_input}")
            reponse_texte = reponse.text
            
        # Afficher la réponse de JARVIS
        with st.chat_message("assistant"):
            st.write(reponse_texte)
else:
    st.error("⚠️ Clé API Gemini manquante. Configure ta clé dans les paramètres de l'application.")
