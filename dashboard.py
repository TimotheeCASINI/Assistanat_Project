import streamlit as st
import pandas as pd
import numpy as np
import descripteur_lib

def change_dataframe(df_modele):
    new_df = None
    if st.session_state.op_descripteur != None:
        new_df = df_modele[df_modele['Descripteur'].isin([st.session_state.op_descripteur])]
    else:
        new_df = df_modele.copy(deep=True)
    return new_df

#Recupération bdd (A mettre en cache)
df_descripteur = descripteur_lib.recupDescripteur()
df_modele = descripteur_lib.recupModeles()
df_modele_user = df_modele.copy(deep=True)
df_gel = pd.read_csv("Data/gel/gel_data_instru.csv",sep=";")

#Creation variable global
list_settings_checkbox = ["Gel","Emulsion","G'","FminE","CoF30","JSM","Moyenne","jinf%","LOG10"]
list_descripteur = df_descripteur['Descripteur'].to_list()
list_settings_gel = df_gel.columns.to_list()[1:]
list_produits_gel = df_gel["Produit"].to_list()


#Debut Streamlit
st.title("Projet ODESSA")

#Analyse données instrumentales
st.header("Analyse des données intrumentales")

#Affichage input instru
ite=0
st.sidebar.header("Input data instru")
st.sidebar.subheader("simple bar chart")

option_parametre = st.sidebar.selectbox(#A implémenter
    'Quel caractérisation voulez vous ?',
    list_settings_gel,
    placeholder="Selectionner une caractérisation...",
    key="op_caractérisation_gel",
)

option_parametre = st.sidebar.multiselect(
    'Quel parametre voulez vous ?',
    list_settings_gel,
    placeholder="Selectionner un parametre...",
    key="op_settings_gel",
)

option_produit = st.sidebar.multiselect(
    'Quel(s) produit(s) voulez vous ?',
    list_produits_gel,
    placeholder="Selectionner un ou plusieurs produits...",
    key="op_produit_gel",
)

#affichage donnée
st.dataframe(df_gel)
if option_parametre==[]:
    option_parametre = list_settings_gel.copy()
if option_produit == []:
    st.bar_chart(df_gel, x="Produit", y=option_parametre)
else:
    st.bar_chart(df_gel[df_gel['Produit'].isin(option_produit)], x="Produit", y=option_parametre)




#Analyse modèle
st.header("Analyse des modèles")

#Affichage input
option_descripteur = st.selectbox(
    'Quel descripteur souhaitez vous ?',
    list_descripteur,
    index=None,
    placeholder="Selectionner un descripteur...",
    key="op_descripteur",
)
if option_descripteur == None:
    list_choose_user = list_descripteur[:]
else:
    list_choose_user = [option_descripteur]

a = st.columns(3)
ite=0
for i in list_settings_checkbox:
    with a[ite%3]:
        st.checkbox(i,key=i)
    ite = ite + 1

df_modele_user = change_dataframe(df_modele)

#Affichage modèle
st.text("Nombre de modèle correspondant "+str(df_modele_user.shape[0])+" :")
st.dataframe(df_modele_user,hide_index=True)

#Selection ligne
"""
selected_indices = st.multiselect('Select rows:', data.index)
selected_rows = data.loc[selected_indices]
st.write('### Selected Rows', selected_rows)
"""

#Affichage efficacité modèle sur borne (Non fonctionnel)
column_chart = []
for i in range (df_modele_user.shape[0]):
    column_chart.append("Equation "+str(i+1))

chart_data = pd.DataFrame(
    np.random.randn(10,df_modele_user.shape[0]),
    columns=column_chart,
)

st.line_chart(chart_data)