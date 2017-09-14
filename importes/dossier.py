import csv
import os
from contextlib import contextmanager

"""Dossiers source et destination abstraits.

Les instances des classes DossierSource et DossierDestination
encapsulent tout ce qui est nécessaire pour lire resp. écrire un
fichier sous l'un des formats gérés par l'application (CSV, texte ou
binaire). Cela comprend le chemin d'accès (de sorte que le code
utilisateur n'a a connaître que des chemins relatifs), mais aussi les
paramètres plateforme-spécifiques d'encodage, séparateurs CSV etc.
"""


class _DossierBase(object):
    def __init__(self, chemin_dossier, encodage="cp1252", delimiteur=";"):
        """
        initialisation de l'objet

        :param chemin_dossier: Chemin du dossier
        :param delimiteur: code délimiteur des champs dans les fichier csv
        :param encodage: encodage des fichiers texte (CSV ou HTML)
        """
        self.chemin = chemin_dossier
        self.delimiteur = delimiteur
        self.quotechar = "|"
        self.encodage = encodage

    def _open(self, chemin_relatif, flags):
        return open(self._chemin(chemin_relatif), flags,
                    newline=None if 'b' in flags else '',
                    encoding=None if 'b' in flags else self.encodage)

    def _chemin(self, chemin_relatif):
        return os.path.join(self.chemin, chemin_relatif)

    def existe(self, chemin_relatif):
        return os.path.exists(self._chemin(chemin_relatif))


class DossierSource(_DossierBase):
    """
    Source de données.

    Une instance représente un répertoire de données source avec tous les réglages
    idoines du parseur (délimiteur, format de caractères). La méthode reader()
    permet d'ouvrir un CSV par nom relatif.
    """
    def reader(self, chemin_relatif):
        return csv.reader(self._open(chemin_relatif, "r"), delimiter=self.delimiteur,
                          quotechar=self.quotechar)

    def dict_reader(self, chemin_relatif):
        return csv.DictReader(self._open(chemin_relatif, "r"), delimiter=self.delimiteur, quotechar=self.quotechar)

    def string_lire(self, chemin_relatif):
        return self._open(chemin_relatif, "r").read()

    def lire(self, chemin_relatif):
        """Renvoie le contenu d'un fichier, en binaire."""
        return self._open(chemin_relatif, "rb").read()


class DossierDestination(_DossierBase):
    """Destination de données.

    Une instance représente un répertoire de données de destination
    avec tous les réglages idoines (délimiteur CSV, format de
    caractères). La méthode open() permet de créer un fichier par nom
    relatif. La méthode csv_writer() fait de même, mais avec un objet
    csv.writer plutôt qu'un descripteur de fichier.
    """

    @contextmanager
    def open(self, chemin_relatif):
        with self._open(chemin_relatif, "w") as fichier:
            yield fichier

    @contextmanager
    def writer(self, chemin_relatif):
        with self._open(chemin_relatif, "w") as csv_fichier:
            yield csv.writer(csv_fichier, delimiter=self.delimiteur,
                             quotechar=self.quotechar)

    def string_ecrire(self, chemin_relatif, texte):
        with self._open(chemin_relatif, "w") as fd:
            fd.write(texte)

    def ecrire(self, chemin_relatif, binaire):
        """Écrit un fichier, en binaire."""
        with self._open(chemin_relatif, "wb") as fd:
            fd.write(binaire)
