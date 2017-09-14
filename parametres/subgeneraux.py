from outils import Outils
from erreurs import ErreurConsistance
from collections import namedtuple

_champs_article = ["indice_d", "code_d", "intitule_long", "intitule_court"]
Article = namedtuple("Article", _champs_article)

_champs_article_t = ["indice_t", "code_t", "texte_t_long", "texte_t_court", "texte_t_ref"]
Article_t = namedtuple("Article_t", _champs_article_t)

class SubGeneraux(object):
    """
    Classe pour l'importation des paramètres généraux
    """

    nom_fichier = "s-paramgen.csv"
    libelle = "Paramètres Généraux"
    cles = ['financier', 'fonds', 'lien', 'lecture', 'sauvegarde', 'indice_t', 'code_t', 'texte_t_long',
            'texte_t_court', "texte_t_ref", 'code_n', 'indice_d', 'code_d', 'intitule_long', 'intitule_court']

    def __init__(self, dossier_source):
        """
        initialisation et importation des données

        :param dossier_source: Une instance de la classe dossier.DossierSource
        """
        self._donnees = {}
        try:
            for ligne in dossier_source.reader(self.nom_fichier):
                cle = ligne.pop(0)
                if cle not in self.cles:
                    Outils.fatal(ErreurConsistance(),
                                 "Clé inconnue dans %s: %s" % (self.nom_fichier, cle))
                while ligne[-1] == "":
                    del ligne[-1]
                self._donnees[cle] = ligne
        except IOError as e:
            Outils.fatal(e, "impossible d'ouvrir le fichier : "+SubGeneraux.nom_fichier)

        erreurs = ""
        for cle in self.cles:
            if cle not in self._donnees:
                erreurs += "\nClé manquante dans %s: %s" % (self.nom_fichier, cle)

        codes_n = []
        for nn in self._donnees['code_n'][1:]:
            if nn not in codes_n:
                codes_n.append(nn)
            else:
                erreurs += "le code N '" + nn + "' n'est pas unique\n"
        codes_t = []
        for tt in self._donnees['code_t'][1:]:
            if tt not in codes_t:
                codes_t.append(tt)
            else:
                erreurs += "le code T '" + tt + "' n'est pas unique\n"
        nb = 0
        self.avec_bonus = False
        for it in self._donnees['indice_t']:
            if it == '2':
                nb += 1
        if nb > 1:
            erreurs += "le code T2 doit être unique ou nul"
        if nb == 1:
            self.avec_bonus = True

        codes_d = []
        for dd in self._donnees['code_d'][1:]:
            if dd not in codes_d:
                codes_d.append(dd)
            else:
                erreurs += "le code D '" + dd + "' n'est pas unique\n"
        nb = 0
        for id in self._donnees['indice_d']:
            if id == '2':
                nb += 1
        if nb != 1:
            erreurs += "le code D2 doit être unique et exister"

        if (len(self._donnees['code_d']) != len(self._donnees['indice_d'])) or \
                (len(self._donnees['code_d']) != len(self._donnees['intitule_long'])) or \
                (len(self._donnees['code_d']) != len(self._donnees['intitule_court'])):
            erreurs += "le nombre de colonnes doit être le même pour le code D, l'indice D, l'intitulé long" \
                       " et l'intitulé court\n"

        if (len(self._donnees['code_t']) != len(self._donnees['indice_t'])) or \
                (len(self._donnees['code_t']) != len(self._donnees['texte_t_long'])) or \
                (len(self._donnees['code_t']) != len(self._donnees['texte_t_ref'])) or \
                (len(self._donnees['code_t']) != len(self._donnees['texte_t_court'])):
            erreurs += "le nombre de colonnes doit être le même pour le code T, l'indice T, le texte T long" \
                       ", le texte T court et le texte T ref\n"

        if erreurs != "":
            Outils.fatal(ErreurConsistance(), self.libelle + "\n" + erreurs)

    def obtenir_code_n(self):
        """
        retourne les codes N
        :return: codes N
        """
        return self._donnees['code_n'][1:]

    def obtenir_code_t(self):
        """
        retourne les codes T
        :return: codes T
        """
        return self._donnees['code_t'][1:]

    @property
    def articles(self):
        """renvoie la liste des articles de facturation.

        :return: une liste ordonnée d'objets Article
        """
        if not hasattr(self, "_articles"):
            self._articles = []
            for i in range(1, len(self._donnees['code_d'])):
                kw = dict((k, self._donnees[k][i]) for k in _champs_article)
                self._articles.append(Article(**kw))
        return self._articles

    @property
    def articles_t(self):
        """renvoie la liste des types de subsides.

        :return: une liste ordonnée d'objets Article
        """
        if not hasattr(self, "_articles_t"):
            self._articles_t = []
            for i in range(1, len(self._donnees['code_t'])):
                kw = dict((k, self._donnees[k][i]) for k in _champs_article_t)
                self._articles_t.append(Article_t(**kw))
        return self._articles_t

    @property
    def articles_d3(self):
        """
        retourne uniquement les articles D3

        :return: une liste ordonnée d'objets Article
        """
        articles_d3 = []
        for a in self.articles:
            if a.indice_d == '3':
                articles_d3.append(a)
        return articles_d3

    def codes_d3(self):
        return [a.code_d for a in self.articles_d3]

    @property
    def articles_t3(self):
        """
        retourne uniquement les articles T3

        :return: une liste ordonnée d'objets Article
        """
        articles_t3 = []
        for a in self.articles_t:
            if a.indice_t == '3':
                articles_t3.append(a)
        return articles_t3

    def article_t(self, code):
        """
        retourne l'article T pour le code donné

        :return: un objet Article or None
        """
        for a in self.articles_t:
            if a.code_t == code:
                return a
        return None

    def article_t_indice(self, indice):
        """
        retourne l'article T pour l'indice donné

        :return: un objet Article or None
        """
        for a in self.articles_t:
            if a.indice_t == indice:
                return a
        return None

    def codes_t3(self):
        return [a.code_t for a in self.articles_t3]


def ajoute_accesseur_pour_valeur_unique(cls, nom, cle_csv=None):
    if cle_csv is None:
        cle_csv = nom

    def accesseur(self):
        return self._donnees[cle_csv][1]
    setattr(cls, nom, property(accesseur))

ajoute_accesseur_pour_valeur_unique(SubGeneraux, "financier")

for champ_valeur_unique in ('fonds', 'lien', 'lecture', 'sauvegarde'):
    ajoute_accesseur_pour_valeur_unique(SubGeneraux, champ_valeur_unique)
