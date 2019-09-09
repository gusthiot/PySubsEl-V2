from outils import Outils


class BilanComptes(object):
    """
    Classe pour la création du bilan des comptes
    """

    @staticmethod
    def bilan(dossier_destination, subedition, subgeneraux, lignes):
        """
        création du bilan
        :param dossier_destination: Une instance de la classe dossier.DossierDestination
        :param subedition: paramètres d'édition
        :param subgeneraux: paramètres généraux
        :param lignes: lignes de données du bilan
        """
        nom = "bilan-subsides-comptes_" + str(subedition.annee_fin_general) + "_" + \
              Outils.mois_string(subedition.mois_fin_general) + ".csv"

        with dossier_destination.writer(nom) as fichier_writer:

            ligne = ["année", "mois", "code client", "code client sap", "abrév. labo", "nom labo", "type client",
                     "nature client", "id-compte", "numéro compte", "intitulé compte", "code type compte",
                     "code type subside", "Subsides MAj", "Subsides MOj"]
            for categorie in subgeneraux.codes_d3():
                ligne.append("Subsides " + categorie + "j")
            ligne += ["total Subsides"]
            fichier_writer.writerow(ligne)

            for ligne in lignes:
                fichier_writer.writerow(ligne)

    @staticmethod
    def creation_lignes(subedition, subgeneraux, consolidation):
        """
        génération des lignes de données du bilan
        :param subedition: paramètres d'édition
        :param subgeneraux: paramètres généraux
        :param consolidation: classe de consolidation des données des bilans
        :return: lignes de données du bilan
        """
        lignes = []
        for code_client, client in sorted(consolidation.clients.items()):

            numbers = {}
            for id_compte, compte in client['comptes'].items():
                numbers[id_compte] = compte['num_compte']

            for id_compte, num_compte in sorted(numbers.items(), key=lambda x: x[1]):
                compte = client['comptes'][id_compte]
                if compte['subs'] > 0:
                    ligne = [subedition.annee_fin_general, subedition.mois_fin_general, code_client, client['sap'],
                             client['abrev'], client['nom'], client['type'], client['nature'], id_compte,
                             num_compte, compte['intitule'], compte['type'], compte['t3'],
                             Outils.format_2_dec(compte['s-mat']), Outils.format_2_dec(compte['s-mot'])]
                    for categorie in subgeneraux.codes_d3():
                        ligne.append(Outils.format_2_dec(compte['s-' + categorie + 't']))
                    ligne += [Outils.format_2_dec(compte['subs'])]
                    lignes.append(ligne)
        return lignes
