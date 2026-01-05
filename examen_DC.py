import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup as bs
from requests import get
import base64
import seaborn as sn
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import altair as alt

# Scraper sur plusieurs pages
def scraper_page(url, stop=119):
    if "chaussures-enfants" in url and stop > 8:
        stop = 8

    if "vetements-enfants" in url and stop > 22:
        stop = 22

    df = pd.DataFrame()
    for index_page in range(1,stop+1):
        url_page = f"{url}?page={index_page}"
        # récupération du contenu de la page
        res = get(url_page)
        # Avoir le contenu dans un objet bs et sparsifier
        soup = bs(res.content, "html.parser")
        # récupération des conteneurs
        containers = soup.find_all("div", "col s6 m4 l3")

        data = []
        for container in containers:
            try:
                type_article = container.find("p", "ad__card-description").text
                prix = container.find("p", "ad__card-price").text.replace("CFA", " ")
                adresse = container.find("p", "ad__card-location").text
                image = "https://image.coinafrica.com" + container.find("img")["src"]
                dic = {
                "Type": type_article,
                "Prix": prix,
                "Adresse": adresse,
                "Image": image
                }
                data.append(dic)
            except:
                pass
        # Dataframe
        DF = pd.DataFrame(data)
        df = pd.concat([df, DF], axis= 0).reset_index(drop= True)
    if "Type" in df.columns:
        df['Type'] = df["Type"].astype(str)
    
    if "Prix" in df.columns:
        df['Prix'] = pd.to_numeric(df["Prix"], errors="coerce")

    return df


url_1 = "https://sn.coinafrique.com/categorie/vetements-homme"
url_2 = "https://sn.coinafrique.com/categorie/chaussures-homme"
url_3 = "https://sn.coinafrique.com/categorie/vetements-enfants"
url_4 = "https://sn.coinafrique.com/categorie/chaussures-enfants"

# Personnalisation de la mise en page
st.set_page_config(layout="wide")
st.title("Ma première application Streamlit")

st.header("Coinafrica Sénégal", divider="gray", width="stretch", text_alignment="justify")
st.image("coinafrica_images.png", width=200)
st.markdown( """
    <div style="text-align:center;">
        
    </div>
    """,
    unsafe_allow_html=True
)

if st.button("Bienvenue"):
    st.write("Vous etes sur Coinafrica Sénégal. En quoi nous pouvons vous aider?")
else:
    st.write("Merci pour la visite")





st.markdown(
    """
    <style>
        .stApp {
            background-color: #e8f0fe;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar
st.sidebar.markdown("""
    <h2 style='color: #003366;
        font-size: 24px;
        text-align: center;
        font-weight: bold;
        background-color: #FF9800'>
        Option pour utilisateur
    </h2> """, unsafe_allow_html=True)


# Éléments interactifs
nb_pages = st.sidebar.selectbox("Nombre de pages à scraper", options=list(range(1, 119)))

option = st.sidebar.selectbox(
    "Choisir l'action à réaliser",
    options=["Scraper les données suivant plusieurs pages", "Charger les données Web Scrapées", "Visualiser les données", "Remplir le formulaire d'evaluation"]
    )


# Contenu principal

st.markdown("<h1 style='text-align: center; color: #333; font-family: Arial; font-weight: bold; font-style: italic; background-color: #f4f4f4; border-left: 5px solid 007BFF'>Projet 2 Coinafrica</h1>", unsafe_allow_html=True)

st.markdown(
    "<div style='margin-bottom:10px'></div>",
    unsafe_allow_html=True
)

st.markdown("""
    <div style='border: 2px solid #ccc; padding: 18px; text-align: justify; font-style: italic; margin-bottom: 10px; font-size: 16px; font-weight: 400; color: #000000; font-family: "Courier New", monospace'>
    <p>
    Cette application développée avec Streamlit permet de scraper des données sur plusieurs pages, télécharger des données déjà scaper à travers Web Scraper 
    voir un dashbord des données et remplir un formulaire d'évaluation de l'app Kobo ou Google Forms) des données
    d'annonces de vetements pour homme et enfant depuis le site Coinafrique Sénégal.
    Elle s'adresse aux utilisateurs souhaitant collecter et analyser des données de marché sur les articles en vente. Data source: <a href='https://sn.coinafrique.com'>Coinafrique</a>
     </p>
    </div>
    """, unsafe_allow_html=True)




if option == "Scraper les Données suivant plusieurs pages":        
    # contenaire centrer 
    st.subheader(" Sélection d'une catégorie à scraper")

    # Scraper les vetements homme
    if st.button("Scraper les vetements homme"):
        st.info(f"Scraping des vetements homme sur {nb_pages} en cours...")
        df_vetements_homme = scraper_page(url_1, nb_pages)
        st.success(f"{len(df_vetements_homme)} annonces récupérées")
        st.write('Data dimension: ' + str(df_vetements_homme.shape[0]) + ' rows and ' + str(df_vetements_homme.shape[1]) + ' columns.')
        st.dataframe(df_vetements_homme)
        csv = df_vetements_homme.to_csv(index=False).encode('utf-8-sig')
        st.download_button("Télécharger CSV", data=csv, file_name="vetements-homme.csv", mime='text/csv')

    # Scraper les chaussures homme
    if st.button("Scraper les chaussures homme"):
        st.info(f"Scraping des chaussures homme sur {nb_pages} en cours...")
        df_chaussures_homme = scraper_page(url_2, nb_pages)
        st.success(f"{len(df_chaussures_homme)} annonces récupérées")
        st.write('Data dimension: ' + str(df_chaussures_homme.shape[0]) + ' rows and ' + str(df_chaussures_homme.shape[1]) + ' columns.')
        st.dataframe(df_chaussures_homme)
        csv = df_chaussures_homme.to_csv(index=False).encode('utf-8-sig')
        st.download_button("Télécharger CSV", data=csv, file_name="chaussures-homme.csv", mime='text/csv')

    # Scraper les vetements enfants
    if st.button("Scraper les vetements enfants"):
        st.info(f"Scraping des vetements enfant sur {nb_pages} en cours...")
        df_vetements_enfant = scraper_page(url_3, nb_pages)
        st.success(f"{len(df_vetements_enfant)} annonces récupérées")
        st.write('Data dimension: ' + str(df_vetements_enfant.shape[0]) + ' rows and ' + str(df_vetements_enfant.shape[1]) + ' columns.')
        st.dataframe(df_vetements_enfant)
        csv = df_vetements_enfant.to_csv(index=False).encode('utf-8-sig')
        st.download_button("Télécharger CSV", data=csv, file_name="vetements-enfants.csv", mime='text/csv')

     # Scraper les chaussures enfant
    if st.button("Scraper les chaussures enfant"):
        st.info(f"Scraping des chaussures enfant sur {nb_pages} en cours...")
        df_chaussures_enfant = scraper_page(url_4, nb_pages)
        st.success(f"{len(df_chaussures_enfant)} annonces récupérées")
        st.write('Data dimension: ' + str(df_chaussures_enfant.shape[0]) + ' rows and ' + str(df_chaussures_enfant.shape[1]) + ' columns.')
        st.dataframe(df_chaussures_enfant)
        csv = df_chaussures_enfant.to_csv(index=False).encode('utf-8-sig')
        st.download_button("Télécharger CSV", data=csv, file_name="chaussures-enfants.csv", mime='text/csv')   
    

        # Fin du conteneur

elif option == "Charger les données Web Scrapées":

    # Fonction de loading des données
    def load_(dataframe, title, key) :
    

        if st.button(title,key):
        
            st.subheader('Display data dimension')
            st.write('Data dimension: ' + str(dataframe.shape[0]) + ' rows and ' + str(dataframe.shape[1]) + ' columns.')
            st.dataframe(dataframe)
            csv = dataframe.to_csv(index=False).encode('utf-8-sig')
            st.download_button("Télécharger CSV", data=csv, file_name=title+".csv", mime='text/csv')



            
    # Charger les données 
    load_(pd.read_csv('data/vetements-homme.csv'), 'Données sur les vetements hommes', '1')
    load_(pd.read_csv('data/chaussures-homme.csv'), 'Données sur les chaussures hommes', '2')
    load_(pd.read_csv('data/vetements-enfants.csv'), 'Données sur les vetements homme', '3')
    load_(pd.read_csv('data/chaussures-enfants.csv'), 'Données sur les chaussures enfants', '4')

elif option == "Visualiser les données":
    
    st.markdown("### Visualisation des données nettoyées")

    fichier = st.selectbox("Choisir une catégorie", 
                           options=["Vetements homme", "Chaussures homme", "Vetements enfant", "Chaussures enfant"])

    # Charger le fichier en fonction du choix
    if fichier == "Vetements homme":
        # df = pd.read_csv("data/vetements-homme.csv").head(n=15)
        # st.bar_chart(df[['Type', 'prix', 'adresse']], horizontal=True)
        df = (pd.read_csv("data/vetements-homme.csv")[["Type","prix", "adresse"]].head(15))
        st.line_chart(df)
    elif fichier == "Chaussures homme":
        # df = pd.read_csv("data/chaussures-homme.csv").head(n=15)
        # st.bar_chart(df[['Type', 'prix', 'adresse']], horizontal=True)
        df = (pd.read_csv("data/chaussures-homme.csv")[["Type","prix", "adresse"]].head(15))
        st.line_chart(df)
    elif fichier == "Vetements enfant":
        # df = pd.read_csv("data/vetements-enfants.csv").head(n=15)        
        # st.bar_chart(df[['type', 'prix', 'adresse']], horizontal=True)
        df = (pd.read_csv("data/vetements-enfants.csv")[["type","prix", "ardresse"]].head(15))
        st.line_chart(df)
    elif fichier == "Chaussures enfant":
        # df = pd.read_csv("data/chaussures-enfants.csv").head(n=15)
        # st.bar_chart(df[['type', 'prix', 'adresse']], horizontal=True)
        df = (pd.read_csv("data/chaussures-enfants.csv")[["Type","prix", "adresse"]])
        st.line_chart(df)
    

else:
    col1, col2 = st.columns(2)
    with col1:
        bouton1 = st.link_button(label="Kobotoolbox", url="https://ee.kobotoolbox.org/x/MKLSh7BJ", type="secondary")
    
    with col2:
        bouton2 = st.link_button(label="Google forms", url="https://docs.google.com/forms/d/e/1FAIpQLSdgKnB4i6AVRZEvLf2h4NzE9Fd2DI2taUvkqma9tjvKXlqsKQ/viewform?usp=header", type="primary")    




# Personnalisation avec le css

st.markdown("""
    <style>
    .main {
        background-image: url(""https://www.codewithrandom.com/wp-content/uploads/2022/10/Number-Guessing-Game-using-JavaScript-3.png"");
        color: black;
    }
    .stButton button {
        background-color: bold;
        color: black;
        font-weight: #FFFFFF ;
        width: 300px;
        height: 50px;
        border-radius: 10px;
    }
            
    /* Fond personnalisé de la barre lateral(siderbar) */
        section[data-testid="stSidebar"] {
        background-image: #00FF00;
      }

    /* Changer la couleur des titres et textes dans la sidebar */
        section[data-testid="stSidebar"] {
        color: bold ! important; 
        font-weight: #FFFFFF;
    }

    /* Facultatif : pour changer la couleur de fond des selectbox */
        section[data-testid="stSidebar"].stSelectbox {
        background-color: #FFFFFF;
        border-radius: 8px;
    }
            
     /* centrage des bonton et mise en forme */
     
    div.stButton {text-align:center}
            
    .stButton>button {
        font-size: 12px;
        height: 5em;
        width: 25em;
    }
            
    </style> """, unsafe_allow_html=True)






