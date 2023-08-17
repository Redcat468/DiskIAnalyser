# DiskIAnalyser
A simple python script to run on TrueNAS server and to analyse the SMART  disks reports via chatGPT;
Le but est d'utiliser l'API de ChatGPT 3.5 Turbo pour lire les rapports SMART de vos disques et de generer un rapport simplifié avec un score de santé de chaque disque. Le rapport est envoyé par mail une fois qu'il a été généré.
Ce script nécéssite l'installation du module openai, si vous ne souhaitez pas utiliser pip, vous pouvez faire comme ça : 

Télécharger le paquet:
Rendez-vous sur la page PyPI du module. Pour openai, l'URL est généralement la suivante :
https://pypi.org/project/openai/

Vous y trouverez des fichiers tar.gz pour différentes versions du module. Téléchargez le fichier .tar.gz qui correspond à la version que vous souhaitez.
Une fois le téléchargement terminé, transférez le fichier .tar.gz sur votre serveur TrueNAS (vous pouvez utiliser scp ou toute autre méthode de votre choix). Une fois le fichier sur le serveur, extrayez son contenu :

<code>tar -xzf openai-x.x.x.tar.gz</code>

Après avoir extrait le paquet, vous devez vous déplacer dans le répertoire du paquet et utiliser la commande setup.py pour installer le module :

<code>cd openai-x.x.x
python3 setup.py install</code>
