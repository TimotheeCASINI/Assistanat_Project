import streamlit as st
import descripteur_lib as des
import sympy as sp
from math import log10

st.title('ODESSA')

#Choix du descripteur souhaité par le client
list_descripteur = ['Fluide','Filant','Glissant','Coussin','Etalement','Doux','Collant','Gras','Penetrant','Pelucheux']
option = st.selectbox('Choix du descripteur',list_descripteur)


#Affichage description descripteur
st.write(des.présentation(option))

#Selection de la valeur souhaité du descripteur
valeur = st.slider("Quel valeur souhaitez-vous pour votre produit pour le descripteur " + str (option) + " ?",0,10)

#Recupere les modèles voulus
equation,parametre = des.recupModele(option,valeur)
st.write("Le modèle optimale pour le descripteur " + str(option) + " à la valeur "+str(valeur)+" requiert ces mesures : " + str(parametre))
st.write(equation)


_ = """
Réalisation du calcul de la valeur à partir d'une chaine de caractère.
Les équations prise pour l'instant sont toute en log10, les entrées et les sorties doivent donc l'êtrec aussi

TO DO : - Prendre en compte plusieurs inconnues si besoin
"""
x = sp.symbols('x')
equation_sympy = sp.sympify(equation)
if valeur == 0:#Les valeurs étant en log10, il est impossible de faire le log de 0 alors on prend une valeur proche
    valeur = 0.25
solutions = sp.solveset(sp.Eq(equation_sympy,log10(valeur)),x)
st.write("Il vous faut des mesures de "+parametre+" égal à: "+str(solutions)+"")


