import unittest

import christofides_p as cr
import graph_utils as gu
import networkx as nx


class TestCrRouting(unittest.TestCase):
    def test_equality(self):
        for i in range(5, 50):
            print(f"Running for i={i}")

            for _ in range(10):
                connected = False
                G = gu.generer_graphe_tsp(i)
                while not connected:
                    number_of_edges = len(G.edges())
                    k = (i - 2) / number_of_edges
                    len_blockages_less_i = False
                    while not len_blockages_less_i:
                        blockages = gu.generer_blockages(G, percentage=k)
                        len_blockages_less_i = len(blockages) < (i - 1)
                    G_verify = G.copy()
                    G_verify.remove_edges_from(blockages)
                    connected = nx.is_connected(G_verify)
                G_cr_tour = cr.canadian_traveller_cyclic_routing(G, blockages)
                self.assertTrue(nx.has_eulerian_path(G_cr_tour))


if __name__ == "__main__":
    unittest.main()
