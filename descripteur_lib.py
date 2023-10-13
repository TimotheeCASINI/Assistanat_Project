#Librarie permettant de gérer les différentes interaction entre l'application streamlit et
#les informations dans les différentes bdd

import pandas as pd

def recupDescripteur():
    """
    But : Recupere les descripteur dans la bdd qui se trouve dans le dossier descripteur et le fichier CSV
    Output : DataFrame pandas
    """
    df = pd.read_csv("Descripteur/descripeur_bdd.csv")
    return df

def recupModele(descripteur,valeur):
    """
    But : Renvoie le modèle qui va être utilisé pour calculer la valeur voulu
    paramètre : le nom du descripteur voulu et la valeur de descripteur recherche
    """
    #Réduction du dataframe avec seulement la bonne valeur et le descripteur
    df = pd.read_csv("Modele/modele.csv")
    df = df[(df.Descripteur == descripteur) & (df.Min <= valeur) & (df.Max >= valeur)]
    #Recuperation du modèle un peu plus logique que ca
    df = df.iloc[0]
    equation = df['Equation']
    para = df['Parametre']
    return equation,para

def recupModeles():
    """
    But : Renvoie tous les modèles d'un descripteur et les metadonnées
    paramètre : le nom du descripteur voulu
    """
    #Réduction du dataframe avec seulement la bonne valeur et le descripteur
    df = pd.read_csv("Modele/modele.csv")
    return df