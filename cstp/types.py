"""Type definitions for TSP algorithm implementations.

This module provides type aliases used throughout the TSP solver implementation
to improve code readability and type safety.
"""

# Node represents a vertex in the graph
Node = int

# Weight represents the cost of traversing an edge
Weight = float

# Edge represents a connection between two nodes
Edge = tuple[Node, Node]

# Path represents a sequence of nodes to visit
Path = list[Node]
