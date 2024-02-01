import streamlit as st
import pandas as pd
import numpy as np
import descripteur_lib
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid
#from streamlit_extras.app_logo import add_logo

def get_dict_BDD_generale():
    dict_df = pd.read_excel("Data/BDD generale/BDD.xlsx",sheet_name=None)
    return dict_df

def load_generale_data():
    dict_BDD = get_dict_BDD_generale()
    df = pd.concat(dict_BDD,axis=1, join="inner")
    load_data(df,"Données sensorielles & instrumentales",True)
    print("Not implemented")

def change_dataframe(df_modele):
    if st.session_state.op_descripteur != None:
        new_df = df_modele[df_modele['Descripteur'].isin([st.session_state.op_descripteur])]
    else:
        new_df = df_modele.copy(deep=True)
    return new_df

def graph_loading(option_parametre):
    st.dataframe(st.session_state.df[['Produit'] + option_parametre])
    st.bar_chart(st.session_state.df, x="Produit", y=option_parametre)

def load_explanation():
    st.write("Cette fonctionnalité est en cours de developpement")
    st.image("https://static.streamlit.io/examples/dice.jpg")

def supp_session_state_data():
    for key in st.session_state.keys():
        del st.session_state[key]
    st.session_state.data_load = False

def check_double(list_to_check):
    newlist = []
    duplist = []
    for i in list_to_check:
        if i not in newlist:
            newlist.append(i)
        else:
            duplist.append(i)  #capture les premiers doublons et les ajoute à la liste
    if len(duplist)>0:
        return True,duplist
    else:
        return False,[]


def load_data(uploaded_file,type_data,generale_BDD):
    supp_session_state_data()
    if generale_BDD:
        df_new_data = uploaded_file
    else:
        df_new_data = pd.read_excel(uploaded_file)
        AgGrid(df_new_data)
    st.session_state.list_caracterisation = df_new_data.iloc[[0]].dropna(
        axis=1).values.flatten()  # list_caracterisation => liste des catégories tel que Analyse sensorielle
    st.session_state.dict_caracterisation = {}  # Creation dict Caracterisation )> dictionnaire qui permet de lier les catégories (clé) avec les cous catégories (values)
    for caract_key in st.session_state.list_caracterisation:  # Creation dict_caracterisation, Parcours toutes les catégories
        result = df_new_data.isin([caract_key])
        columnNames = result.any()
        colomn_key_name = list(columnNames[columnNames == True].index)
        caract_key_index = df_new_data.columns.get_loc(colomn_key_name[0])
        list_carac_value = []
        for index in range(caract_key_index, df_new_data.shape[
            1]):  # Parcours toutes les sous catégories à partir de l'id de leur catégories
            value_column = df_new_data.iloc[1, index]
            if pd.isnull(df_new_data.iloc[0, index]) == False and df_new_data.iloc[
                0, index] != caract_key:  # Break permettant de changer de catégories
                break
            if pd.isnull(value_column) == False:
                list_carac_value.append(value_column)
        st.session_state.dict_caracterisation[caract_key] = list_carac_value

    list_experience = (
        st.session_state.dict_caracterisation.values())  # Liste experience => liste de toutes les expériences
    list_experience = [x for sub in list_experience for x in sub]  # liste 2D en 1D
    st.session_state.dict_experience = {}  # Creation dict experience )> dictionnaire qui permet de lier les sous catégories (clé) avec les variables (values)
    for experience_key in list_experience:  # Creation dict_experience
        result = df_new_data.isin([experience_key])
        columnNames = result.any()
        colomn_key_name = list(columnNames[columnNames == True].index)
        experience_key_index = df_new_data.columns.get_loc(colomn_key_name[0])
        list_experience_value = []
        for index in range(experience_key_index, df_new_data.shape[1]):
            value_column = df_new_data.iloc[2, index]
            if pd.isnull(df_new_data.iloc[1, index]) == False and df_new_data.iloc[
                1, index] != experience_key:  # Break permettant de changer de sous catégories
                break
            if pd.isnull(value_column) == False:
                list_experience_value.append(value_column)
        st.session_state.dict_experience[experience_key] = list_experience_value

    st.session_state.produits_list = df_new_data.iloc[3:, 0].to_list()  # Creation liste de tous les produits
    st.session_state.list_caracterisation = np.append(st.session_state.list_caracterisation, "All")
    if type_data == "Données sensorielles & instrumentales":
        st.session_state.list_caracterisation = np.delete(st.session_state.list_caracterisation, 0, 0)
    if type_data == "Données sensorielles" or type_data=="Données sensorielles & instrumentales":
        st.session_state.list_settings_senso = [st.session_state.dict_experience[key] for key in st.session_state.dict_caracterisation["ANALYSE SENSORIELLE"]]
        st.session_state.list_settings_senso = [x for sub in st.session_state.list_settings_senso for x in sub]  # 2D en 1D
    st.session_state.list_all_settings = [x for sub in st.session_state.dict_experience.values() for x in sub]
    if type_data == "Données sensorielles & instrumentales":
        st.session_state.list_settings_instru = [x for x in st.session_state.list_all_settings if x not in st.session_state.list_settings_senso]
    elif type_data == "Données instrumentales":
        st.session_state.list_settings_instru = st.session_state.list_all_settings

    df_new_data = df_new_data.drop([0, 1])  # Modification du dataframe pour s'assurer qu'il soit utilisable
    df_new_data.iloc[0, 0] = "Produit"
    df_new_data.columns = df_new_data.iloc[0].to_list()
    df_new_data = df_new_data[1:]
    df_new_data.iloc[:,1:] = df_new_data.iloc[:,1:].apply(pd.to_numeric,errors='coerce')
    st.session_state.df = df_new_data
    st.session_state.data_load = True  # Variable permettant de s'assurer de la bonne intégration des données
    st.session_state.type_data = type_data
    if generale_BDD:
        st.session_state.name_file = "Generale BDD"
    else:
        st.session_state.name_file = uploaded_file.name

    #Verification de duplicas dans les colonnes
    list_verif_double = [st.session_state.list_caracterisation,st.session_state.list_all_settings,[x for y in list(st.session_state.dict_caracterisation.values()) for x in y]]
    print(list(st.session_state.dict_caracterisation.values()))
    for list_data in list_verif_double:
        is_double, duplicates = check_double(list_data)
        if is_double:
            supp_session_state_data()
            st.write("Il y a des duplicas dans les colonne "+str(duplicates))
            st.write("Veuiller choisir un nouveau fichier ou modifier le fichier")


def add_data():
    print(st.session_state.title_add_data)
    print("Not implemented")


#Recupération bdd (A mettre en cache)
df_descripteur = descripteur_lib.recupDescripteur()
df_modele = descripteur_lib.recupModeles()
df_modele_user = df_modele.copy(deep=True)

#Creation variable global
list_descripteur = df_descripteur['Descripteur'].to_list()#A remplacer plus tard

#creation variable utilisateur
list_settings_senso_user = None
list_settings_user = None
list_produits_user = None
df_user = None
if 'data_load' not in st.session_state:
    st.session_state.data_load = False

#Debut Streamlit
st.title("Projet ODESSA")
logo_url = "img/logo.png"
st.sidebar.image(logo_url)
selected = option_menu(
    menu_title=None,
    options = ["Home","New Data","Visualization","Prediction"],
    icons = ["house","plus circle","bar-chart","question"],
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
    st.write("1. Utilisez la section New Data pour ajouter de nouvelles données.")
    st.write("2. Explorez la section de visualisation pour analyser les données existantes.")

    # Ajouter un appel à l'action pour encourager l'exploration
    st.success("Commencez dès maintenant ! 🚀")

######################################## New Data #####################################################
_ ="""

Cette catégories permet d'ajouter des données à visualiser. de nombreuses variables seont crées pour permettre de s'assurer du bon fonctionnement
de la visualisation.
Toutes les variables seront placés dans session_state pour s'assurer qu'elle soit bien conservé lors du rechargement de la page

Amélioration potentielle : - Mettre new data dans une fonction qui sera mises en cache et rappelé la fonction au début du chargement de la parti visualisation data.
 et garder seulement dans le session_state les variables data_load, pour s'assurer du bon fonctionnement, et chemin (qui n'est pas existante), pour pouvoir réutiliser le chemin.

"""

#Ajouter all à list_caracterisation
if selected == "New Data":

    type_data = st.selectbox(
            'Quel type de donnée voulez vous mettre?',
            ["Données instrumentales", "Données sensorielles", "Données sensorielles & instrumentales"],
            placeholder="Selectionner un type...",
            key="op_data_type_user",
            index=None
        )
    if type_data != None:
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            if uploaded_file.name.startswith("BDD."):
                st.write("Pour des raisons de sécurité votre fichier n'est pas permis de s'appeler comme ca")
            else:
                load_data(uploaded_file,type_data,False)

    col = st.columns(3)
    with open("Doc/Modele.xlsx", 'rb') as my_file:
        with col[1]:
            st.download_button(label='Telecharger le modèle', data=my_file, file_name='Modele.xlsx',
                           mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


###################################### Visualization Data ##########################################
_ = """
Cette partie permet la visualisation des donnnées.
Il y a deux parties : -Une partie instru (Input, graph)
- Une partie senso (Input, Graph)
"""

if selected == "Visualization":
    if not st.session_state.data_load:
        st.header("Veuillez mettre un document ou charger la base de données générale")
        col = st.columns(3)
        with col[1]:
            st.button("Charger base de données de générale",on_click=load_generale_data)

    else:
        if st.session_state.type_data == "Données sensorielles" or st.session_state.type_data == "Données sensorielles & instrumentales":
            list_settings_senso_user = st.session_state.list_settings_senso.copy()
        if st.session_state.type_data == "Données instrumentales" or st.session_state.type_data == "Données sensorielles & instrumentales":
            list_settings_user = st.session_state.list_settings_instru.copy()
        list_produits_user = st.session_state.produits_list.copy()
        df_user = st.session_state.df.copy(deep=True)

        st.header("Analyse du fichier "+st.session_state.name_file)

        st.sidebar.subheader("Input generale")
        option_produit = st.sidebar.multiselect(
            'Quel(s) produit(s) voulez vous ?',
            list_produits_user,
            placeholder="Selectionner un ou plusieurs produits...",
            key="op_produit_user",
        )

        if st.session_state.type_data == "Données instrumentales" or st.session_state.type_data == "Données sensorielles & instrumentales":
            ######################### INSTRUMENTAL ###########################

            # Affichage input instru
            ite=0
            st.sidebar.subheader("Input data instru")
            st.sidebar.subheader("simple bar chart")

            option_caracterisation = st.sidebar.selectbox(
                'Quel caractérisation voulez vous ?',
                st.session_state.list_caracterisation,
                placeholder="Selectionner une caractérisation...",
                key="op_caractérisation_user",
            )

            option_parametre = st.sidebar.multiselect(
                'Quel parametre voulez vous ?',
                list_settings_user,
                placeholder="Selectionner un parametre...",
                key="op_settings_user",
            )

            #Analyse données instrumentales
            st.subheader("Analyse des données intrumentales")
            if option_parametre==[] and option_caracterisation!="All":
                tempo_list = st.session_state.dict_caracterisation.get(option_caracterisation)
                tempo_list2 = [st.session_state.dict_experience.get(key) for key in tempo_list]
                option_parametre = [n for one_dim in tempo_list2 for n in one_dim]

            elif option_parametre == []:
                option_parametre = list_settings_user.copy()

            if option_produit == []:
                graph_loading(option_parametre)
            else:
                st.dataframe(df_user[['Produit']+option_parametre][df_user['Produit'].isin(option_produit)])
                st.bar_chart(df_user[df_user['Produit'].isin(option_produit)], x="Produit", y=option_parametre)

            with st.expander("Voir explication"):
                load_explanation()


        if st.session_state.type_data == "Données sensorielles" or st.session_state.type_data == "Données sensorielles & instrumentales":
            ####################### SENSO #############################

            ##Affichage input senso
            st.sidebar.header("Input data senso")
            option_senso = st.sidebar.multiselect(
                'Quel(s) parametre sensoriel voulez vous ?',
                list_settings_senso_user,
                placeholder="Selectionner un ou plusieurs parametre sensoriel...",
                key="op_senso_user",
            )


            #Analyse données sensorielle
            st.subheader("Analyse des données sensorielle")

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

        if st.session_state.type_data == "Données sensorielles & instrumentales":
            ####################### Modele #############################

            #Analyse modèle
            st.subheader("Analyse des modèles")

            #Affichage input
            option_descripteur = st.selectbox(
                'Quel descripteur souhaitez vous ?',
                list_settings_senso_user,
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
            for i in st.session_state.list_settings_instru:
                with a[ite%3]:
                    st.checkbox(i,key=i)
                ite = ite + 1

            #Affichage modèle
            df_modele_user = change_dataframe(df_modele)
            st.text("Nombre de modèle correspondant "+str(df_modele_user.shape[0])+" :")
            st.dataframe(df_modele_user,hide_index=True)

            #Selection ligne
            _ = """
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

#################################### Autre ###################################"

        st.sidebar.header("Sauvegarde données")
        if st.sidebar.button("Sauvegarde des données dans la bdd"):
            title = st.sidebar.text_input('Nom des données à sauvegarder',on_change=add_data,key="title_add_data")
            #st.sidebar.button("Ajouter",on_click=add_data,args=(title,))
        st.sidebar.header("Enlever données")
        st.sidebar.button("Enlever les données",on_click=supp_session_state_data())

    if selected == "Prediction":
        st.write("not here")
