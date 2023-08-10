import pandas as pd
descripteur = 'Fluide'
valeur = 7
df = pd.read_csv("Modele/modele.csv")
df = df[(df.Descripteur == descripteur) & (df.Min <= valeur) & (df.Max >= valeur)]
#Recuperation du modèle un peu plus logique que ca
fonction = df.at[0,'Equation']
print(type(fonction[0]))