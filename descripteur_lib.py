#Librarie permettant de gérer les différentes interaction entre l'application streamlit et les informations sur les descripteurs

import pandas as pd

def présentation(descripteur):
    """
    But : Renvoie STRING avec description du descripteur choisi
    paramètre : le nom du descripteur voulu
    """
    if descripteur == "Fluide":
        return "Descripteur permettant de déterminer a quel point un produit est fluide"
    elif descripteur == "Filant":
        return "Descripteur permettant de déterminer a quel point un produit est filant"
    else:
        return "Rien a affiche pour ce descripteur"

def recupModele(descripteur,valeur):
    """
    But : Renvoie le modèle qui va être utilisé pour calculer la valeur voulu
    paramètre : le nom du descripteur voulu et la valeur de descripteur recherchee
    """
    #Réduction du dataframe avec seulement la bonne valeur et le descripteur
    df = pd.read_csv("Modele/modele.csv")
    df = df[(df.Descripteur == descripteur) & (df.Min <= valeur) & (df.Max >= valeur)]
    #Recuperation du modèle un peu plus logique que ca
    df = df.iloc[0]
    equation = df['Equation']
    return equation