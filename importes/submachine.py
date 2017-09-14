from importes import SubFichier
from outils import Outils


class SubMachine(SubFichier):
    """
    Classe pour l'importation des données de Plafonds des Subsides Machines
    """

    cles = ['id_compte', 'ma_mois', 'ma_compte', 'mo_mois', 'mo_compte']
    nom_fichier = "plafmachine.csv"
    libelle = "Plafonds Subsides Machines"

    def est_coherent(self, subcomptes):
        """
        vérifie que les données du fichier importé sont cohérentes 
        :param subcomptes: comptes subsides importés
        :return: 1 s'il y a une erreur, 0 sinon
        """

        if self.verifie_coherence == 1:
            print(self.libelle + ": cohérence déjà vérifiée")
            return 0

        msg = ""
        ligne = 1
        donnees_dict = {}
        ids = []

        for donnee in self.donnees:

            if donnee['id_compte'] == "":
                msg += "le compte id de la ligne " + str(ligne) + " ne peut être vide\n"
            elif donnee['id_compte'] not in ids:
                ids.append(donnee['id_compte'])
            else:
                msg += "le compte id '" + donnee['id_compte'] + "' de la ligne " + str(ligne) +\
                       " n'est pas unique\n"

            if donnee['id_compte'] not in subcomptes.obtenir_ids():
                msg += "le compte id '" + donnee['id_compte'] + "' de la ligne " + str(ligne) +\
                       " n'est pas référencée dans les comptes subisdes\n"

            donnee['ma_mois'], info = Outils.est_un_nombre(donnee['ma_mois'], "le maximum ma mois", ligne)
            msg += info

            donnee['mo_mois'], info = Outils.est_un_nombre(donnee['mo_mois'], "le maximum mo mois", ligne)
            msg += info

            donnee['ma_compte'], info = Outils.est_un_nombre(donnee['ma_compte'], "le maximum ma compte", ligne)
            msg += info

            donnee['mo_compte'], info = Outils.est_un_nombre(donnee['mo_compte'], "le maximum mo compte", ligne)
            msg += info

            donnees_dict[donnee['id_compte']] = donnee

            ligne += 1

        for id_compte in subcomptes.obtenir_ids():
            if id_compte not in ids:
                msg += "Le compte id '" + id_compte + "' dans les comptes subsides n'est pas présente dans " \
                                               "les plafonds machines\n"

        self.donnees = donnees_dict
        self.verifie_coherence = 1

        if msg != "":
            msg = self.libelle + "\n" + msg
            Outils.affiche_message(msg)
            return 1
        return 0
