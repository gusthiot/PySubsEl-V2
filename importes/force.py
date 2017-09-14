from importes import SubFichier


class Force(SubFichier):
    """
    Classe pour l'importation des données Compts forcés
    """

    cles = ['id_compte', 'type_compte']
    nom_fichier = "forcecompte.csv"
    libelle = "Comptes Forcés"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._comptes = None

    def obtenir_comptes(self):
        """
        obtenir les comptes forcés et de leurs id subsides compte
        :return: comptes forcés
        """
        if not self._comptes:
            self._comptes = {}
            for donnee in self.donnees:
                self._comptes[donnee['id_compte']] = donnee['type_compte']
        return self._comptes
