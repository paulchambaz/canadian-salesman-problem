#import "template.typ": report
#show: report.with(
  title: [
    Projet de RP
  ],
  authors: (
    (
      "Paul Chambaz", "Philipp Hanussek"
    )
  )
)

= Introduction

= Algorithme de Christofides


= Cyclic Routing
L'idée derrière l'algorithme de Liao et al. est de partitionner le tour entier du graphe en plusieurs tours partiels. Dans chaque tour partiel, le voyageur canadien essaie de visiter un nombre maximum des noeuds non-visités dans le sens d'un tour de Christofides.  
L'algorithme peut être utilisé si les conditions suivantes sont réunies :
- un blockage ne change pas après être détecté par le voyageur
- le graphe initial avec blockages enlevés reste un graphe connexe.

== Tests unitaires 

=== Validité du chemin retourné 
Pour valider que le chemin retourné par l'algorithme est une solution valide, on vérifie les trois conditions suivantes :
+ le tour commence et termine au même noeud
+ le tour contient tous les noeuds du graphe initial
+ le tour ne contient pas des chemins bloqués
*Résultat*: Nos tests valident toutes les conditions indiqués pour des graphes de taille n avec n élément [4,256] et un nombre de blockages k, k élément [0,n-2], n et k tirés aléatoirement uniformement pour 200 itérationsxx.

=== Tests de performance


= CNN 
#lorem(200)