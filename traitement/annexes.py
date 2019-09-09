from outils import Outils
from latex import Latex


class Annexes(object):
    """
    Classe pour la création des annexes
    """
    @staticmethod
    def annexes(consolidation, plateforme, subgeneraux, subedition, dossier_annexe):
        """
        création des annexes de subsides
        :param consolidation: classe de consolidation des données des bilans
        :param plateforme: OS utilisé
        :param subgeneraux: paramètres généraux
        :param subedition: paramètres d'édition
        :param dossier_annexe: nom du dossier dans lequel enregistrer le dossier des annexes
        """
        for code_client, dcl in consolidation.clients.items():
            code_client = Latex.echappe_caracteres(code_client)

            contenu = Latex.entete(plateforme)
            contenu += r'''
                \usepackage[margin=10mm, includehead]{geometry}
                \usepackage{changepage}
                \usepackage{graphicx}
                \usepackage{longtable}
                \usepackage{dcolumn}
                \usepackage[scriptsize]{caption}
                \usepackage{fancyhdr}
                '''

            if subedition.filigrane != "":
                contenu += r'''
                    \usepackage{draftwatermark}
                    \SetWatermarkLightness{0.8}
                    \SetWatermarkAngle{45}
                    \SetWatermarkScale{2}
                    \SetWatermarkFontSize{2cm}
                    \SetWatermarkText{''' + subedition.filigrane[:15] + r'''}
                    '''

            contenu += r'''
                \pagestyle{fancy}

                \fancyhead{}
                \fancyfoot{}

                \renewcommand{\headrulewidth}{0pt}
                \renewcommand{\footrulewidth}{0pt}

                \fancyhead[L]{\leftmark \\ \rightmark}
                \fancyhead[R]{\thepage}

                \newcommand{\fakesection}[2]{
                    \markboth{#1}{#2}
                }
                
                \begin{document}
                \renewcommand{\arraystretch}{1.5}
                '''
            reference = "SUBS" + str(subedition.annee_fin_general)[2:] + \
                        Outils.mois_string(subedition.mois_fin_general) + "." + code_client

            contenu += r'''
                \begin{titlepage}
                \vspace*{8cm}
                \begin{adjustwidth}{5cm}{}
                \Large\textsc{Annexes subsides \newline Subsidies Appendices}\newline
                \Large\textsc{''' + reference + r'''}\newline\newline\newline
                '''

            debut = Outils.mois_nom(subedition.mois_debut_general) + " " + str(subedition.annee_debut_general)
            fin = Outils.mois_nom(subedition.mois_fin_general) + " " + str(subedition.annee_fin_general)
            dic_entete = {'code': code_client, 'code_sap': Latex.echappe_caracteres(dcl['sap']),
                          'nom': Latex.echappe_caracteres(dcl['abrev']),
                          'debut': debut, 'fin': fin}

            contenu += r'''Client %(code)s - %(code_sap)s - %(nom)s \newline
                 %(debut)s - %(fin)s
                \end{adjustwidth}
                \end{titlepage}    
                \clearpage
                ''' % dic_entete
            contenu += Annexes.contenu_client(code_client, consolidation, subgeneraux, subedition)
            contenu += r'''\end{document}'''

            nom = "subside_" + str(subedition.annee_fin_general) + "_" + \
                  Outils.mois_string(subedition.mois_fin_general) + "_" + code_client

            Latex.creer_latex_pdf(nom, contenu, dossier_annexe)

    @staticmethod
    def contenu_client(code_client, consolidation, subgeneraux, subedition):
        """
        création du contenu de l'annexe pour un client
        :param code_client: code du client pour l'annexe
        :param consolidation: classe de consolidation des données des bilans
        :param subgeneraux: paramètres généraux
        :param subedition: paramètres d'édition
        """

        contenu = ""

        client = consolidation.clients[code_client]
        reference = "SUBS" + str(subedition.annee_fin_general)[2:] + \
                    Outils.mois_string(subedition.mois_fin_general) + "." + code_client

        debut = Outils.mois_nom(subedition.mois_debut_general) + " " + str(subedition.annee_debut_general)
        fin = Outils.mois_nom(subedition.mois_fin_general) + " " + str(subedition.annee_fin_general)
        dic_section = {'code': code_client, 'code_sap': Latex.echappe_caracteres(client['sap']),
                       'nom': Latex.echappe_caracteres(client['abrev']), 'ref': reference,
                       'date_debut': debut, 'date_fin': fin}

        contenu += r'''
            \fakesection{%(ref)s \hspace*{4cm} Client %(code)s - %(code_sap)s - %(nom)s - %(date_debut)s - %(date_fin)s}
            {}
            ''' % dic_section

        contenu_recap_compte = ""
        contenu_detail_compte = ""
        inc_4 = 0
        taille_d3 = len(subgeneraux.articles_d3)

        numbers = {}
        for id_compte, compte in client['comptes'].items():
            numbers[id_compte] = compte['num_compte']

        for id_compte, num_compte in sorted(numbers.items(), key=lambda x: x[1]):
            compte = client['comptes'][id_compte]

            # ## COMPTE

            # ## ligne 3
            if compte['subs'] > 0:
                dico_recap_compte = {'numero': num_compte, 'intitule': Latex.echappe_caracteres(compte['intitule']),
                                     'code': Latex.echappe_caracteres(compte['id_sub']),
                                     'type_s': Latex.echappe_caracteres(compte['type_s']),
                                     'type_p': Latex.echappe_caracteres(compte['type_p']),
                                     'montant': Outils.format_2_dec(compte['subs'])}
                contenu_recap_compte += r'''
                    %(numero)s & %(intitule)s & %(code)s & %(type_s)s & %(type_p)s & %(montant)s \\
                    \hline
                      ''' % dico_recap_compte

            # ## partie 4

            if compte['subs'] > 0:
                dico_detail_compte = {'taille': (4 + taille_d3), 'numero': num_compte,
                                      'intitule': Latex.echappe_caracteres(compte['intitule']),
                                      'type': Latex.echappe_caracteres(compte['type'])}
                if inc_4 > 0:
                    contenu_detail_compte += r'''
                        \multicolumn{%(taille)s}{c}{} \\ \noalign{\penalty-5000}
                          ''' % dico_detail_compte
                else:
                    inc_4 = 1
                contenu_detail_compte += r'''
                    \hline
                    \multicolumn{%(taille)s}{|c|}{%(numero)s - %(intitule)s - %(type)s} \\*
                    \hline
                    Année & Mois & \multicolumn{1}{c|}{Machine} & 
                    \multicolumn{1}{c|}{M.O. op.} 
                      ''' % dico_detail_compte

                for article in subgeneraux.articles_d3:
                    contenu_detail_compte += r''' & \multicolumn{1}{c|}{
                        ''' + Latex.echappe_caracteres(article.intitule_court) + r'''}'''

                for a, annee in sorted(compte['annees'].items()):
                    for m, mois in sorted(annee['mois'].items()):
                        dico = {'annee': a, 'mois': m, 'maj': Outils.format_2_dec(mois['maj']),
                                'moj': Outils.format_2_dec(mois['moj'])}
                        contenu_detail_compte += r'''\\*
                            \hline
                            %(annee)s & %(mois)s & %(maj)s & %(moj)s
                            ''' % dico
                        for d3 in subgeneraux.codes_d3():
                            contenu_detail_compte += r''' & ''' + Outils.format_2_dec(mois[d3 + 'j'])

                dico_detail_compte = {'ma_mois': compte['ma_mois'], 'mo_mois': compte['mo_mois'],
                                      'ma_compte': compte['ma_compte'], 'mo_compte': compte['mo_compte'],
                                      'mat': Outils.format_2_dec(compte['mat']),
                                      'mot': Outils.format_2_dec(compte['mot']),
                                      'mat_p': Outils.format_2_dec(compte['mat_p']),
                                      'mot_p': Outils.format_2_dec(compte['mot_p']),
                                      's-mat': Outils.format_2_dec(compte['s-mat']),
                                      's-mot': Outils.format_2_dec(compte['s-mot'])}

                contenu_detail_compte += r'''\\*
                    \hline
                    \multicolumn{2}{|l|}{Total période} & %(mat)s & %(mot)s
                    ''' % dico_detail_compte
                for d3 in subgeneraux.codes_d3():
                    contenu_detail_compte += r''' &
                    ''' + Outils.format_2_dec(compte[d3 + 't'])

                contenu_detail_compte += r'''\\*
                    \hline
                    \multicolumn{2}{|l|}{Plafond par mois} & %(ma_mois)s & %(mo_mois)s
                    ''' % dico_detail_compte
                for d3 in subgeneraux.codes_d3():
                    contenu_detail_compte += r''' &
                    ''' + Outils.format_2_dec(compte[d3 + '_mois'])

                contenu_detail_compte += r'''\\*
                    \hline
                    \multicolumn{2}{|l|}{Total des montants plafonnés} & %(mat_p)s & %(mot_p)s
                    ''' % dico_detail_compte
                for d3 in subgeneraux.codes_d3():
                    contenu_detail_compte += r''' &
                    ''' + Outils.format_2_dec(compte[d3 + 't_p'])

                contenu_detail_compte += r'''\\*
                    \hline
                    \multicolumn{2}{|l|}{Plafond par compte} & %(ma_compte)s & %(mo_compte)s
                    ''' % dico_detail_compte
                for d3 in subgeneraux.codes_d3():
                    contenu_detail_compte += r''' &
                    ''' + Outils.format_2_dec(compte[d3 + '_compte'])

                contenu_detail_compte += r'''\\*
                    \hline
                    \multicolumn{2}{|l|}{Subsides} & %(s-mat)s & %(s-mot)s
                    ''' % dico_detail_compte
                for d3 in subgeneraux.codes_d3():
                    contenu_detail_compte += r''' &
                    ''' + Outils.format_2_dec(compte['s-' + d3 + 't'])

                dico_detail_compte = {'taille': (2 + len(subgeneraux.articles_d3)),
                                      'subs': Outils.format_2_dec(compte['subs'])}
                contenu_detail_compte += r'''\\*
                    \hline
                    \multicolumn{2}{|l|}{Total subsides} & \multicolumn{%(taille)s}{r|}{%(subs)s} \\ 
                    \hline
                    ''' % dico_detail_compte

        # ## 1

        structure_total = r'''{|c|l|l|r|}'''
        contenu_total = r'''
            \hline
            Code OP & \multicolumn{1}{c|}{Poste} & \multicolumn{1}{c|}{Prestation} & \multicolumn{1}{c|}{Montant} \\
            \hline
            '''
        base = client['nature'] + str(subedition.annee_fin_general)[2:] + \
               Outils.mois_string(subedition.mois_fin_general)
        if client['bonus'] > 0:
            poste = Latex.echappe_caracteres(subgeneraux.article_t_indice('2').texte_t_long)
            prestation = Latex.echappe_caracteres(subgeneraux.articles[0].intitule_long)
            op = subgeneraux.article_t_indice('2').code_t + base + subgeneraux.articles[0].code_d
            dico = {'op': op, 'poste': poste, 'prestation': prestation, 'montant': Outils.format_2_dec(client['bonus'])}
            contenu_total += r'''
                %(op)s & %(poste)s & %(prestation)s & %(montant)s \\
                \hline
                ''' % dico
        for t3, client_t3 in sorted(client['codes'].items()):
            poste = subgeneraux.article_t(t3).texte_t_long
            if client_t3['sm'] > 0:
                prestation = Latex.echappe_caracteres(subgeneraux.articles[0].intitule_long)
                op = t3 + base + subgeneraux.articles[0].code_d
                dico = {'op': op, 'poste': poste, 'prestation': prestation,
                        'montant': Outils.format_2_dec(client_t3['sm'])}
                contenu_total += r'''
                    %(op)s & %(poste)s & %(prestation)s & %(montant)s \\
                    \hline
                    ''' % dico
            for article in subgeneraux.articles_d3:
                if client_t3['s' + article.code_d] > 0:
                    prestation = Latex.echappe_caracteres(article.intitule_long)
                    op = t3 + base + article.code_d
                    dico = {'op': op, 'poste': poste, 'prestation': prestation,
                            'montant': Outils.format_2_dec(client_t3['s' + article.code_d])}
                    contenu_total += r'''
                        %(op)s & %(poste)s & %(prestation)s & %(montant)s \\
                        \hline
                        ''' % dico
        total = Outils.format_2_dec(client['subs'] + client['bonus'])
        contenu_total += r'''
            \multicolumn{3}{|r|}{TOTAL} & ''' + total + r''' \\
            \hline
            '''

        legende_total = r'''Table 1 - Récapitulatif des bonus et subsides'''

        contenu += Latex.tableau(contenu_total, structure_total, legende_total)

        # ## 2

        if client['bonus'] > 0:
            structure_bonus = r'''{|c|c|l|r|}'''
            contenu_bonus = r'''
                \hline
                Année & Mois & \multicolumn{1}{c|}{Code} & \multicolumn{1}{c|}{Montant} \\
                \hline
                '''

            for a, annee in sorted(client['annees'].items()):
                for m, mois in sorted(annee['mois'].items()):
                    code = Latex.echappe_caracteres(subgeneraux.article_t_indice('2').texte_t_court)
                    dico = {'annee': a, 'mois': m, 'bj': mois['bj'],
                            'code': code}
                    contenu_bonus += r'''
                        %(annee)s & %(mois)s & %(code)s & %(bj)s \\
                        \hline
                        ''' % dico

            contenu_bonus += r'''
                \multicolumn{3}{|r|}{TOTAL} & ''' + str(client['bonus']) + r''' \\
                \hline
                '''

            legende_bonus = r'''Table 2 - Bonus d'utilisation en heures creuses'''

            contenu += Latex.tableau(contenu_bonus, structure_bonus, legende_bonus)
        else:
            contenu += Latex.tableau_vide(r'''Table 2 vide : Pas de bonus d'utilisation en heures creuses''')

        if client['subs'] > 0:

            # ## 3

            structure_recap = r'''{|r|l|l|l|l|r|}'''
            contenu_recap = r'''
                \hline
                \multicolumn{1}{|c|}{N. compte} & \multicolumn{1}{c|}{Intitulé compte} & \multicolumn{1}{c|}{Code} & 
                \multicolumn{1}{c|}{Type Subsides} & \multicolumn{1}{c|}{Type projet} & \multicolumn{1}{c|}{Montant} \\
                \hline
                '''
            contenu_recap += contenu_recap_compte
            contenu_recap += r'''
                \multicolumn{5}{|r|}{TOTAL} & ''' + Outils.format_2_dec(client['subs']) + r''' \\
                \hline
                '''

            legende_recap = r'''Table 3 - Récapitulatif des subsides par compte'''

            contenu += Latex.tableau(contenu_recap, structure_recap, legende_recap)

            # ## 4

            structure_detail = r'''{|>{\centering}p{1.5cm}|c|r|r|'''
            for i in range(taille_d3):
                structure_detail += r'''r|'''
            structure_detail += r'''}'''

            legende_detail = r'''Table 4 - Détail des subsides'''

            contenu += Latex.long_tableau(contenu_detail_compte, structure_detail, legende_detail)

        else:
            contenu += Latex.tableau_vide(r'''Table 3 vide : Pas de subsides''')

        return contenu
