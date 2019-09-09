from outils import Outils
import math


class Consolidation(object):
    """
    Classe servant à consolider les données des bilans
    """

    def __init__(self):
        self.clients = {}
        self.a_verifier = 1

    def coherence_bilans(self, bilans, subcomptes, subgeneraux, subedition, force):
        """
        vérifie que les données importées dans les bilan soit cohérentes, et construit la base consolidée
        :param bilans: bilans importés
        :param subcomptes: comptes subsides importés
        :param subgeneraux: paramètres généraux
        :param subedition: paramètres d'édition
        :param force: comptes forcés importés
        :return: > 0 s'il y a une erreur, 0 sinon
        """
        coherence_clients = 0
        coherence_comptes = 0

        for bilan in reversed(bilans):
            d_bon = Outils.comparaison_date(bilan.annee, bilan.mois,
                                            subedition.annee_debut_bonus, subedition.mois_debut_bonus)
            f_bon = Outils.comparaison_date(bilan.annee, bilan.mois,
                                            subedition.annee_fin_bonus, subedition.mois_fin_bonus)
            ok_bon = not d_bon < 0 and not f_bon > 0
            d_sub = Outils.comparaison_date(bilan.annee, bilan.mois,
                                            subedition.annee_debut_subs, subedition.mois_debut_subs)
            f_sub = Outils.comparaison_date(bilan.annee, bilan.mois,
                                            subedition.annee_fin_subs, subedition.mois_fin_subs)
            ok_sub = not d_sub < 0 and not f_sub > 0
            for donnee in bilan.donnees:
                client = donnee[bilan.cles['code client']]
                sap = donnee[bilan.cles['code client sap']]
                nature = donnee[bilan.cles['nature client']]
                ctype = donnee[bilan.cles['type client']]
                abrev = donnee[bilan.cles['abrév. labo']]
                nom = donnee[bilan.cles['nom labo']]
                id_compte = donnee[bilan.cles['id-compte']]
                num_compte = donnee[bilan.cles['numéro compte']]
                intitule = donnee[bilan.cles['intitulé compte']]
                if subgeneraux.avec_bonus:
                    try:
                        bj = float(donnee[bilan.cles['bonus']])
                    except ValueError:
                        Outils.affiche_message("Le bonus n'est pas un nombre")
                        return 1
                else:
                    bj = 0
                if ctype == subgeneraux.article_t_indice('1').code_t and nature in subgeneraux.obtenir_code_n():
                    mois = {'bj': bj}
                    if force and id_compte in force.obtenir_comptes():
                        type_compte = force.obtenir_comptes()[id_compte]
                    else:
                        type_compte = donnee[bilan.cles['code type compte']]
                    if client not in self.clients:
                        annees = {}
                        if ok_bon:
                            annees[bilan.annee] = {'mois': {bilan.mois: mois}}

                        self.clients[client] = {'comptes': {}, 'nature': nature, 'type': ctype, 'abrev': abrev,
                                                'sap': sap, 'coherent': True, 'nom': nom, 'annees': annees}
                    else:
                        if nature != self.clients[client]['nature']:
                            self.clients[client]['coherent'] = False
                            coherence_clients += 1
                        if ctype != self.clients[client]['type']:
                            self.clients[client]['coherent'] = False
                            coherence_clients += 1
                        if ok_bon:
                            if bilan.annee in self.clients[client]['annees']:
                                if bilan.mois in self.clients[client]['annees'][bilan.annee]['mois']:
                                    self.clients[client]['annees'][bilan.annee]['mois'][bilan.mois]['bj'] += bj
                                else:
                                    self.clients[client]['annees'][bilan.annee]['mois'][bilan.mois] = mois
                            else:
                                self.clients[client]['annees'][bilan.annee] = {'mois': {bilan.mois: mois}}
                    comptes = self.clients[client]['comptes']
                    id_sub = subcomptes.obtenir_id(nature, type_compte)
                    if id_sub:
                        try:
                            maj = float(donnee[bilan.cles['maj']])
                            moj = float(donnee[bilan.cles['moj']])
                            rj = float(donnee[bilan.cles['rabais']])
                        except ValueError:
                            Outils.affiche_message("Certaines valeurs (maj, moj, rabais) ne sont pas des nombres")
                            return 1
                        maj -= (bj + rj)
                        mois = {'maj': maj, 'moj': moj}
                        for d3 in subgeneraux.codes_d3():
                            try:
                                j = float(donnee[bilan.cles[d3 + 'j']])
                            except ValueError:
                                Outils.affiche_message("Certaines valeurs d3 ne sont pas des nombres")
                                return 1
                            mois[d3 + 'j'] = j
                        if id_compte not in comptes:
                            annees = {}
                            if ok_sub:
                                annees[bilan.annee] = {'mois': {bilan.mois: mois}}
                            code_t3 = subcomptes.donnees[id_sub]['type_subside']
                            type_s = subgeneraux.article_t(code_t3).texte_t_court
                            comptes[id_compte] = {'id_sub': id_sub, 'num_compte': num_compte, 'intitule': intitule,
                                                  'type_p': subcomptes.donnees[id_sub]['intitule'],
                                                  'type': type_compte, 'type_s': type_s, 't3': code_t3,
                                                  'coherent': True, 'annees': annees}
                        else:
                            if id_sub != comptes[id_compte]['id_sub']:
                                comptes[id_compte]['coherent'] = False
                                coherence_comptes += 1
                            if ok_sub:
                                if bilan.annee in comptes[id_compte]['annees']:
                                    comptes[id_compte]['annees'][bilan.annee]['mois'][bilan.mois] = mois
                                else:
                                    comptes[id_compte]['annees'][bilan.annee] = {'mois': {bilan.mois: mois}}

        if coherence_clients > 0:
            msg = "Les clients suivants ne sont pas homogènes sur la période, " \
                  "soit pour la nature du client soit pour le type du client : \n"
            for k, v in self.clients.items():
                if not v['coherent']:
                    msg += " - " + k + "/" + v['abrev'] + "\n"
            Outils.affiche_message(msg)

        if coherence_comptes > 0:
            msg = "Les comptes suivants ne sont pas homogènes sur la période, " \
                  "soit pour la nature du client soit pour le code type compte : \n"
            for k, v in self.clients.items():
                for l, w in v['comptes'].items():
                    if not w['coherent']:
                        msg += " - " + k + "/" + v['abrev'] + "/" + w['num_compte'] + "/" + l + "/" + \
                               w['intitule'] + "\n"
            Outils.affiche_message(msg)

        reponse = coherence_clients + coherence_comptes
        self.a_verifier = 0

        return reponse

    def calcul_sommes(self, subgeneraux, submachines, subprestations):
        for cl, client in self.clients.items():
            client['subs'] = 0
            client['bonus'] = 0
            client['codes'] = {}
            client['subs_ma'] = 0
            client['subs_mo'] = 0
            for d3 in subgeneraux.codes_d3():
                client['subs_' + d3 + 't'] = 0
            for a, annee in client['annees'].items():
                for m, mois in annee['mois'].items():
                    mois['bj'] = math.ceil(mois['bj'])
                    client['bonus'] += mois['bj']
            for co, compte in client['comptes'].items():
                compte['mat'] = 0
                compte['mot'] = 0
                compte['mat_p'] = 0
                compte['mot_p'] = 0
                compte['ma_mois'] = submachines.donnees[compte['id_sub']]['ma_mois']
                compte['mo_mois'] = submachines.donnees[compte['id_sub']]['mo_mois']
                compte['ma_compte'] = submachines.donnees[compte['id_sub']]['ma_compte']
                compte['mo_compte'] = submachines.donnees[compte['id_sub']]['mo_compte']
                for d3 in subgeneraux.codes_d3():
                    compte[d3 + 't'] = 0
                    compte[d3 + 't_p'] = 0
                    compte[d3 + '_mois'] = subprestations.donnees[compte['id_sub']+d3]['max_mois']
                    compte[d3 + '_compte'] = subprestations.donnees[compte['id_sub']+d3]['max_compte']
                for a, annee in compte['annees'].items():
                    for m, mois in annee['mois'].items():
                        compte['mat'] += mois['maj']
                        compte['mot'] += mois['moj']
                        compte['mat_p'] += min(mois['maj'], compte['ma_mois'])
                        compte['mot_p'] += min(mois['moj'], compte['mo_mois'])
                        for d3 in subgeneraux.codes_d3():
                            compte[d3 + 't'] += mois[d3 + 'j']
                            compte[d3 + 't_p'] += min(mois[d3 + 'j'], compte[d3 + '_mois'])
                compte['s-mat'] = min(compte['mat_p'], compte['ma_compte'])
                compte['s-mot'] = min(compte['mot_p'], compte['mo_compte'])
                compte['subs'] = compte['s-mat'] + compte['s-mot']
                if compte['t3'] not in client['codes']:
                    client['codes'][compte['t3']] = {'sm': 0}
                client_t3 = client['codes'][compte['t3']]
                client_t3['sm'] += compte['s-mat'] + compte['s-mot']
                for d3 in subgeneraux.codes_d3():
                    compte['s-' + d3 + 't'] = min(compte[d3 + 't_p'], compte[d3 + '_compte'])
                    compte['subs'] += compte['s-' + d3 + 't']
                    client['subs_' + d3 + 't'] += compte['s-' + d3 + 't']
                    if ('s' + d3) not in client_t3:
                        client_t3['s' + d3] = 0
                    client_t3['s' + d3] += compte['s-' + d3 + 't']
                client['subs'] += compte['subs']
                client['subs_ma'] += compte['s-mat']
                client['subs_mo'] += compte['s-mot']

        a_effacer = []
        for code, client in self.clients.items():
            if client['subs'] == 0 and client['bonus'] == 0:
                a_effacer.append(code)
                continue
            del client['coherent']
            for l, w in client['comptes'].items():
                del w['coherent']
        for k in a_effacer:
            del self.clients[k]
