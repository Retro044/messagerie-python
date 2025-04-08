# Messagerie sécurisée 🔐

Développer une application de messagerie instantanée qui permet aux utilisateurs d'échanger des messages de manière sécurisée. L'application doit garantir la confidentialité, l'intégrité et l'authenticité des messages échangés.

## Fonctionnalités importantes

1. **Chiffrement de Bout en Bout :**
   Méthode de sécurisation des communications qui garantit que seuls les participants à une conversation peuvent lire les messages échangés.

- Les messages sont chiffrés sur l'appareil de l'expéditeur et ne sont déchiffrés que sur l'appareil du destinataire.
- Cela signifie que même les serveurs intermédiaires ou les fournisseurs de services ne peuvent pas accéder au contenu des messages.
- Fonctionnement :
  - Chaque utilisateur possède une paire de clés, un publique et une privée
  - La clé publique est utilisé pour crypter les messages
  - La clé privée permet, elle, de décrypter des données cryptées par la clé publique correspondante
  - Exemple :
    - Dylan veut envoyer un message à Julia
    - Il connait la clé publique de Julia.
    - Il écrit son message et au moment de l'envoi, sa machine crypte le message avec la **clé publique de Julia**
    - Le message est **stocké crypté en BDD**
    - Julia recoit le message crypté, elle le décrypte avec **sa clé privée**
    - Elle répond, en cryptant le message avec la clé publique de Dylan qui pourra décrypter le message avec sa clé privée
    - ...
  - Exemple d'algorithme : `RSA` pour la gestion de clés.
- Il faut donc générer une paire de clé par utilisateur
- La clé publique peut être stockée en BDD
- La clé privé doit elle être stockée sur la machine du client
  - Pour simuler cela sur un seul PC on peut créer un dossier par client et y stocker sa clé privée
- La bibliothèque Python `cryptography` peut vous aider à générer et partager des clés



2. **Authentification des Utilisateurs :**

- Mettre en place un système d'authentification pour vérifier l'identité des utilisateurs.
- Le mot de passe doit être **robuste**.
- Utiliser des mots de passe **hachés** et **salés** pour sécuriser les informations d'identification.
  - Le _hashage_ est une fonction à sens unique permettant de transformer un texte simple (mot de passe) en longue chaine de caractères illisibles.
  - Le but de stocker les mot de passe hashé dans la BDD est d'assurer que les comptes utilisateurs ne seront pas utilisable si un hacker entre dans la BDD
    - Quand l'utilisateur se connecte, on hash son mot de passe, si ce hash correspond à celui dans la BDD, alors le mot de passe est bon on valide la connexion
  - Le _salage_ lui consiste à ajouter une chaine de caractère prédéfini à ce mot de passe avant de le hasher, cela peut être n'importe quoi par exemple "coucou"
  - Ainsi un mot de passe "_abcd_" deviens "_abcdcoucou_" après salage et deviens _4b8b6f73db3805920dc963dc7547e42b785d2faa_ apres hashage (**SHA1**)

3. **Interface Utilisateur :**

- Développer une interface utilisateur simple pour envoyer et recevoir des messages.
- Utiliser une bibliothèque comme `Tkinter` pour créer une interface graphique basique.

4. **Utilisation de la POO :**

- Afin d'avoir un code évolutif et robuste votre TechLead vous demande d'utiliser la Programation Orientée Objet pour ce projet.
- Des classes logiques semblent se dessiner :
  - Utilisateur
  - Messages
  - Conversation
- N'hésitez pas à en ajouter d'autre si besoin.
- Pensez au principe d'héritage

4. **Fonctionnalité supplémentaire**

- Toujours en quête de proposition, votre TechLead vous demande de lui proposer une fonctionnalité supplémentaire pour votre messagerie, tout en gardant l'aspect sécuritaire.
- Cela peut concerner le type de message envoyé (image, vidéo, audio), le mode d'envois (groupe, fils...) ou n'importe quoi d'autre

## **Étapes du Projet :**

1. **Recherche et Conception :**

- Étudier les concepts de cryptographie et les algorithmes de chiffrement.
- Concevoir l'architecture de l'application et les flux de données.
- Comparer les outils utilisables en Python facilitant la réalisation du projet
- Choix de la BDD à utiliser
- Plannification du projet avec la méthode _Kanban_ (A faire / En cours / Fini)
  - Découpage **fin** des taches à réaliser (pas seulement le dev)
  - **Assignation** des taches
  - **Estimation** des taches (en heures ou en jours/homme)
  - Précision des **antécédents** si besoin

2. **Développement :**

- Implémenter les fonctionnalités de chiffrement et de déchiffrement.
- Développer le système d'authentification et de gestion des clés.
- Créer l'interface utilisateur pour l'envoi et la réception des messages.

3. **Tests :**

- Tester l'application pour s'assurer que les messages sont correctement chiffrés et déchiffrés.
- Vérifier la sécurité de l'authentification et de la gestion des clés.

4. **Documentation :**

- Documenter le code et **les choix de conception** (BDD ...).
- Documenter les mesures mise en place pour sécuriser l'application
  - Concepts utilisés et explication de leurs utilités
  - Type de chiffrement
  - ...
- Documenter les tests. Qu'avez vous fait pour valider que l'application fonctionne ?
- Préparer une présentation pour expliquer le fonctionnement de l'application et les mesures de sécurité mises en place.

## Rendu attendu

- **Planning** complet et précis (outil au choix)
- **Repo github**
  - Le code de l'application à jour sur la branche principale
  - Documentation complète tel que décrite ci dessus sous forme d'un `readme.md` en **_Markdown_**
- **Présentation** pour l'oral (29 avril)

## Infos sur le déroulement du projet

Vous allez former des groupes de 3 ou 4 (3x4 et 2x3), il faudra vous **répartir le travail** et bien communiquer pour être efficace.

Je joue le role de _TechLead_ sur ce projet, le role d'un TechLead est d'**assister** et de **conseiller** les équipes dans leurs choix. Donc **n'hésitez pas à me demander des conseils** ou de l'aide sur certains sujets.

Nous avons seulement 5 séances (19h30) ensemble pour mener ce projet à terme. Il y a beaucoup à faire, **ne trainez pas**.

- 13 mars 4h
- 25 mars 4h
- 8 avril 4h
- 22 avril 7h30 (Rendu à 00h max)

### Oral du 29 avril

- 15min de présentation
- 20min de question environ

#### Points à aborder :

- Contexte du projet & équipe
- Planning
- Choix et conception
- Réalisation & difficultés rencontrés
- Tests réalisés
- Démonstration

## Conseils :

- **COMMUNIQUEZ** c'est la principale difficulté des travaux de groupe, vous devez savoir qui fait quoi et pourquoi
- Posez des questions et demandez de l'aide, je suis là pour ça.
- Utilisez toutes les ressources à votre dispositions.
- **Comprenez ce que vous faites** ! N'appliquez pas bêtement ce que chatGPT vous dit, demandez vous pourquoi faire comme ça et pas autrement
- Prenez le temps de faire un **repo git propre**. Mettre 1 mois de travail en commun à la dernière minute c'est foncer droit dans le mur.
- **Documentez vos choix** tout au long du projet.
