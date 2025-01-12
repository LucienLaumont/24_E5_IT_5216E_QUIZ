### Projet Quiz FullStack

Bienvenue sur le projet FullStack Quizz Olympique sur le sujet des Jo de Paris 2024. 


## Architecture du Projet

Le projet est donc une webapp permettant aux utilisateurs de répondre à un quizz et d'évaluer ses connaissances sur les JO.
Cela est permis par une base de donnée backend que l'on alimente avec les questions, et qui récupère et enregistre les réponses des participants pour établir un classement.
L'application run sous Flask, et l'UI est générée avec VueJS. La BDD est sous SQL-Lite, et communique avec l'application via des API Fast-API. 
Le tout est hébergé sur 2 conteneurs différents, un pour le backend, et un pour le frontend.


## Utilisateurs

Comme mentioné plus tôt, les utilisateurs peuvent se connecter au site, puis commencer une partie.
Les utilisateurs ont aussi accès à un certain nombre d'informations sur la Main Page.
A la fin, ils obtiennent leur score, ainsi que leur place sur le classement, et peuvent retenter leur chance jusqu'à accéder au podium!


## Les admins

Beaucoup d'actions nécéssitent une identification par mot de passe. En effet, un ulisateur lambda ne doit pas pouvoir modifier la BDD, les questions, ou les scores de chacun et pouvoir tricher. 
Après identification, les admins peuvent effectuer un certain nombre d'actions pour modifier le Quizz. 
Ils peuvent modifier l'ordre des questions, leur titre, le texte, l'image, voire même tout supprimer. 
Il est également possible de modifier les scores et noms des participants!

Ces actions se font via Postman, et ainsi alimenter/manipuler la base de donnée dynamiquement sans que son contenu soit stocké directement dans les conteneurs. Un accès administrateur sur le site est prévu ulterieurment.

### Amusez vous bien!