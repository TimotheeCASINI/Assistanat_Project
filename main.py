import streamlit as st
import descripteur_lib as des
import sympy as sp

st.title('ODESSA')

#Choix du descripteur souhaité par le client
list_descripteur = ['Fluide','Filant','Glissant','Coussin','Etalement','Doux','Collant','Gras','Penetrant','Pelucheux']
option = st.selectbox('Choix du descripteur',list_descripteur)


#Affichage description descripteur
st.write(des.présentation(option))

#Selection de la valeur souhaité du descripteur
valeur = st.slider("Quel valeur souhaitez-vous pour votre produit pour le descripteur "+option+" ?",0,10)

#Recupere les modèles voulus
equation,parametre = des.recupModele(option,valeur)
st.write("Le modèle optimale pour le descripteur "+option+" à la valeur "+str(valeur)+" requiert ces mesures : "+parametre)
st.write(equation)

#Faire le calcul avec la valeur
"""
Il faut pouvoir prendre plusieurs inconnues
"""
x = sp.symbols('x')
equation_sympy = sp.sympify(equation)
solutions = sp.solve(equation_sympy,x)
st.write("Il vous faut des mesures de "+parametre+" égal à: "+str(solutions)+"")


