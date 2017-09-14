# PySubsEl-V2

- installer Python 3 (https://www.python.org/downloads/)
    si l'option "rajouter Python au PATH" se présente, la cocher
- installer TeX Live (https://www.tug.org/texlive/)
- dans une fenêtre de commande ou un terminal, taper<pre>
  pip install -r requirements.txt</pre>
- lancer main.py et choisir un dossier de travail qui contient des csv de données brutes

- si la fabrication de pdf avec tex live ne fonctionne pas, ouvrir une console de commande et taper 'fmtutil --sys --all'

Le dossier 'importes' contient les classes servant à l'importation des données contenues dans les csv et au traitement 
de base de ces données

Le dossier 'paramètres' contient les classes servant à l'importation des paramètres d'édition et des paramètres généraux

Le dossier 'traitement' contient les classes servant à la fabrication des annexes et des bilans

Le dossier de travail doit contenir les fichiers suivants (noms modifiables dans le code au besoin) :

    - cptesubside.csv 
    - plafmachine.csv
    - plafprestation.csv
    - s-paramedit.csv
    - s-paramgen.csv
    - forcecompte.csv (facultatif)
    - ainsi que les bilan-comptes_aaa_mm.csv nécessaires
