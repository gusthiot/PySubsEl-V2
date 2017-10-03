# from latex import Latex
from outils import Outils


class Virement(object):
    """
    Classe contenant les méthodes nécessaires à la génération des virements
    """

    @staticmethod
    def virements(consolidation, destination, subedition, subgeneraux, annexes):
        """
        génère les virements sous forme de csv
        
        :param consolidation: classe de consolidation des données des bilans
        :param destination: Une instance de la classe dossier.DossierDestination
        :param subedition: paramètres d'édition
        :param subgeneraux: paramètres généraux
        :param annexes: dossier contenant les annexes
        """

        nom = "subsides_" + str(subedition.annee_fin_general) + "_" + \
              Outils.mois_string(subedition.mois_fin_general) + ".csv"
        with destination.writer(nom) as fichier_writer:
            fichier_writer.writerow(["Référence (XBLNR)", "Texte d'entête (BKTXT)", "Code à barres (BARCODE)",
                                     "Montant (DMBTR)", "Clé compta au débit", "Compte au débit", "Fonds au débit",
                                     "Code opération au débit", "Centre de coût au débit", "Centre financier au débit",
                                     "Code TVA au débit", "Texte du poste au débit", "Clé compta au crédit",
                                     "Compte au crédit", "Fonds au crédit", "Code opération au crédit",
                                     "Centre de coût au crédit", "Centre financier au crédit", "Code TVA au crédit",
                                     "Texte du poste au crédit", "Code Client SAP (Crédit)"])

            combo_list = {}

            for code_client, dcl in consolidation.clients.items():

                reference = "SUBS" + str(subedition.annee_fin_general)[2:] + \
                            Outils.mois_string(subedition.mois_fin_general) + "." + code_client
                base = dcl['nature'] + str(subedition.annee_fin_general)[2:] + \
                       Outils.mois_string(subedition.mois_fin_general)

                nom_annexe = "subside_" + str(subedition.annee_fin_general) + "_" + \
                             Outils.mois_string(subedition.mois_fin_general) + "_" + code_client + ".pdf"
                dossier_annexe = annexes + "/" + nom_annexe

                debut = "Début de période : " + Outils.mois_string(subedition.mois_debut_general) + "/" + \
                        str(subedition.annee_debut_general)
                fin = "Fin de période : " + Outils.mois_string(subedition.mois_fin_general) + "/" + \
                      str(subedition.annee_fin_general)
                dico_contenu = {'code': code_client, 'abrev': dcl['abrev'], 'sap': dcl['sap'],
                                'nom': dcl['nom'], 'ref': reference, 'debut': debut, 'fin': fin}
                contenu_client = r'''<section id="%(code)s"><div id="entete"> %(code)s <br />
                    %(sap)s <br />
                    %(abrev)s <br />
                    %(nom)s <br />
                    </div><br />
                    %(ref)s <br /><br />
                    %(debut)s <br />
                    %(fin)s <br />
                    ''' % dico_contenu

                contenu_client += r'''<table id="tableau">
                    <tr>
                    <td>Code OP </td><td> Poste </td><td> Prestation </td><td> Montant </td>
                    </tr>
                    '''

                if dcl['bonus'] > 0:
                    texte = subgeneraux.article_t_indice('2').texte_t_court + " / " + \
                            subgeneraux.articles[0].intitule_court
                    op = subgeneraux.article_t_indice('2').code_t + base + subgeneraux.articles[0].code_d
                    t_ref = subgeneraux.article_t_indice('2').texte_t_ref

                    fichier_writer.writerow([t_ref, reference, "", "%.2f" % dcl['bonus'], "", "",
                                             subgeneraux.fonds, op, "", "", "", dcl['abrev'] + " : " + texte, "", "",
                                             "", "", "", "", "", "CMi : " + texte, dcl['sap']])

                    poste = subgeneraux.article_t_indice('2').texte_t_long
                    prestation = subgeneraux.articles[0].intitule_long
                    contenu_client += Virement.ligne_tableau(op, poste, prestation, dcl['bonus'])

                for t3, client_t3 in sorted(dcl['codes'].items()):
                    op = t3 + base + subgeneraux.articles[0].code_d
                    texte = subgeneraux.article_t(t3).texte_t_court + " / " + subgeneraux.articles[0].intitule_court
                    t_ref = subgeneraux.article_t(t3).texte_t_ref

                    fichier_writer.writerow([t_ref, reference, "", "%.2f" % client_t3['sm'], "", "",
                                             subgeneraux.fonds, op, "", "", "", dcl['abrev'] + " : " + texte, "", "",
                                             "", "", "", "", "", "CMi : " + texte, dcl['sap']])

                    poste = subgeneraux.article_t(t3).texte_t_long
                    prestation = subgeneraux.articles[0].intitule_long
                    contenu_client += Virement.ligne_tableau(op, poste, prestation, client_t3['sm'])

                    for article in subgeneraux.articles_d3:
                        if client_t3['s' + article.code_d] > 0:
                            op = t3 + base + article.code_d
                            texte = subgeneraux.article_t(t3).texte_t_court + " / " + article.intitule_court

                            fichier_writer.writerow([t_ref, reference, "", "%.2f" % client_t3['s' + article.code_d],
                                                     "", "", subgeneraux.fonds, op, "", "", "",
                                                     dcl['abrev'] + " : " + texte, "", "", "", "", "", "", "",
                                                     "CMi : " + texte, dcl['sap']])

                            poste = subgeneraux.article_t(t3).texte_t_long
                            prestation = article.intitule_long
                            contenu_client += Virement.ligne_tableau(op, poste, prestation,
                                                                     client_t3['s' + article.code_d])

                contenu_client += r'''
                    <tr><td colspan="3" id="toright">TOTAL </td><td id="toright">
                    ''' + "%.2f" % (dcl['subs'] + dcl['bonus']) + r'''</td></tr>
                    </table>
                    '''
                contenu_client += r'''<table><tr><td><a href="''' + dossier_annexe + r'''" target="new">
                    ''' + nom_annexe + r'''</a></td></tr></table>'''
                contenu_client += "</section>"

                combo_list[dcl['abrev'] + " (" + code_client + ")"] = contenu_client

            Virement.creer_html(destination, combo_list, subedition)

    @staticmethod
    def ligne_tableau(op, poste, prestation, montant):
        """
        retourne une ligne de tableau html

        :param op: code OP
        :param poste: texte T long
        :param prestation: intitulé D long
        :param montant: montant net
        :return: ligne de tableau html
        """
        dico_tab = {'poste': poste, 'op': op, 'prestation': prestation,
                    'montant': "%.2f" % montant}
        ligne = r'''<tr>
            <td> %(op)s </td><td> %(poste)s </td><td> %(prestation)s </td>
            <td id="toright"> %(montant)s </td></tr>
            ''' % dico_tab
        return ligne

    @staticmethod
    def creer_html(destination, combo_list, subedition):
        """
        crée une page html autour d'une liste de sections

        :param destination:  Une instance de la classe dossier.DossierDestination
        :param combo_list: liste des clients et leurs sections
        :param subedition: paramètres d'édition
        """
        nom = "ticket_" + str(subedition.annee_fin_general) + "_" + \
              Outils.mois_string(subedition.mois_fin_general) + ".html"
        with destination.open(nom) as fichier:

            html = r'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
                "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
                <html xmlns="http://www.w3.org/1999/xhtml">
                <head>
                <meta content="text/html; charset=cp1252" http-equiv="content-type" />
                <meta content="CMi" name="author" />
                <style>
                #entete {
                    margin-left: 600px;
                    text-align:left;
                }
                #tableau {
                    border-collapse: collapse;
                    margin: 20px;
                    margin-left: 50px;
                }
                #tableau tr, #tableau td {
                    border: 1px solid black;
                    vertical-align:middle;
                }
                #tableau td {
                    padding: 3px;
                }
                #toright {
                    text-align:right;
                }
                #combo {
                    margin-top: 10px;
                    margin-left: 50px;
                }
                </style>
                <link rel="stylesheet" href="./css/reveal.css">
                <link rel="stylesheet" href="./css/white.css">
                </head>
                <body>
                <div id="combo">
                <select name="client" onchange="changeClient(this)">
                '''
            i = 0
            for k, v in sorted(combo_list.items()):
                html += r'''<option value="''' + str(i) + r'''">''' + str(k) + r'''</option>'''
                i += 1
            html += r'''
                </select>
                </div>
                <div class="reveal">
                <div class="slides">
                '''
            for k, v in sorted(combo_list.items()):
                html += v
            html += r'''</div></div>
                    <script src="./js/reveal.js"></script>
                    <script>
                        Reveal.initialize();
                    </script>
                    <script>
                    function changeClient(sel) {
                        Reveal.slide(sel.value, 0);
                    }
                    </script>
                    </body>
                </html>'''
            fichier.write(html)
