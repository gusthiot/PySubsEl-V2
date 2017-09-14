from importes import SubFichier
from outils import Outils


class SubPrestation(SubFichier):
    """
    Classe pour l'importation des données de Plafonds des Subsides de Prestations
    """

    cles = ['id_compte', 'categorie', 'max_mois', 'max_compte']
    nom_fichier = "plafprestation.csv"
    libelle = "Plafonds Subsides Prestations"

    def est_coherent(self, subgeneraux, subcomptes):
        """
        vérifie que les données du fichier importé sont cohérentes 
        :param subgeneraux: paramètres généraux
        :param subcomptes: comptes subsides importés
        :return: 1 s'il y a une erreur, 0 sinon
        """

        if self.verifie_coherence == 1:
            print(self.libelle + ": cohérence déjà vérifiée")
            return 0

        msg = ""
        ligne = 1
        categories = []
        couples = []
        donnees_dict = {}

        for donnee in self.donnees:
            if donnee['id_compte'] not in subcomptes.obtenir_ids():
                msg += "le compte id '" + donnee['id_compte'] + "' de la ligne " + str(ligne) +\
                       " n'est pas référencée dans les comptes subisdes\n"

            if donnee['categorie'] == "":
                msg += "la catégorie de la ligne " + str(ligne) + " ne peut être vide\n"
            elif donnee['categorie'] not in subgeneraux.codes_d3():
                msg += "la catégorie '" + donnee['categorie'] + "' de la ligne " + str(ligne) +\
                       " n'existe pas dans les paramètres D3\n"
            elif donnee['categorie'] not in categories:
                categories.append(donnee['categorie'])

            if (donnee['categorie'] != "") and (donnee['id_compte'] != ""):
                couple = [donnee['categorie'], donnee['id_compte']]
                if couple not in couples:
                    couples.append(couple)
                else:
                    msg += "Couple categorie '" + donnee['categorie'] + "' et compte id '" + \
                           donnee['id_compte'] + "' de la ligne " + str(ligne) + " pas unique\n"

            donnee['max_mois'], info = Outils.est_un_nombre(donnee['max_mois'], "le maximum mois", ligne)
            msg += info

            donnee['max_compte'], info = Outils.est_un_nombre(donnee['max_compte'], "le maximum compte", ligne)
            msg += info

            donnees_dict[donnee['id_compte'] + donnee['categorie']] = donnee
            ligne += 1

        self.donnees = donnees_dict
        self.verifie_coherence = 1

        for categorie in subgeneraux.codes_d3():
            if categorie not in categories:
                msg += "La categorie D3 '" + categorie + "' dans les paramètres généraux n'est pas présente dans " \
                                                         "les plafonds de prestations\n"

        for categorie in categories:
            for id_compte in subcomptes.obtenir_ids():
                couple = [categorie, id_compte]
                if couple not in couples:
                    msg += "Couple categorie '" + categorie + "' et compte id '" + \
                           id_compte + "' n'existe pas\n"

        if msg != "":
            msg = self.libelle + "\n" + msg
            Outils.affiche_message(msg)
            return 1
        return 0
