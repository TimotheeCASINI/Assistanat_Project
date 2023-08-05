import streamlit as st
import descripteur_lib as des

st.title('ODESSA')

#Choix du descripteur souhaité par le client
list_descripteur = ['Fluide','Filant','Glissant','Coussin','Etalement','Doux','Collant','Gras','Penetrant','Pelucheux']
option = st.selectbox('Choix du descripteur',list_descripteur)

st.write(des.présentation(option))


