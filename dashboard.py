import streamlit as st
import pandas as pd
import numpy as np
import descripteur_lib
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid

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
df_gel = pd.read_csv("Data/gel/donnees_brutes_Gels.csv",sep=";")
df_emulsion = pd.read_csv("Data/emulsion/donnees_brutes_emulsion.csv",sep=";")

#Creation variable global
list_settings_checkbox = ["Gel","Emulsion","G'","FminE","CoF30","JSM","Moyenne","jinf%","LOG10"] #remplacer plus tard
list_descripteur = df_descripteur['Descripteur'].to_list()

list_caracterisation = ["Rheologie","Texture","all"]
dict_caracterisation = {"Rheologie":["Flow","Sweep"],"Texture":["Extrusion","Penetration"],"Sensorielle":["Dans le contenant","Prise en main","Application","Rendu immédiat","Rendu 1m"]}
dict_experience = {"Dans le contenant":["Fluid","Softness"],"prise en main":["High peak","Slippery"],"Application":["Spreading","No visual residue"],"Rendu immédiat":["Greasy","sticky"],"Rendu 1 min":["No visual residue 1min","Smooth","Greasy 1min","Sticky 1min"],"Flow":["n","η1000","n1000","σ0.01","σ1","σ1000","sigma 0.01","sigma1","sigma1000","Yield stress","k","n(2)"],"Sweep":["G1","G2","tanD","Gamma DL","Sigma DL","Sigma crossover","Gamma crossover","10s","60s"],"Extrusion":["Firmness","Cohesiveness","Consistency","Viscosity index"],"Penetration":["Fmax","Fmin","Aplus","Aminus"]}

list_settings_senso_gel = ["Fluide","Filant","Glissant","Etalement","Doux","Collant","Gras","Penetrant","Effet coussin","Effet cassant","Pelucheux","Test filant"]
list_settings_gel = [x for x in df_gel.columns.to_list()[1:] if x not in list_settings_senso_gel]
list_produits_gel = df_gel["Produit"].to_list()

list_settings_senso_emulsion = ["Fluid","Softness","Adherence","High peak","Slippery","Spreading","No visual residue","Greasy","Sticky","No visual residue 1min","Smooth","Greasy 1min","Sticky 1min"]
list_settings_emulsion = [x for x in df_emulsion.columns.to_list()[1:] if x not in list_settings_senso_emulsion]
list_produits_emulsion = df_emulsion["Produit"].to_list()

#creation variable utilisateur
list_settings_senso_user = None
list_settings_user = None
list_produits_user = None
df_user = None

#Debut Streamlit
st.title("Projet ODESSA")
selected = option_menu(
    menu_title=None,
    options = ["Home","New Data","Visualization Data"],
    icons = ["house","plus circle","bar-chart"],
    menu_icon = "cast",
    default_index=0,
    orientation="horizontal"
)

######################################### Home ###################################

if selected == "Home":
    st.title("Bienvenue dans notre application")
    st.write("Explorez et visualisez différentes caractéristiques des produits cosmétiques.")

    # Ajouter une section avec des icônes et des informations supplémentaires
    st.subheader("Qu'est-ce que notre application offre ?")
    st.write("📊 Visualisation interactive des données cosmétiques.")
    st.write("📈 Analyse des tendances et des variations.")
    st.write("🔍 Ajout facile de nouvelles données pour une mise à jour dynamique.")

    # Ajouter une section pour expliquer comment utiliser l'application
    st.subheader("Comment utiliser l'application ?")
    st.write("1. Utilisez la section de gauche pour ajouter de nouvelles données.")
    st.write("2. Explorez la section de visualisation pour analyser les données existantes.")

    # Ajouter un appel à l'action pour encourager l'exploration
    st.success("Commencez dès maintenant ! 🚀")

######################################## New Data #####################################################

if selected == "New Data":
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        df_new_data = pd.read_excel(uploaded_file)
        AgGrid(df_new_data)
        print(df_new_data)
        list_caracterisation = df_new_data.iloc[[0]].dropna(axis=1).values.flatten()


    col = st.columns(3)
    with open("Doc/Modele.xlsx", 'rb') as my_file:
        with col[1]:
            st.download_button(label='Telecharger le modèle', data=my_file, file_name='Modele.xlsx',
                           mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


###################################### Visualization Data ##########################################
if selected == "Visualization Data":

    #Affichage input general
    st.sidebar.header("Input data general")

    type = st.sidebar.radio(
        "Voulez-vous emulsion ou gel ?",
        ["Emulsion", "Gel"]
    )

    if type=="Emulsion":
        list_settings_senso_user = list_settings_senso_emulsion.copy()
        list_settings_user = list_settings_emulsion.copy()
        list_produits_user = list_produits_emulsion.copy()
        df_user = df_emulsion.copy(deep=True)
    elif type=="Gel":
        list_settings_senso_user = list_settings_senso_gel.copy()
        list_settings_user = list_settings_gel.copy()
        list_produits_user = list_produits_gel.copy()
        df_user = df_gel.copy(deep=True)

    ######################### INSTRUMENTAL ###########################

    #Affichage input instru
    ite=0
    st.sidebar.header("Input data instru")
    st.sidebar.subheader("simple bar chart")

    option_caracterisation = st.sidebar.selectbox(#A implémenter
        'Quel caractérisation voulez vous ?',
        list_caracterisation,
        placeholder="Selectionner une caractérisation...",
        key="op_caractérisation_user"
    )

    option_parametre = st.sidebar.multiselect(
        'Quel parametre voulez vous ?',
        list_settings_user,
        placeholder="Selectionner un parametre...",
        key="op_settings_user",
    )

    option_produit = st.sidebar.multiselect(
        'Quel(s) produit(s) voulez vous ?',
        list_produits_user,
        placeholder="Selectionner un ou plusieurs produits...",
        key="op_produit_user",
    )

    #Analyse données instrumentales
    st.header("Analyse des données intrumentales")

    if option_parametre==[] and option_caracterisation!="all":
        tempo_list = dict_caracterisation.get(option_caracterisation)
        tempo_list2 = [dict_experience.get(key) for key in tempo_list]
        option_parametre = [n for one_dim in tempo_list2 for n in one_dim]

    elif option_parametre == []:
            option_parametre = list_settings_user.copy()

    if option_produit == []:
        print(option_parametre)
        st.dataframe(df_user[['Produit']+option_parametre])
        st.bar_chart(df_user, x="Produit", y=option_parametre)
    else:
        st.dataframe(df_user[['Produit']+option_parametre][df_user['Produit'].isin(option_produit)])
        st.bar_chart(df_user[df_user['Produit'].isin(option_produit)], x="Produit", y=option_parametre)

    with st.expander("Voir explication"):
        st.write("Cette fonctionnalité est en cours de developpement")
        st.image("https://static.streamlit.io/examples/dice.jpg")



    ####################### SENSO #############################""

    ##Affichage input senso
    st.sidebar.header("Input data senso")
    option_senso = st.sidebar.multiselect(
        'Quel(s) parametre sensoriel voulez vous ?',
        list_settings_senso_user,
        placeholder="Selectionner un ou plusieurs parametre sensoriel...",
        key="op_senso_user",
    )


    #Analyse données sensorielle
    st.header("Analyse des données sensorielle")

    if option_senso==[]:
        option_senso = list_settings_senso_user.copy()
    if option_produit == []:
        st.dataframe(df_user[['Produit']+option_senso])
        st.bar_chart(df_user, x="Produit", y=option_senso)
    else:
        st.dataframe(df_user[['Produit']+option_senso][df_user['Produit'].isin(option_produit)])
        st.bar_chart(df_user[df_user['Produit'].isin(option_produit)], x="Produit", y=option_senso)

    df_descripteur_user = df_descripteur[df_descripteur['Descripteur'].isin(option_senso)]
    for i in df_descripteur_user.index:
        st.markdown("**"+df_descripteur_user["Descripteur"][i] + "**: "+df_descripteur_user["Explication"][i])




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

    #Affichage modèle
    df_modele_user = change_dataframe(df_modele)
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