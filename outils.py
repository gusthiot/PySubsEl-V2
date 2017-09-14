from tkinter.filedialog import *
from tkinter.scrolledtext import *

import shutil
import errno
import os
import platform

from erreurs import ErreurConsistance


class Outils(object):
    """
    Classe contenant diverses méthodes utiles
    """
    if platform.system() in ['Linux', 'Darwin']:
        _interface_graphique = len(os.environ.get('DISPLAY', '')) > 0
    else:
        _interface_graphique = True

    @classmethod
    def interface_graphique(cls, opt_nouvelle_valeur=None):
        """
        enregistre que l'on veut l'interface graphique ou non
        :param opt_nouvelle_valeur: True ou False pour interface graphique
        :return: valeur enregistrée
        """
        if opt_nouvelle_valeur is not None:
            cls._interface_graphique = opt_nouvelle_valeur
        return cls._interface_graphique

    @classmethod
    def affiche_message(cls, message):
        """
        affiche une petite boite de dialogue avec un message et un bouton OK
        :param message: message à afficher
        """
        if cls.interface_graphique():
            fenetre = Tk()
            fenetre.title("Message")
            texte = ScrolledText(fenetre)
            texte.insert(END, message)
            texte.pack()
            button = Button(fenetre, text='OK', command=fenetre.destroy)
            button.pack()
            mainloop()
        else:
            print(message)

    @classmethod
    def fatal(cls, exn, message):
        """
        affiche erreur fatal
        :param exn: erreur
        :param message: message à afficher
        """
        Outils.affiche_message(message + "\n" + str(exn))
        if isinstance(exn, ErreurConsistance) or isinstance(exn, ValueError):
            sys.exit(1)
        else:
            sys.exit(4)            

    @staticmethod
    def copier_dossier(source, dossier, destination):
        """
        copier un dossier
        :param source: chemin du dossier à copier
        :param dossier: dossier à copier
        :param destination: chemin de destination de copie
        """
        chemin = destination + "/" + dossier
        if not os.path.exists(chemin):
            try:
                shutil.copytree(source + dossier, chemin)
            except OSError as exc:
                if exc.errno == errno.ENOTDIR:
                    shutil.copy(source, destination)

    if platform.system() in ['Linux', 'Darwin']:
        _interface_graphique = len(os.environ.get('DISPLAY', '')) > 0
    else:
        _interface_graphique = True

    @staticmethod
    def choisir_dossier(plateforme):
        """
        affiche une interface permettant de choisir un dossier
        :param plateforme: OS utilisé
        :return: la position du dossier sélectionné
        """
        fenetre = Tk()
        fenetre.title("Choix du dossier")
        dossier = askdirectory(parent=fenetre, initialdir="/",
                               title='Choisissez un dossier de travail')
        fenetre.destroy()
        if dossier == "":
            Outils.affiche_message("Aucun dossier choisi")
            sys.exit("Aucun dossier choisi")
        return dossier + Outils.separateur_os(plateforme)

    @staticmethod
    def mois_string(mois):
        """
        prend un mois comme nombre, et le retourne comme string, avec un '0' devant si plus petit que 10
        :param mois: mois formaté en nombre
        :return: mois formaté en string
        """
        if mois < 10:
            return "0" + str(mois)
        else:
            return str(mois)

    @staticmethod
    def mois_nom(mois):
        """
        retourne le nom du mois en question
        :param mois: mois formaté en nombre
        :return: nom du mois
        """
        mois_fr = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre",
                   "novembre", "décembre"]
        return mois_fr[mois-1]

    @staticmethod
    def separateur_os(plateforme):
        """
        retourne le séparateur de chemin logique en fonction de l'OS (si windows ou pas)
        :param plateforme: OS utilisé
        :return: séparateur, string
        """
        if plateforme == "win32":
            return "\\"
        else:
            return "/"

    @staticmethod
    def separateur_lien(texte, generaux):
        """
        remplace le séparateur de chemin logique en fonction du lien donné dans les paramètres généraux
        :param texte: texte à traiter
        :param generaux: paramètres généraux
        :return: séparateur, string
        """
        if "\\" in generaux.lien:
            if "/" in generaux.lien:
                Outils.affiche_message("'/' et '\\' présents dans le lien des paramètres généraux !!! ")
            texte = texte.replace("/", "\\")
        else:
            texte = texte.replace("\\", "/")
        return texte.replace("//", "/").replace("\\" + "\\", "\\")

    @staticmethod
    def separateur_dossier(texte, generaux):
        """
        remplace le séparateur de chemin logique en fonction du chemin donné dans les paramètres généraux
        :param texte: texte à traiter
        :param generaux: paramètres généraux
        :return: séparateur, string
        """
        if "\\" in generaux.sauvegarde:
            if "/" in generaux.sauvegarde:
                Outils.affiche_message("'/' et '\\' présents dans le lien des paramètres généraux !!! ")
            texte = texte.replace("/", "\\")
            """
            if "\\" != Outils.separateur_os(plateforme):
                Outils.affiche_message_conditionnel("Le chemin d'enregistrement n'utilise pas le même séparateur que "
                                                    "l'os sur lequel tourne le logiciel. Voulez-vous tout de même "
                                                    "continuer ?")
            """
        else:
            texte = texte.replace("\\", "/")
            """
            if "/" != Outils.separateur_os(plateforme):
                Outils.affiche_message_conditionnel("Le chemin d'enregistrement n'utilise pas le même séparateur que "
                                                    "l'os sur lequel tourne le logiciel. Voulez-vous tout de même "
                                                    "continuer ?")
            """
        return texte.replace("//", "/").replace("\\" + "\\", "\\")

    @staticmethod
    def eliminer_double_separateur(texte):
        """
        élimine les doubles (back)slashs
        :param texte: texte à nettoyer
        :return: texte nettoyé
        """
        return texte.replace("//", "/").replace("\\" + "\\", "\\")

    @staticmethod
    def chemin(structure, plateforme, generaux=None):
        """
        construit le chemin pour dossier/fichier
        :param structure: éléments du chemin
        :param plateforme:OS utilisé
        :param generaux: paramètres généraux
        :return: chemin logique complet pour dossier/fichier
        """
        chemin = ""
        first = True
        for element in structure:
            if not first:
                chemin += Outils.separateur_os(plateforme)
            else:
                first = False
            chemin += str(element)
        if generaux is None:
            return Outils.eliminer_double_separateur(chemin)
        else:
            return Outils.eliminer_double_separateur(Outils.separateur_dossier(chemin, generaux))

    @staticmethod
    def existe(chemin, creation=False):
        """
        vérifie si le dossier/fichier existe
        :param chemin: chemin du dossier/fichier
        :param creation: création de l'oobjet s'il n'existe pas
        :return: True si le dossier/fichier existe, False sinon
        """
        existe = True
        if not os.path.exists(chemin):
            existe = False
            if creation:
                os.makedirs(chemin)
        return existe

    @staticmethod
    def lien_dossier(structure, plateforme, generaux):
        """
        construit le chemin pour enregistrer les données sans vérifier son existence
        :param structure: éléments du chemin
        :param plateforme: OS utilisé
        :param generaux: paramètres généraux
        :return:chemin logique complet pour dossier
        """
        chemin = ""
        for element in structure:
            chemin += str(element) + Outils.separateur_os(plateforme)
        return Outils.eliminer_double_separateur(Outils.separateur_lien(chemin, generaux))

    @staticmethod
    def format_2_dec(nombre):
        """
        affiche un nombre en float arrondi avec 2 chiffres après la virgule
        :param nombre: nombre à afficher
        :return: nombre arrondi, avec 2 chiffres après la virgule, en string
        """
        try:
            float(nombre)
            return "%.2f" % round(nombre, 2)
        except ValueError:
            return "pas un nombre"

    @staticmethod
    def est_un_nombre(donnee, colonne, ligne):
        """
        vérifie que la donnée est bien un nombre
        :param donnee: donnée à vérifier
        :param colonne: colonne contenant la donnée
        :param ligne: ligne contenant la donnée
        :return: la donnée formatée en nombre et un string vide si ok, 0 et un message d'erreur sinon
        """
        try:
            fl_d = float(donnee)
            return fl_d, ""
        except ValueError:
            return 0, colonne + " de la ligne " + str(ligne) + " doit être un nombre\n"

    @staticmethod
    def comparaison_date(annee_1, mois_1, annee_2, mois_2):
        """
        compare 2 dates pour savoir la plus récente
        :param annee_1: année date 1
        :param mois_1:  mois date 1
        :param annee_2: année date 2
        :param mois_2: mois date 2
        :return: 1 si date 1 plus récente, 0 si même date, -1 si date 1 plus ancienne
        """
        date_1 = annee_1 * 100 + mois_1
        date_2 = annee_2 * 100 + mois_2
        if date_1 > date_2:
            return 1
        elif date_1 == date_2:
            return 0
        else:
            return -1
