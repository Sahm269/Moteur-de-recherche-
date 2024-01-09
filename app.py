import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import praw
from classes.Document import Document 
from classes.Author import Author
from classes.Corpus import Corpus
import datetime 
import pandas as pd 
import urllib.request
import xmltodict
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

#=========================
app = dash.Dash(__name__, suppress_callback_exceptions=True)



mon_corpus = Corpus(nom="Corpus_article")


# Première page (Page d'accueil)
layout_accueil = html.Div([
    html.H1("Recuperer les Données"),
    html.Div([
        html.Div([ 
            html.H3("Reddit"),

            html.Label("Thème Reddit"),
            dcc.Input(id='theme_reddit_input', type='text', value='football', placeholder='Entrez le thème Reddit'),
        
            html.Label("Limite Reddit"),
            dcc.Slider(id='limit_reddit_input', min=1, max=100, step=1, value=10, marks={i: str(i) for i in range(0, 101, 10)}),


            html.Div([

                html.Div([
                html.Label("ID Client"),
                dcc.Input(id='idclient_input', type='text', value='_jjmAvQmLvyPWeH7mSTYrw', placeholder='Entrez l\'ID Client Reddit')]),
                
                html.Div([
                html.Label("Secret Client"),
                dcc.Input(id='secretclient_input', type='text', value='j7vF0wxXN9VuvOrIri3dt3W4fSvH4w', placeholder='Entrez le Secret Client Reddit')]),

                html.Div([
                html.Label("Utilisateur"),
                dcc.Input(id='user_input', type='text', value='td3', placeholder='Entrez le nom d\'utilisateur Reddit')]) ],className="identifiant" ),
            
            ],className='reddit'),

        
        html.Div([ 
            html.H3("Arxiv"),

            html.Label("Thème Arxiv"),
            dcc.Input(id='theme_arxiv_input', type='text', value='foot', placeholder='Entrez le thème Arxiv'),
        
            html.Label("Limite Arxiv"),
            dcc.Slider(id='limit_arxiv_input', min=1, max=100, step=1, value=10, marks={i: str(i) for i in range(0, 101, 10)}),
            html.Div([ 
                html.Button(id='save_corpus_button', n_clicks=0, children='Enregistrer le Corpus'),
                 html.Button(id='load_data_button', n_clicks=0, children='Recupérer les Données')
            ], className='btnsave' )
        
        ], className='arxiv'),

    ],className='formulaire'),

    
    
    html.Div(id='result_output'),
    
    html.Button(id='show_corpus_button', n_clicks=0, children='Afficher le Corpus'),
    
    
    
    html.Button(id='open_corpus_button', n_clicks=0, children='Ouvrir le Corpus'),

    dcc.Link('Accéder au Moteur de recherche', href='/recherche', className="link"),


    html.Div(id='result_output1'),
    html.Div(id='result_output2'),
    html.Div(id='result_output3'),




    # Ajoutez ce lien vers votre fichier CSS
    html.Link(rel='stylesheet', href='/assets/app.css')
], className='container')

# Deuxième page (Moteur de recherche de recherche)
layout_recherche = html.Div([
    html.H1("Moteur de recherche"),
    html.Div(id='search-container', children=[
        dcc.Input(id='champ_recherche_cosinus', type='text', value='', placeholder='Entrez vos mots-clés'),
     
        html.Button(id='bouton_recherche_cosinus', n_clicks=0, children=[
            html.I(className='fas fa-search', id='icone_recherche'),
            'Rechercher'
        ]),
    ]),
    
    html.Div([
           dcc.Dropdown(
            id='source_selection',
            options=[
                {'label': 'Les deux', 'value': 'Les deux'},
                {'label': 'Reddit', 'value': 'Reddit'},
                {'label': 'Arxiv', 'value': 'Arxiv'},
            ],
            value='Les deux',
            style={'width': '50%'}  # Ajustez la largeur selon vos préférences
        ),
    ]),

    html.Div([
    dcc.Dropdown(
        id='dropdown_auteur',
        options=[], 
        multi=True,  # Permet à l'utilisateur de sélectionner plusieurs auteurs
        placeholder='Sélectionnez un ou plusieurs auteurs',
        style={'width': '50%'} 
        ),
    ]),

    html.Div(id='output_recherche_cosinus'),
    dcc.Link('Retour à la page d\'accueil', href='/' ,className='link'),
])


# Callback pour gérer les changements de page
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/recherche':
        return layout_recherche
    else:
        return layout_accueil


# Callback pour effectuer la recherche
@app.callback(
    Output('output_recherche_cosinus', 'children'),
    [Input('bouton_recherche_cosinus', 'n_clicks')],
    [State('champ_recherche_cosinus', 'value'),
     State('source_selection', 'value')]
)
def effectuer_recherche_cosinus(n_clicks, mots_clefs_utilisateur, source_selectionnee):
    if n_clicks > 0:
        

        # Chargez le corpus combiné (corpus.csv)
        mon_corpus.load("corpus.csv")
        mon_corpus.construire_mat_tfidf()
        vocab = mon_corpus.get_vocabulaire()
        vecteur_requete = np.zeros(len(vocab))

        mots_clefs_propres = mon_corpus.nettoyer_texte(mots_clefs_utilisateur)
        for mot in mots_clefs_propres.split():
            if mot in vocab:
                mot_id = vocab[mot]['id'] - 1
                vecteur_requete[mot_id] += 1

        # Calcule la similarité
        mat_tfidf = mon_corpus.get_mattdidf()
        indices_tries = np.argsort(cosine_similarity([vecteur_requete], mat_tfidf)[0])[::-1]
        id2doc = mon_corpus.get_id2doc()

        # Filtrer les résultats en fonction de la source sélectionnée
        if source_selectionnee == 'Reddit':
            indices_tries = [indice for indice in indices_tries if id2doc[indice + 1].type == 'Reddit']
        elif source_selectionnee == 'Arxiv':
            indices_tries = [indice for indice in indices_tries if id2doc[indice + 1].type == 'Arxiv']

      

        # Construire le contenu HTML
        contenu_html = []
        for indice_document in indices_tries:
            score_similarite = cosine_similarity([vecteur_requete], mat_tfidf)[0, indice_document]

            # Si le score de similarité est supérieur à zéro
            if score_similarite > 0:
                # Indexation
                indice_document += 1
                document = id2doc.get(indice_document)  # Utilise get pour éviter une KeyError

                if document:
                    contenu_html.append(
                        html.Div([
                            html.P(f"Score de similarité avec le document {document.titre} : {score_similarite}"),
                            html.A(document.url, href=document.url, target='_blank'),
                            html.P(f"Contenu du document : {document.texte}"),
                            html.P(f"Auteur : {document.auteur}"),
                            html.P(f"Date : {document.date}"),
                            html.P(f"Type : {document.type}"),
                            html.Hr(),
                        ])
                    )


        return dcc.Loading(
            id="loading-recherche-cosinus",
            type="circle",
            children=contenu_html,
            style={'color': 'red'}
        )


# Callback pour gérer le clic sur le bouton de chargement
@app.callback(
    Output('result_output', 'children'),  # Ajoutez le composant de sortie ici
    [Input('load_data_button', 'n_clicks')],
    [
        State('theme_reddit_input', 'value'),
        State('limit_reddit_input', 'value'),
        State('idclient_input', 'value'),
        State('secretclient_input', 'value'),
        State('user_input', 'value'),
        State('theme_arxiv_input', 'value'),
        State('limit_arxiv_input', 'value'),
    ]
)
def load_data(n_clicks, theme_reddit, limit_reddit, idclient, secretclient, user, theme_arxiv, limit_arxiv):

    if n_clicks > 0:
        reddit = praw.Reddit(client_id=idclient, client_secret=secretclient, user_agent=user)
        subr = reddit.subreddit(theme_reddit)

        collection = []

        for doc in subr.controversial(limit=limit_reddit):
            titre = doc.title.replace("\n", '')
            auteur = str(doc.author)
            date = datetime.datetime.fromtimestamp(doc.created).strftime("%Y/%m/%d")
            url = "https://www.reddit.com/" + doc.permalink
            texte = doc.selftext.replace("\n", "")

            doc_class = Document(titre, auteur, date, url, texte)
            collection.append(doc_class)
            
            
    # ====================================================Partie Arxiv : 
    #==========================chargement des données Arxiv en instanciant un objet docyment
        url = f'http://export.arxiv.org/api/query?search_query=all:{theme_arxiv}&start=0&max_results={limit_arxiv}'
        url_read = urllib.request.urlopen(url).read()
    

        # url_read est un "byte stream" qui a besoin d'être décodé
        data =  url_read.decode()
        dico = xmltodict.parse(data) #xmltodict permet d'obtenir un objet ~JSON
        docs = dico['feed']['entry']
        for doc in docs:
            titre = doc["title"].replace('\n', '')  # On enlève les retours à la ligne
            try:
                authors = ", ".join([a["name"] for a in doc["author"]])  # On fait une liste d'auteurs, séparés par une virgule
            except:
                authors = doc["author"]["name"]  # Si l'auteur est seul, pas besoin de liste
            summary = doc["summary"].replace("\n", "")  # On enlève les retours à la ligne
            date = datetime.datetime.strptime(doc["published"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y/%m/%d")  # Formatage de la date en année/mois/jour avec librairie datetime

            doc_class = Document(titre, authors, date, doc["id"], summary)  # Création du Document
            collection.append(doc_class)  # Ajout du Document à la liste.
            
        # Enlever les doublons en se basant sur tout le contenu
        seen_documents = set()
        unique_collection = []

        for doc in collection:
            doc_tuple = (doc.titre, doc.auteur, doc.date, doc.texte, doc.type)
            if doc_tuple not in seen_documents:
                seen_documents.add(doc_tuple)
                unique_collection.append(doc)

        # Garder uniquement les documents avec plus de 200 caractères dans le texte
        filtered_collection = [doc for doc in unique_collection if len(doc.texte) > 200]

        # Afficher le nombre de documents avant et après le nettoyage
        print(f"Nombre de documents avant le nettoyage : {len(collection)}")
        print(f"Nombre de documents après le nettoyage : {len(filtered_collection)}")

        # Réaffecter la liste filtrée à votre collection
        collection = filtered_collection

        #Rempli le corpus 
        for doc in collection:
            if "reddit" in doc.url.lower():
                doc.type = "Reddit"
            else:
                doc.type = "Arxiv"
            mon_corpus.add(doc)
        return f"Données chargées avec succès. Thème Reddit: {theme_reddit}, Limite Reddit: {limit_reddit}, Thème Arxiv: {theme_arxiv}, Limite Arxiv: {limit_arxiv}"
    else:
        return "" 
    


# Callbacks pour les boutons du corpus
@app.callback(Output('result_output1', 'children'),
              [Input('show_corpus_button', 'n_clicks')])
def show_corpus(n_clicks):
    if n_clicks > 0:
        return repr(mon_corpus)
       
    else:
        return None

        
       
# callbacks  pour 'save_corpus_button' et 'open_corpus_button'
@app.callback(Output('result_output2', 'children'),
              [Input('save_corpus_button', 'n_clicks')])
def save_corpus(n_clicks):
    if n_clicks > 0:
        mon_corpus.save("corpus.csv")
        return f"Le corpus a été enregistré avec succès."
    else:
        return None


@app.callback(Output('result_output3', 'children'),
            [Input('open_corpus_button', 'n_clicks')])
def open_corpus(n_clicks):
    if n_clicks>0 :
        mon_corpus.load("corpus.csv") 
        return f"Le corpus a été ouvert avec succès."
    
    
    






# Exécuter l'application
if __name__ == '__main__':
    app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content'),
    ])
    app.run_server(debug=True)


