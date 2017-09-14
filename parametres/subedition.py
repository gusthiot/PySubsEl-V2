from outils import Outils
from erreurs import ErreurConsistance


class SubEdition(object):
    """
    Classe pour l'importation des paramètres d'édition des Subsides
    """

    nom_fichier = "s-paramedit.csv"
    libelle = "Paramètres d'Edition des Subsides"

    def __init__(self, dossier_source):
        """
        initialisation et importation des données

        :param dossier_source: Une instance de la classe dossier.DossierSource
        """
        donnees_csv = []
        try:
            for ligne in dossier_source.reader(self.nom_fichier):
                donnees_csv.append(ligne)
        except IOError as e:
            Outils.fatal(e, "impossible d'ouvrir le fichier : " + SubEdition.nom_fichier)

        num = 5
        if len(donnees_csv) != num:
            Outils.fatal(ErreurConsistance(),
                         SubEdition.libelle + ": nombre de lignes incorrect : " +
                         str(len(donnees_csv)) + ", attendu : " + str(num))
        if len(donnees_csv[0]) != 3 or len(donnees_csv[1]) != 3 or len(donnees_csv[2]) != 3 or len(donnees_csv[3]) != 3:
            Outils.fatal(ErreurConsistance(), SubEdition.libelle + ": nombre de colonnes incorrect")
        try:
            self.annee_debut_bonus = int(donnees_csv[0][1])
            self.mois_debut_bonus = int(donnees_csv[0][2])
            self.annee_fin_bonus = int(donnees_csv[1][1])
            self.mois_fin_bonus = int(donnees_csv[1][2])

            self.annee_debut_subs = int(donnees_csv[2][1])
            self.mois_debut_subs = int(donnees_csv[2][2])
            self.annee_fin_subs = int(donnees_csv[3][1])
            self.mois_fin_subs = int(donnees_csv[3][2])
        except ValueError as e:
            Outils.fatal(e, SubEdition.libelle + "\nles mois et les années doivent être des nombres entiers")

        if Outils.comparaison_date(self.annee_debut_bonus, self.mois_debut_bonus,
                                   self.annee_fin_bonus, self.mois_fin_bonus) > 0:
            Outils.fatal(ErreurConsistance(), SubEdition.libelle + ": la fin du bonus ne peut être avant le début")
        if Outils.comparaison_date(self.annee_debut_subs, self.mois_debut_subs,
                                   self.annee_fin_subs, self.mois_fin_subs) > 0:
            Outils.fatal(ErreurConsistance(), SubEdition.libelle + ": la fin des subsides ne peut être avant le début")

        if Outils.comparaison_date(self.annee_debut_bonus, self.mois_debut_bonus,
                                   self.annee_debut_subs, self.mois_debut_subs) < 0:
            self.annee_debut_general = self.annee_debut_bonus
            self.mois_debut_general = self.mois_debut_bonus
        else:
            self.annee_debut_general = self.annee_debut_subs
            self.mois_debut_general = self.mois_debut_subs

        if Outils.comparaison_date(self.annee_fin_bonus, self.mois_fin_bonus,
                                   self.annee_fin_subs, self.mois_fin_subs) > 0:
            self.annee_fin_general = self.annee_fin_bonus
            self.mois_fin_general = self.mois_fin_bonus
        else:
            self.annee_fin_general = self.annee_fin_subs
            self.mois_fin_general = self.mois_fin_subs

        self.filigrane = donnees_csv[4][1]
