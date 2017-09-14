from outils import Outils


class Bilan(object):

    def __init__(self, dossier_source, nom_fichier, annee, mois):
        """
        initialisation et importation des données

        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param nom_fichier: nom du fichier à importer
        :param annee: année selon paramètres d'édition
        :param mois: mois selon paramètres d'édition
        """
        self.nom = nom_fichier
        self.mois = mois
        self.annee = annee
        try:
            fichier_reader = dossier_source.reader(nom_fichier)
            donnees_csv = []
            for ligne in fichier_reader:
                donnees_csv.append(ligne)
            self.cles = {}
            i = 0
            for cle in donnees_csv[0]:
                self.cles[cle] = i
                i += 1
            self.donnees = donnees_csv[1:]
            self.verifie_date = 0
        except IOError as e:
            Outils.fatal(e, "impossible d'ouvrir le fichier : "+nom_fichier)

    def verification_date(self):
        """
        vérifie que le mois et l'année présents sur la ligne sont bien ceux espérés
        :return: 0 si ok, 1 sinon
        """
        if self.verifie_date == 1:
            print(self.nom + ": date déjà vérifiée")
            return 0

        msg = ""
        position = 1
        for donnee in self.donnees:
            try:
                if int(donnee[self.cles['mois']]) != self.mois or int(donnee[self.cles['année']]) != self.annee:
                    msg += "date incorrect ligne " + str(position) + "\n"
            except ValueError:
                msg += "année ou mois n'est pas valable" + str(position) + "\n"
            position += 1

        # del self.donnees[0]
        self.verifie_date = 1

        if msg != "":
            # msg = self.nom + "\n" + msg
            msg = "L’année et le mois ne correspondent pas à ceux attendus dans " + self.nom
            Outils.affiche_message(msg)
            return 1
        return 0
