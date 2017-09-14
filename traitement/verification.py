
class Verification(object):
    """
    Classe servant à vérifier les dates et la cohérence de toutes les données importées
    """

    def __init__(self):
        """
        initialisation
        """
        self.a_verifier = 2

    def verification_date(self, bilans):
        """
        vérifie les dates de tous les bilans importés
        :param bilans: bilans importés
        :return: 0 si ok, sinon le nombre d'échecs à la vérification
        """
        verif = 0
        for bilan in bilans:
            verif += bilan.verification_date()
        self.a_verifier = 1
        return verif

    def verification_coherence(self, subgeneraux, subedition, subcomptes, submachines, subprestations, bilans,
                               consolidation, force):
        """
        vérifie la cohérence des données importées
        :param subgeneraux: paramètres généraux
        :param subedition: paramètres d'édition
        :param subcomptes: comptes subsides importés
        :param submachines: plafonds machines importées
        :param subprestations: plafonds prestations importées
        :param bilans: bilans importés
        :param consolidation: classe de consolidation des données des bilans
        :param force: comptes forcés importés
        :return: 0 si ok, sinon le nombre d'échecs à la vérification
        """
        verif = 0

        verif += subcomptes.est_coherent(subgeneraux)
        verif += submachines.est_coherent(subcomptes)
        verif += subprestations.est_coherent(subgeneraux, subcomptes)
        verif += consolidation.coherence_bilans(bilans, subcomptes, subgeneraux, subedition, force)
        self.a_verifier = 0
        return verif
