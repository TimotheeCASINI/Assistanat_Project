#Librarie permettant de gérer les différentes interaction entre l'application streamlit et les informations sur les descripteurs


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
