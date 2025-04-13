#import "template.typ": *
#import "@preview/cetz:0.3.1": canvas, draw
#import "@preview/cetz-plot:0.1.0": plot

#show: report.with(
  title: [ Problème du voyageur canadien couvrant ],
  course: [ Résolution de problème ],
  authors: ("Paul Chambaz", "Philipp Hanussek" ),
  university: [ Sorbonne Université ],
  reference: [ Master #smallcaps[Ai2d] M1 & #smallcaps[Iq] ],
  nb-columns: 2,
  abstract: [
    #lorem(20)
  ]
)

== Introduction

Le problème du voyageur de commerce (_Traveling Salesman Problem_ ou _TSP_) constitue l'un des défis classiques en optimisation combinatoire. Dans sa formulation standard, on cherche à déterminer le parcours de longueur minimale permettant de visiter une seule fois chaque ville d'un ensemble donné avant de revenir au point de départ. Malgré sa simplicité d'énoncé, ce problème est $cal(N P)$-difficile.

Une variante moins étudiée mais particulièrement pertinente pour les applications pratiques est le problème du voyageur canadien couvrant (_Covering Canadian Travaller Problem_ ou _CCTP_). Contrairement au TSP classique où l'ensemble des arêtes est connu à l'avance, le CCTP introduit un élément d'incertitude : certaines arêtes peuvent être bloquées, et un voyageur ne découvre qu'une arête est inaccessibles qu'en atteignant l'un de ses sommets adjacents. Cette contrainte reflète des situtations réelles comme la planification d'itinéraires dans des réseaux routiers où des blocages imprévus (accident, travaux) ne sont découverts qu'en arrivant à proximité.

Une spécialisation importante de ce problème est le $k$-CCTP, où le nombre d'arêtes bloquées est limité à $k$. Cette restriction permet de développer des algorithmes avec des garanties de performance théoriques. Dans ce contexte, on s'intéresse au rapport d'approximation, qui quantifie le ratio entre la distance parcourue par l'algorithme et celle qu'aurait parcourue un voyageur omniscient connaissant à l'avance l'emplacement de toutes les arêtes bloquées.

Dans ce document, nous présentons deux algorithmes qui ont été proposés pour résoudre le $k$-CCTP. L'algorithme CR et l'algorithme CNN, qui possède un rapport d'aproximation de $O(sqrt(k))$ et de $O(log k)$ respectivement. Nous analysons les garanties théoriques et évaluons empiriquement leurs performances sur diverses classes de graphes.

== Christofides

L'algorithme de Christofides, proposé en 1976, est une méthode d'approximation pour le problème du voyageur de commerce dans les graphes métriques, c'est-à-dire où les distances satisfont l'inégalité triangulaire. Cet algorithme garantit une solution dont le coût ne dépasse par 1.5 fois celui de la solution optimale, ce qui en fait l'un des algorithmes d'approximation les plus performants pour le TSP métrique.

=== Description de l'algorithme
L'algorithme de Christofides se déroule en cinq étapes principales :

1. Calcul d'un arbre couvrant de poids minimal $T$ du graphe $G$.
2. Identification des sommets de degré impair dans $T$.
3. Calcul d'un couplage parfait de poids minimal $M$ pour les sommets de degré impair.
4. Combinaison de $T$ et $M$ pour formet un multigraphe eulérien $H$.
5. Construction d'un circuit eulérien dans $H$, puis conversion en cycle hamiltonien par _raccourcissement_ (élimination des sommets répétés).

Cette approche exploite le fait que tout graphe possédant uniquement des sommets de degré pair admet un circuit eulérien, c'est-à-dire un circuit qui emprunte chaque arête exactement une fois. En ajoutant le couplage minimal $M$ à l'arbre couvrant $T$, on obtient un tel graphe.

=== Preuve du rapport d'approximation
Cette section présente la preuve de l'article de N. Chrisofides (1976).

==== Thérorème
L'algorithme de Christofides garantit un rapport d'aprpoximation de 1.5 pour le problème du voyageur de commerce dans les graphes métriques.

==== Preuve
Soit $G = (V, E)$ un graphe complet métrique et $OPT$ le coût de la solution optimale au TSP sur $G$. Nous voulons montrer que le coût du cycle hamiltonien produit par l'algorithme de Christofides est au plus $3/2 dot OPT$.

L'algorithme de Christofides fonctionne par construction intérmédiaires, nous analyserons leurs coûts.

Montrons que $c(T) <= OPT$. Soit $C^*$ un cycle hamiltonien optimal. En supprimant une arête quelconque de $C^*$, nous obtenons un arbre couvrant $T'$. Puisque $T$ est un arbre couvrant de poids minimal, nous avons : $c(T) <= c(T') <= OPT$.

Montrons que $c(M) <= OPT/2$. Soit $O subset V$ l'ensemble des sommets de degré impair dans $T$. D'après le lemme des poignées de mains, qui stipule "chaque graphe non orienté fini a un nombre pair de sommets de degré impair", $|O|$ est pair. Considérons le cycle hamiltonien optimal $C^*$. En parcourant $C^*$ de manière alternée, nous pouvons partitionner ses arêtes en deux ensembles $E_1$ et $E_2$ tels que chaque ensemble forme une collection de chemins dont les extremités sont exactement les sommets de $O$ et $c(E_1) + c(E_2) = OPT$. Par conséquent, l'un de ces ensembles, disons $E_1$, a un coût au plus égal à $OPT/2$. Les chemins dans $E_1$ induisent un couplage valide $M'$ entre les sommets de $O$. En vertu de l'inégalité triangulaire, le coût de ce couplage $M'$ est au plus égal au coût des chemins correspodnants dans $E_1$. Pusique $M$ est un couplage parfait de poids minimal entre les sommets de $O$, nous avons : $c(M) <= c(M') <= c(E_1) <= OPT/2$.

Le coût du multigraphe eulérien $H$ est donc : $c(H) = c(T) + c(M) <= OPT + OPT/2 = 3/2 dot OPT$.

Le circuit eulérien parcourt exactement les arêtes de $H$, donc son coût est égal à $c(H)$.

Le cycle hamiltonien est obtenu en _raccourcissant_ le circuit eulérien, c'est-à-dire en prenant des raccourcis directs lorsqu'un sommet est revisité. Grâce à l'inégalité triangulaire, ces raccourcis ne peuvent qu'améliorer (ou au pire maintenir) le coût. Donc le coût du cycle hamiltonien final est au plus $c(H) <= 3/2 dot OPT$.
#h(1fr) $qed$

=== Implémentation et validation
Notre implémentation de l'algorithme de Christofides utilise _Python_ et la bibliothèque _NetworkX_ pour représenter les graphes. Cette implémentation est disponible dans le fichier `cctp/christofides.py`. Pour valider la correction de l'implémentation, nous avons développé une suite de tests unitaires vérifiant que :
- le tour commence et se termine au même sommet ;
- le tour généré visite tous les sommets du graphe ;
- le tour généré passe au plus une fois par chaque sommet.

Pour assurer la robustesse de notre implémentation face à différentes configurations, nous avons également effectué 200 tests _fuzzy_ sur des graphes générés aléatoirement avec un nombre de sommet variant entre 4 et 256.

=== Cadre expérimental
Pour évaluer empiriquement les performances de l'algorithmes, nous avons généré des graphes complets aléatoires respectant l'inégalité triangulaire. Chaque graphe est construit en plaçant $n$ points aléatoirement dans un espace euclidien à deux dimensions, avec des coordonnées tirées uniforméments dans $[-5.0, 5.0]$. Les distances entre les sommets corresponent aux distances euclidiennes, garantissant ainsi l'inégalité triangulaire.

Pour chaque taille de graphe, nous avons effectué 15 mesures indépendantes afin d'obtenir des résultats statistiquement significatifs pour des comparaisons. Notre analyse reporte les statistiques suivantes : la valeur minimale et maximale, le premier et troisième quartile et la moyenne inter-quartile. 

=== Analyse du rapport d'approximation
Pour évaluer le rapport d'approximation empirique, nous avons comparé le coût des solutions générées par l'algorithme de Christofides au coût optimal obtenu par une recherche exhaustive, nous limitons la taille de ces instances à 12 nœuds pour se ramener à des instances calculables en un temps raisonnable.

#figure(
  image("figures/christofides_ratio_plot.svg"),
  caption: [
  Évaluation du rapport d'approximation de l'algorithme de Christofides sur des instances du TSP générées aléatoirement en fonction du nombre de sommet (15 instances par taille). La courbe bleue représente la moyenne interquartile et la zone bleutée représente l'intervalle entre le minimum et le maximum.
  ]
) <fig-1>

La @fig-1 présente l'évolution du rapport d'approximation en fonction du nombre de sommets. Les résultats montrent que, bien que le rapport théorique soit de 1.5, le rapport observé en pratique est généralement meilleur, se situant autout de 1.1 pour les graphes euclidiens aléatoires. Ce résultat est cohérent avec la borne pessimiste de 1.5 donnée par l'algorithme de Christofides.

=== Analyse de complexité
La complexité théorique de l'algorithme de Christofides est dominée par le calcul du couplage parfait de poids minimal, qui peut être résolu en $O(n^3)$ où $n$ est le nombre de sommets. Pour vérifier cette complexité empiriquement, nous avons mesuré le temps d'exécution de l'algorithme sur des graphes de tailles croissantes.

#figure(
  image("figures/christofides_time_plot.svg"),
  caption: [
  Évolution du temps d'exécution de l'algorithme de Christofides sur des instances du TSP générées aléatoirement en fonction du nombre de sommet (15 mesures par taille). La courbe bleue représente la moyenne interquartile et la zone bleutée l'intervalle interquartile. La courbe noire représente le résultat de la regréssion linéaire sur les racines cubiques des IQM, $R^2$ représente le cohéfficient de linéarité, avec des valeur proches de $1$ indiquant une forte corrélation linéaire.
  ]
) <fig-2>

La @fig-2 présente les résultats de cette analyse, avec le temps d'exécution en fonction du nombre de sommets. Nous avons appliqué une régression linéaire sur la racine cubique du temps d'exécution, obtenant un coefficient de corrélation linéaire $R^2$ proche de 1, ce qui confrime la complexité théorique en $O(n^3)$. Cette analyse empirique valide l'analyse théorique et donne également une estimation pratique des constantes impliquées, permettant de prédire le temps d'execution pour de plus grandes instances.

==  Cr

// TODO: écrire cette partie, mais ce n'est pas ma tache mais celle de mon binome

== Cnn

L'algorithme CNN (Christofides Nearest Neighbor) représente une amélioration par rapport à l'algorithme CR, offrant un rapport d'approximation de $O(log k)$ et découvert par N. Hahn et M. Xefteris.

=== Description de l'algorithme
L'algorithme CNN se déroule en quatre phases principales.

1. Calcul d'un tour initial par Christofides $T$.
2. Parcours du tour en utilisant la procédure #smallcaps[Shortcut] utilisé par CR. Suite à ce tour, si on ne termine pas au nœud initial, on revient sur ses pas jusqu'à ce qu'on y revienne. Lors de cette phase, à chaque passage de sommet, on note les arêtes qui sont bloquées.
3. On construit un graphe de connaissance $H$, ce graphe contient tous les sommets du graphe et toutes les arêtes adjacentes à des arêtes visitées lors du tour initial et non bloquées. C'est avec ce graphe de connaissance que l'on peut construire un multigraphe d'exploration $G'$, qui contient tous les nœuds qui n'ont pas pu être exploré lors du tour initial, et le sommet initial. Ce graphe contient entre tous deux sommets $u$ et $v$ deux chemins : d'une part un chemin risqué, qui correspond à l'arête $(u, v)$ de $G$, mais dont on ne peut pas être sur de si il est accessible ou non, et d'autres part, un chemin alternatif, calculé dans $H$, mais plus long. On a donc deux options pour chaque passage, soit, si il est accessible, prendre le chemin court, sinon, prendre le chemin long, garanti d'être accessible car calculé dans le graphe de connaissance, mais qui fait faire un détour.
4. La dernière phase utilise l'algorithme du plus proche voisin (_Nearest Neighbor_) pour compléter le tour en visitant tous les nœuds de $G'$. L'algorithme sélectionne itérativement le nœud le plus proche accessible par un chemin non bloqué. Une fois tous les nœuds visitiés, l'algorithme revient au point de départ pour compléter le tour.

=== Preuve du rapport d'approximation
Cette section présente la preuve de l'article de N. Hahn et M. Xefteris (2023).

==== Théorème
L'algorithme CNN a un rapport d'approximation de $O(log k)$ pour le problème k-CCTP, où $k$ est le nombre maximal d'arêtes bloquées.

==== Preuve
Soit $G$ un graphe complet métrique et $T$ le tour initial calculé par l'algorithme de Christofides. Puisque Christofides garantit une $3/2$-approximation du TSP, nous avons :

$ c(T) <= 3/2 dot OPT $

Lors de la phase de raccourci, l'algorithme suit $T$ jusqu'à rencontrer des arêtes bloquées, puis retourne au point de départ. Soit $T_S$ le tour obtenue à la suite de la phase de raccourci. Dans le pire cas l'algorithme parcourt le tour puis revient sur ses pas donc :

$ c(T_S) <= 3 dot OPT $

Après cette phase, il reste un ensemble de sommets non visités $U$. Remarquons que chaque sommet non visité correspond à au moins une arête bloqué découverte pendant la phase de raccourci. En effet, pour qu'un sommet reste non visité, l'arête qui aurait permis d'y accéder dans le tour $T$ devait être bloquée. Puisqu'il y a au plus $k$ arêtes bloquée, nous avons $|U| <= k$. Par conséquent, le graphe d'exploration $G'$ contient au plus $k + 1$ sommets (les sommets non visités plus le sommet de départ).

Pour compléter le tour, l'algorithme utilise l'heuristique du plus proche voisin sur $G'$. Pour chaque paire de sommets dans $G'$, il existe toujours au moins un chemin sûr dans le graphe de connaissance. En effet, le graphe original $G$ est complet avec un degré $n-1$ pour chaque sommet. Pour isoler complètement un sommet dans le graphe de connaissance, il faudrait que toutes ses arêtes soient bloquées, ce qui nécessiterait $n-1$ arêtes bloquées. Comme $k < n-1$, cela est impossible. Ainsi, l'algorithme du plus proche voisin peut toujours progresser en utilisant soit le chemin direct (s'il n'est pas bloqué), soit le chemin sûr par le graphe de connaissance.

Il est établit que sur un graphe arbitraire de $n$ sommets, l'algorithme du plus proche voisin a un rapport d'aproximation de $O(log n)$. Appliqué au graphe d'exploration de taille au plus $k+1$, cela donne un rapport $O(log(k+1)) = O(log k)$.

Le cout optimal pour visiter tous les sommets de $G'$ dans le graphe original ne peut pas être inférieur à la solution optimale $OPT$. Soit $T_"NN"$ le tour obtenu après la phase d'exploration, nous avons :

$ c(T_"NN") = O(log k) dot OPT $

En combinant les coûts des deux phases, nous obtenons un coût total d'au plus :

$ 
c(T_"CNN") = c(T_S) + c(T_"NN") \
= 3 dot OPT  + O(log k) dot OPT = O(log k)
$

Ce qui établit le rapport d'approximation de $O(log k)$ pour l'algorithme CNN.

=== Implémentation et validation
Notre implémentation de l'algorithme CNN est disponible dans le fichier `cctp/cnn.py`. Pour valider la correction de l'implémentation, nous avons développé une suite de tests unitaires vérifiant que :
- le tour commence et se termine au même sommet ;
- le tour généré visite tous les sommet du graphe ;
- le tour ne contient aucune arête bloquée.

Pour assurer la robustesse de notre implémentation face à différente configuration, nous avons egalement effectué 200 tests _fuzzy_ sur des graphes générés aléatoirement avec un nombre de sommet variant entre 4 et 256.

=== Cadre expérimental
Nous réutilisons ici les mêmes méthodes déjà utilisée durant les autres parties.

=== Analyse du rapport d'approximation
Pour évaluons le rapport d'approximation empirique de CNN, on cherche une classe de graphe qui atteint la borne de complexité. Cela est le cas pour la famille de graphe qui sert d'exemple au fait que la borne en $O(log k)$ est serrée.

=== Analyse de complexité
La complexité temporelle de l'algorithme CNN est dominée par celle de l'algorithme CNN, c'est pourquoi nous retirons la phase de calcul du tour de Christofides de la mesure de performance temporelle. On s'intéresse alors à la complexité du reste de l'exécution de l'algorithme.

La phase de raccourci a une complexité de $O(n)$ due à l'algorithme de Christofides. La phase de calcul du graphe de connaissance et du graphe d'exploration implique le calcul de $O(k^2)$ plus courts chemins dans un graphe de taille $n$, pour une complexité de $O(k^2 dot n^2)$. La phase d'exploration a une complexité de $O(k^2)$ car elle applique l'algorithme du plus proche voisin sur un graphe de $k+1$ sommets.

La complexité totale est donc $O(k^2 + n^2)$. Pour $k << n$, cette complexité est dominée par $O(n^2)$. On note en particulier, que l'observation faite durant l'évaluation du rapport d'approximation tient toujours ici : pour faire plus que le passage initial, il faut qu'au moins un nœud bloqué soit dans le tour de Christofides initial, mais cette probabilité réduit à mesure que $n$ grandit. Pour vérifier cette complexité empiriquement, nous avons mesuré le temps d'exécution de l'algorithme sur des graphes de tailles croissantes.

La @fig-cnn-time-n présente les résultats de cette analyse, avec le temps d'exécution en fonction du nombre de sommets. Nous avons appliqué une régression linéaire, obtenant un coefficient de corrélation linéaire $R^2$ proche de $1$, ce qui confirme la complexité théorique en $O(n^2)$.

#figure(
  image("figures/cnn_time_plot_n.svg"),
  caption: [
  Évolution du temps d'exécution de l'algorithme CNN sur des instances du TSP générées aléatoirement en fonction du nombre de sommet (15 mesures par taille). La courbe bleue représente la moyenne interquartile et la zone bleutée l'intervalle interquartile. La courbe noire représente le résultat de la regréssion linéaire sur les racines cubiques des IQM, $R^2$ représente le cohéfficient de linéarité, avec des valeur proches de $1$ indiquant une forte corrélation linéaire. On fixe $k$ à $n-2$.
  ]
) <fig-cnn-time-n>

La @fig-cnn-time-k présente les résultats de cette analyse, avec le temps d'exécution en fonction du nombre de sommets bloqué. Nous avons appliqué une régression linéaire, obtenant un coefficient de corrélation linéaire $R^2$ proche de $1$, ce qui confirme la complexité théorique en $O(k^2)$. On note tout de même que la variance est grande sur cette mesure en comparaison à celle observée sur l'évolution en fonction de $n$.

#figure(
  image("figures/cnn_time_plot_k.svg"),
  caption: [
  Évolution du temps d'exécution de l'algorithme CNN sur des instances du TSP générées aléatoirement en fonction du nombre de sommet (25 mesures par taille). La courbe bleue représente la moyenne interquartile et la zone bleutée l'intervalle interquartile. La courbe noire représente le résultat de la regréssion linéaire sur les racines cubiques des IQM, $R^2$ représente le cohéfficient de linéarité, avec des valeur proches de $1$ indiquant une forte corrélation linéaire. On fixe $n$ à $258$.
  ]
) <fig-cnn-time-k>


// parler de l'implementatentation et en particulier des tests unitaires faits pour valider les resultats
// parler du setup experiment, rappeler rapidement comment on genere des graphes complets aleatoires de n noeuds et qui respecte l'inegalite triangulaires, parler de ce comment on genere une liste de k noeuds distincts qui seront bloques pendant l'execution
// parler du rapport d'approximation, discuter le cas des tights bounds, montrer le graphique de ratio des tights bounds avec les methodes de regressions lineaires pour montrer empiriquement la tight bound a log(k) // TODO: lire l'article pour comprendre les tights bounds de CNN et les implementer // TODO: il faut etudier par rapport a n et par rapport a k, normalement O(log k) pour k et O(1) pour n
// - parler de la complexite de cnn et montrer le graphique // TODO: il faut trouver la complexite reelle de CNN pour faire cela (dominée par celle de Christofides) donc probablement tres courte, il me semble que c'est genre O(n + k) donc O(n) (ou un truc du genre, probablement pas plus), de meme il faut etudier la complexite en fonction de k et en fonction de n

== Comparaisons

// TODO: ecrire la partie de comparative entre CR et CNN
// on étudie 4 classes distinctes de graphes pour étudier le comportement des algorithmes
//  - graphes basés sur des distances euclidiennes
//  - graphes en grilles (Manhattan) avec inégalité triangulaire stricte
//  - graphes fortement clusterisés (communautés avec distances courtes intra-cluster et longuers inter-clusters)
//  - graphes asé sur des loi de puissances
//  - graphes basés sur des données réelles
// pour chaque classes de problème, étudier :
//  - évolution du ratio d'approximation empirique en fonction de n
//  - évolution du ratio d'approximation empirique en fonction de k
//  - analyse du temps d'éxécution
//  - breve analyse et discussion de la variation de l'iqm et du max mesuré.
// discuter de l'avantage et désavantage de CR et CNN sur des cas pratiques.
// proposer une recommendation générale sur quel algorithme à utiliser dans quel contexte

== Conclusion

// TODO: resumer les resultats
