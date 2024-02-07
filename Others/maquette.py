import streamlit as st
import pandas as pd
import numpy as np
from library import descripteur_lib
import random


# Fonction pour calculer les inconnues en fonction de la valeur choisie par le client
def calculer_inconnues(nb_inconnue):
    inconnues = {}
    for x in range (0,nb_inconnue):
        nom = "Instrument"+str(x+1)
        inconnues.update({nom : random.uniform(0,10)})
    return inconnues


#Definition variable
list_descripteur = ['Fluide','Filant','Glissant','Coussin','Etalement','Doux','Collant','Gras','Penetrant','Pelucheux']

# Interface Streamlit
st.title("Projet ODESSA")


# Partie chercheurs
st.header("Partie chercheurs")
st.subheader("Analyse des descripteurs")

option_chercheurs = st.selectbox('Choix du descripteur',list_descripteur)

df = descripteur_lib.recupModeles(option_chercheurs)

# Visualisation des équations et de la plage efficace
st.write("Équations disponibles :")
st.dataframe(df,column_config={"Equation":"test"},hide_index=True)

column_chart = []
for i in range (df.shape[0]):
    column_chart.append("Equation "+str(i+1))

chart_data = pd.DataFrame(
    np.random.randn(10,df.shape[0]),
    columns=column_chart,
)

st.line_chart(chart_data)

st.subheader("Ajouter de nouvelles données")
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file, sep=';')
    st.dataframe(dataframe,hide_index=True)

st.divider()
# Partie client
st.header("Partie client")
st.write("Calcul des inconnues pour une valeur choisie par le client")

option_clients = st.selectbox('Choix du descripteur',list_descripteur, key=1)

valeur_client = st.slider("Choisir une valeur (entre 1 et 10)", 1, 10, 5)

nb_inconnue = 2
inconnues = calculer_inconnues(nb_inconnue)

equation, parametre = descripteur_lib.recupModele(option_clients, valeur_client)
st.write("Le modèle optimale pour le descripteur "+option_clients+" à la valeur "+str(valeur_client)+" requiert ces mesures : "+parametre)
st.write(equation)


st.write("Inconnues calculées pour la valeur choisie:")
st.write(inconnues)
