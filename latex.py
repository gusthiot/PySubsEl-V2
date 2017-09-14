import re
import os
import shutil
import subprocess
from outils import Outils


class Latex(object):

    @classmethod
    def possibles(cls):
        return bool(shutil.which("pdflatex"))

    @staticmethod
    def echappe_caracteres(texte):
        """
        échappement des caractères qui peuvent poser problème dans les tableaux latex
        :param texte: texte à échapper
        :return: texte échappé
        """

        p = re.compile("[^ a-zA-Z0-9_'Éèéêëâàäïûùüçöô.:,;\-%#&$/|]")
        texte = p.sub('', texte)

        caracteres = ['%', '$', '_', '&', '#']
        latex_c = ['\%', '\$', '\_', '\&', '\#']
        for pos in range(0, len(caracteres)):
            texte = texte.replace(caracteres[pos], latex_c[pos])

        return texte

    @staticmethod
    def creer_latex_pdf(nom_fichier, contenu, nom_dossier=""):
        """
        création d'un pdf à partir d'un contenu latex
        :param nom_fichier: nom du pdf final
        :param contenu: contenu latex
        :param nom_dossier: nom du dossier dans lequel enregistrer le pdf
        """
        with open(nom_fichier + ".tex", 'w') as f:
            f.write(contenu)

        proc = subprocess.Popen(['pdflatex', nom_fichier + ".tex"])
        proc.communicate()

        # 2 fois pour que les longtable soient réguliers (courant de relancer latex)

        proc = subprocess.Popen(['pdflatex', nom_fichier + ".tex"])
        proc.communicate()

        os.unlink(nom_fichier + '.tex')
        os.unlink(nom_fichier + '.log')
        os.unlink(nom_fichier + '.aux')

        if nom_dossier != '':
            try:
                shutil.copy(nom_fichier + ".pdf", nom_dossier)
                os.unlink(nom_fichier + '.pdf')
            except IOError:
                Outils.affiche_message("Le pdf " + nom_fichier + " est resté ouvert et ne sera pas mis à jour")

    @staticmethod
    def long_tableau(contenu, structure, legende):
        """
        création d'un long tableau latex (peut s'étendre sur plusieurs pages)
        :param contenu: contenu du tableau
        :param structure: structure du tableau
        :param legende: légende du tabéeau
        :return: long tableau latex
        """
        return r'''
            {\tiny
            \begin{longtable}[c]
            ''' + structure + contenu + r'''
            \caption*{''' + legende + r'''}
            \end{longtable}}
            '''

    @staticmethod
    def tableau(contenu, structure, legende):
        """
        création d'un tableau latex
        :param contenu: contenu du tableau
        :param structure: structure du tableau
        :param legende: légende du tableau
        :return: tableau latex
        """
        return r'''
            \begin{table}[!ht]
            \tiny
            \centering
            \begin{tabular}''' + structure + contenu + r'''\end{tabular}
            \caption*{''' + legende + r'''}
            \end{table}
            '''

    @staticmethod
    def tableau_vide(legende):
        """
        création d'un tableau vide, juste pour avoir la légende formatée
        :param legende: légende du tableau vide
        :return: tableau avec juste la légende
        """
        return r'''
            \begin{table}[!ht]
            \tiny
            \centering
            \caption*{''' + legende + r'''}
            \end{table}
            '''

    @staticmethod
    def entete(plateforme):
        """
        création de l'entête de fichier latex en fonction de l'OS
        :param plateforme: OS utilisé
        :return: le contenu de l'entête
        """
        debut = r'''\documentclass[a4paper,10pt]{article}
            \usepackage[T1]{fontenc}
            \usepackage{lmodern}
            \usepackage[french]{babel}
            \usepackage{microtype}
            \DisableLigatures{encoding = *, family = * }
            '''
        if plateforme == "win32":
            debut += r'''
                \usepackage[cp1252]{inputenc}
                '''
        elif plateforme == "darwin":
            debut += r'''\usepackage[appelmac]{inputenc}'''
        else:
            debut += r'''\usepackage[utf8]{inputenc}'''
        return debut
