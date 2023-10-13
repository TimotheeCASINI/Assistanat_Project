import streamlit as st
import pandas as pd
import numpy as np
import descripteur_lib

#Creation variable global
list_settings_checkbox = ["Gel","Emulsion","G'","FminE","CoF30","JSM","Moyenne","jinf%","LOG10"]

#Recupération bdd (A mettre en cache)
df_descripteur = descripteur_lib.recupDescripteur()
list_descripteur = df_descripteur['Descripteur'].to_list()

df_modele = descripteur_lib.recupModeles()


#Debut Streamlit
st.title("Projet ODESSA")
st.header("Analyse des descripteurs")


#Affichage input
option_descripteur = st.selectbox(
    'Quel descripteur souhaitez vous ?',
    list_descripteur,
    index=None,
    placeholder="Selectionner un descripteur..."
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

#Affichage modèle
st.text("Nombre de modèle correspondant "+str(df_modele[df_modele['Descripteur'].isin(list_choose_user)].shape[0])+" :")
st.dataframe(df_modele[df_modele['Descripteur'].isin(list_choose_user)],hide_index=True)



#Affichage efficacité modèle sur borne (Non fonctionnel)
column_chart = []
for i in range (df_modele[df_modele['Descripteur'].isin(list_choose_user)].shape[0]):
    column_chart.append("Equation "+str(i+1))

chart_data = pd.DataFrame(
    np.random.randn(10,df_modele[df_modele['Descripteur'].isin(list_choose_user)].shape[0]),
    columns=column_chart,
)

st.line_chart(chart_data)

