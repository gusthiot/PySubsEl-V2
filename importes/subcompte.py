from importes import SubFichier
from outils import Outils


class SubCompte(SubFichier):
    """
    Classe pour l'importation des données Comptes de Subsides
    """

    cles = ['id_compte', 'nature', 'type_compte', 'type_subside', 'intitule']
    nom_fichier = "cptesubside.csv"
    libelle = "Comptes Subsides"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ids = []

    def obtenir_ids(self):
        """
        retourne les ids de tous les comptes
        :return: ids de tous les comptes
        """
        if self.verifie_coherence == 0:
            info = self.libelle + ". vous devez vérifier la cohérence avant de pouvoir obtenir les ids"
            print(info)
            Outils.affiche_message(info)
            return []
        return self._ids

    def obtenir_id(self, nature, type_compte):
        """
        obtenir l'id subsides compte pour un type de compte et une nature client, s'il existe
        :param nature: nature client
        :param type_compte: type de compte
        :return: id subise compte s'il existe, ou None
        """
        if self.verifie_coherence == 0:
            info = self.libelle + ". vous devez vérifier la cohérence avant de pouvoir obtenir les ids"
            print(info)
            Outils.affiche_message(info)
            return None
        for k, v in self.donnees.items():
            if v['nature'] == nature and v['type_compte'] == type_compte:
                return k
        return None

    def est_coherent(self, subgeneraux):
        """
        vérifie que les données du fichier importé sont cohérentes 
        :param subgeneraux: paramètres généraux
        :return: 1 s'il y a une erreur, 0 sinon
        """

        if self.verifie_coherence == 1:
            print(self.libelle + ": cohérence déjà vérifiée")
            return 0

        msg = ""
        ligne = 1
        donnees_dict = {}

        for donnee in self.donnees:

            if donnee['id_compte'] == "":
                msg += "le compte id de la ligne " + str(ligne) + " ne peut être vide\n"
            elif donnee['id_compte'] not in self._ids:
                self._ids.append(donnee['id_compte'])
            else:
                msg += "le compte id '" + donnee['id_compte'] + "' de la ligne " + str(ligne) +\
                       " n'est pas unique\n"

            if donnee['nature'] == "":
                msg += "le nature de la ligne " + str(ligne) + " ne peut être vide\n"
            elif donnee['nature'] not in subgeneraux.obtenir_code_n():
                msg += "la nature '" + donnee['nature'] + "' de la ligne " + str(ligne) +\
                    " n'existe pas dans les types N\n"

            if donnee['type_subside'] == "":
                msg += "le type subside de la ligne " + str(ligne) + " ne peut être vide\n"
            elif donnee['type_subside'] not in subgeneraux.obtenir_code_t():
                msg += "le type subside '" + donnee['type_subside'] + "' de la ligne " + str(ligne) +\
                    " n'existe pas dans les types T3\n"

            donnees_dict[donnee['id_compte']] = donnee

            ligne += 1

        self.donnees = donnees_dict
        self.verifie_coherence = 1

        if msg != "":
            msg = self.libelle + "\n" + msg
            Outils.affiche_message(msg)
            return 1
        return 0
