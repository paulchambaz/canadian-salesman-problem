import unittest
import christofides_p as cr
import graph_utils as gu
import networkx as nx

class TestCrRouting(unittest.TestCase):
    def test_equality(self):
        for i in range(5,15):
            G = gu.generer_graphe_tsp(i)
            blockages = gu.generer_blockages(G)
            G_cr_tour = cr.canadian_traveller_cyclic_routing(G,blockages)
            self.assertTrue(nx.has_eulerian_path(G)) 



if __name__ == "__main__":
    unittest.main()