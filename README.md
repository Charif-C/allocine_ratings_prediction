# Sujet :

A partir des informations disponibles sur tous les films déjà sortis à l’écran et grâce aux techniques et méthodes apprises en Datamining, nous avons essayé de prévoir les notes d’un film avant sa sortie.

# Données :

## Source

Afin de récupérer les données dont nous avons eu besoin, nous avons décidé de scrapper le site d’Allociné et plus précisément la page : http://www.allocine.fr/films/
Cette page nous a permis de récupérer les données de plusieurs films pour chaque requête, ce qui a accéléré le fonctionnement de notre scrapper.
Le scrapper utilisé a été réalisé avec la librairie Python Beautiful Soup.
Le fichier correspondant est [ScrapVall.ipynb](https://github.com/Charif-C/allocine_ratings_prediction/blob/master/ScrapVall.ipynb)

Pour chaque film, nous récupérons :
-	Le titre
-	La date de sortie
-	Le(s) réalisateur(s)
-	Les acteurs
-	Le(s) genre(s)
-	La note presse
-	La note spectateurs

## Taille des données récupérées

Plusieurs scrappings ont été mis en place et plusieurs csv ont été créés. En effet, pour améliorer la qualité des données, le volume des csv et la performance du scrapper, nous avons dû faire plusieurs essais.

Le csv final comptait :
-	25 000 lignes environ
-	7 colonnes

Il s’agit d’une concaténation des fichiers : [scrapperv11_1_200.csv](https://github.com/Charif-C/allocine_ratings_prediction/blob/master/scrapperv11_1_200.csv), [scrapperv11_201_400.csv](https://github.com/Charif-C/allocine_ratings_prediction/blob/master/scrapperv11_201_400.csv), [scrapperv11_401_600.csv](https://github.com/Charif-C/allocine_ratings_prediction/blob/master/scrapperv11_401_600.csv), [scrapperv11_601_800.csv](https://github.com/Charif-C/allocine_ratings_prediction/blob/master/scrapperv11_601_800.csv), [scrapperv11_801_1000.csv](https://github.com/Charif-C/allocine_ratings_prediction/blob/master/scrapperv11_801_1000.csv), [scrapperv10_1001_1500.csv](https://github.com/Charif-C/allocine_ratings_prediction/blob/master/scrapperv11_1001_1500.csv), [scrapperv10_1501_2000.csv](https://github.com/Charif-C/allocine_ratings_prediction/blob/master/scrapperv10_1501_2000.csv).

## Nettoyage des données

Pour utiliser au mieux les données du site Allociné, il a fallu nettoyer les données et les adapter pour nos traitements.
Il a fallu par exemple revoir la forme des notes afin de remplacer la virgule par un point pour pouvoir directement utiliser nos colonnes.

## Traitement des données pour utilisation

Dans un premier temps, nous avons arrêté d’utiliser les colonnes Titre et Date, inutiles pour les prévisions de notes. De même, après analyse des données, nous avons décidé de travailler uniquement sur la note des spectateurs qui est plus renseignée que la note presse.

Afin de pouvoir utiliser la colonne « acteurs », il a fallu passer d’une colonne pour tous les acteurs à une colonne pour chaque acteur. Nous avons fait transformer cette colonne en une « matrice binaire » : les colonnes étant les noms des acteurs de tous les films du csv et les lignes étant les films, cette matrice est remplie de 0 ou 1 pour signifier la présence ou non de l’acteur.

Ce traitement s’est fait dans le fichier [Data_Processing_4.ipynb](https://github.com/Charif-C/allocine_ratings_prediction/blob/master/Data_Processing_4.ipynb).

Le CSV utilisable, data_processing_4.csv, compte 25 000 lignes et 40 000 colonnes environ.

# Méthodes utilisées pour la classification :

Afin de traiter notre csv, nous avons utilisé les bibliothèques Python : Pandas, Numpy et ScikitLearn.

Les classifieurs utilisés pour prévoir la note d’un film ont été :
  * Régression linéaire
  * Arbre de décision
  * Random Forest
  * XGBoost

Pour évaluer les performances, nous avons utilisé la MSE (Mean Squarred Error) sur la base d'un classifieur "aléatoire" : nous avons ajouté une colonne sur la base d'un array Numpy, avec des notes aléatoire (« random ») de 0 à 5, puis évalué la MSE entre cette colonne et les vraies notes.
Sur les classifieurs testés, un seul ne converge pas (régression linéaire), et les autres sont meilleurs que l'aléatoire.

Le fichier correspondant est [Spectators Rating Prediction V1.ipynb](https://github.com/Charif-C/allocine_ratings_prediction/blob/master/Spectators%20Rating%20Prediction%20V1.ipynb).
