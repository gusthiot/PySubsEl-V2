from outils import Outils


class BilanMensuel(object):
    """
    Classe pour la création du bilan mensuel
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

        nom = "bilan-subsides_" + str(subedition.annee_fin_general) + "_" + \
              Outils.mois_string(subedition.mois_fin_general) + ".csv"

        with dossier_destination.writer(nom) as fichier_writer:

            ligne = ["année", "mois", "code client", "code client sap", "abrév. labo", "nom labo", "type client",
                     "nature client", "Bonus", "Subsides MAt", "Subsides MOt"]
            for categorie in subgeneraux.codes_d3():
                ligne.append("Subsides " + categorie + "t")
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
            ligne = [subedition.annee_fin_general, subedition.mois_fin_general, code_client, client['sap'],
                     client['abrev'], client['nom'], client['type'], client['nature'], client['bonus'],
                     Outils.format_2_dec(client['subs_ma']), Outils.format_2_dec(client['subs_mo'])]
            for categorie in subgeneraux.codes_d3():
                ligne.append(Outils.format_2_dec(client['subs_' + categorie + 't']))
            ligne += [Outils.format_2_dec(client['subs'])]
            lignes.append(ligne)
        return lignes
