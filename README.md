# EVALUATION IG DATA

[![forthebadge](http://forthebadge.com/images/badges/built-with-love.svg)](http://forthebadge.com)  [![forthebadge](http://forthebadge.com/images/badges/powered-by-electricity.svg)](http://forthebadge.com)

Le sujet concerne l'analyse d'un dataset contenant des informations sur des produits Amazon au Canada. Le dataset comprend des colonnes telles que l'ID du produit, le titre, l'URL de l'image, la note du produit, le nombre de revues, le prix, le prix original, la catégorie, et si le produit est un best-seller ou non ainsi que le nombre d'acaht du produit dans le mois.

Les compétences évaluées incluent la capacité à utiliser les technologies fournies pour le traitement et le stockage des données, ainsi que l'analyse créative des données en fonction des critères fournis.

## Pour commencer

Avant de débuter le projet il faut s'assurer d'avoir les bons outils et les bonnes versions.

### Pré-requis

Pré-requis d'user session à utiliser sur la machine virtuelle : Hadoop avec le mot de passe hadoop.

Les prérequis sont d'outils sont :

- hadoop 3.3.6 
- airflow 2.8.0 
- pyspark 3.3.4 
- python 3.10.12
- openjdk 11.0.21

Les prérequis de librairies python sont (à installer avec pip) :

- kaggle


### Installation

Veuillez a bien suivre les étapes d'installation si votre version n'est pas la bonne:

hadoop 3.3.6 airflow 2.8.0 pyspark 3.3.4 python 3.10.12

***Python - Optionnel(n'est pas recommandé aux débutants, tester avec votre version python sinon cahnger la version de python a 3.10.12) :***
- wget https://www.python.org/ftp/python/3.10.12/Python-3.10.12.tgz
- tar xzf Python-3.10.12.tgz
- cd Python-3.10.12
- ./configure --enable-optimizations
- make
- sudo make altinstall

***Airflow :***
- pip uninstall apache-airflow
- pip install apache-airflow==2.8.0
- pip install Flask-Session==0.5.0 (**IMPORTANT: UNE ERREUR SURVIENT AVEC FLASK VERSION 0.6.0 VEUILLEZ A BIEN EXECUTER CETTE COMMANDE APRES L'INSTALLATION D'AIRFLOW**)

***Pyspark :***
- pip uninstall pyspark
- pip install pyspark==3.3.4

***Hadoop :***
- sudo rm -rf /usr/local/hadoop
- wget https://archive.apache.org/dist/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
- tar -xzvf hadoop-3.3.6.tar.gz
- sudo mv hadoop-3.3.6 /usr/local/

***Spark :***
- sudo rm -rf /usr/local/spark
- wget https://archive.apache.org/dist/spark/spark-3.3.4/spark-3.3.4-bin-hadoop3.tgz
- tar -xzvf spark-3.3.4-bin-hadoop3.tgz
- sudo mv spark-3.3.4-bin-hadoop3 /usr/local/spark

Apres les installation voici quelque étapes à suivre:


***Important -> export path for hadoop:***
- nano ~/.bashrc
- export PATH=$PATH:/home/hadoop/.local/bin (**Modifiez le nom de votre session si ce n'est pas hadoop, CTRL+X et ENTRER**)
- source ~/.bashrc
- Redemarer le terminal


***Airflow setup :***
- airflow db init
- airflow users create \
  --username admin \
  --firstname fname \
  --lastname lname \
  --role Admin \
  --email test@gmail.com
- pass example :123456


***Airflow start :***
- airflow webserver
- airflow scheduler


***HDFS start :***
- start-dfs.sh
- start-yarn.sh

***kaggle lib install :***
- pip install kaggle


## Démarrage

Je conseille de démarrer le projet sur la session hadoop car c'est la que je l'ai développé et testé.

Pour démarrer le projet il faut d'abord:
- Créer un dossier /home/hadoop/Bureau/ECBD ou bien extraire mon dossier projet sur le bureau avec le nom du dossier "ECBD"
- Faire le HDFS start
- Modifier le airflow.cfg pour pointer vers mon dossier dags du projet exemple pour moi : dags_folder = /home/hadoop/Bureau/ECBD/dags
- Faire le Airflow start
- Dépondant de votre session il faudra sois move mes credetials d'api kaggle qui sont dasn mon dossier projet/data soit en faire pour vous et deplacer le kaggle.json vers /home/hadoop/.kaggle/ (modifier hadoop si ce n'est pas votre session)
- Ensuite quand c'est fait vous pouvez vous connecter sur airflow et lancer manuellement (ou bien attendre l'interval d'un an, oui ç fait beaucoup mais le data sur kaggle se met a jour tous les ans malheureusement) le dag1 qui va automatiquement trigger les autres dags si il est en succes.

## Fabriqué avec

Entrez les programmes/logiciels/ressources que vous avez utilisé pour développer votre projet

_exemples :_
* [Materialize.css](http://materializecss.com) - Framework CSS (front-end)
* [Atom](https://atom.io/) - Editeur de textes

## Contributing

Pas de contribution , c'est un projet d'évaluation donc qui ne sera pas mis à jour dans le temps.

## Versions
- hadoop 3.3.6 
- airflow 2.8.0 
- pyspark 3.3.4 
- spark 3.3.4
- python 3.10.12
- openjdk 11.0.21

## Auteurs
Je suis, moi, Kayumars LOWY-NEKRUZ le seul auteur de ce chef d'oeuvre, retrouvez moi sur https://github.com/knekruz/

## License

Ce projet est sous licence ``EVALUATION TRES LONGUE ET PAS EVIDENTE``


