__all__ = [
    "Graph",
]

from random import choice
from typing import Any, Dict, FrozenSet, Iterable, List, Optional, Set, Tuple

import networkx
from matplotlib import pyplot

from rules import people_rules
from utils import collection


class Graph(networkx.Graph):
    nodes_positions: Dict[Any, Iterable[float]]
    solution: Optional[Tuple[Tuple[str, str], ...]] = None

    def __init__(
        self,
        pairs: Optional[FrozenSet[FrozenSet[str]]] = None,
        incoming_graph_data=None,
        **attr,
    ) -> None:
        super().__init__(incoming_graph_data=incoming_graph_data, **attr)
        if pairs is not None:
            self.add_pairs(pairs)
            self.solution = self.find_solution()

    @staticmethod
    def _convert_edges_path_to_edges_sequence(
        edges_path: List[str],
    ) -> Iterable[Tuple[str, str]]:
        n = len(edges_path)
        for i in range(n - 1):
            yield (edges_path[i], edges_path[i + 1])

    def add_pair(self, pair: Tuple[str, str]) -> None:
        self.add_edge(pair[0], pair[1])

    def add_pairs(self, pairs: FrozenSet[FrozenSet[str]]) -> None:
        for pair in pairs:
            p = tuple(pair)
            self.add_pair((p[0], p[1]))

    def add_person(self, person: str) -> None:
        self.add_node(person)

    def close_solution(self) -> Optional[Tuple[Tuple[str, str], ...]]:
        if self.solution is not None:
            people_with_single_connection = (
                self.people_with_single_connection_in_solution
            )
            if people_with_single_connection is not None:
                is_pair_possible = self.has_edge(*people_with_single_connection)
                if is_pair_possible:
                    person1 = next(
                        iter(people_with_single_connection - {self.solution[0][0]})
                    )
                    person2 = next(iter(people_with_single_connection - {person1}))
                    pair = (person1, person2)
                    self.solution = self.solution + (pair,)

        return self.solution

    # TODO: implement depth first algorithm where stop criteria = random starting node
    def find_solution(self) -> Optional[Tuple[Tuple[str, str], ...]]:
        self.solution = self.hamiltonian_path()

        # TODO: remove this block after testing, since it forces a group of solutions
        # FIXME: the code may be stuck in this block loop even if solution is random
        people_with_single_connection = self.people_with_single_connection_in_solution
        while (
            people_with_single_connection is None
            or "LL" in people_with_single_connection
            or "EJ" in people_with_single_connection
        ):
            self.solution = self.hamiltonian_path()
            people_with_single_connection = (
                self.people_with_single_connection_in_solution
            )

        self.solution = self.close_solution()
        return self.solution

    def hamiltonian_path(self) -> Optional[Tuple[Tuple[str, str], ...]]:
        random_node = choice(list(self.nodes()))  # nosec
        F = [(self, [random_node])]
        n = self.number_of_nodes()
        while F:
            graph, path = F.pop()
            confs = []
            neighbors = (
                node for node in graph.neighbors(path[-1]) if node != path[-1]
            )  # exclude self loops
            for neighbor in neighbors:
                conf_p = path[:]
                conf_p.append(neighbor)
                conf_g = networkx.Graph(graph)
                conf_g.remove_node(path[-1])
                confs.append((conf_g, conf_p))
            for g, p in confs:
                if len(p) == n:
                    return tuple(self._convert_edges_path_to_edges_sequence(p))
                else:
                    F.append((g, p))
        return None

    @property
    def pairs(self) -> FrozenSet[FrozenSet[str]]:
        return frozenset((frozenset(edge) for edge in self.edges))

    @property
    def pairs_in_solution(self) -> Optional[FrozenSet[FrozenSet[str]]]:
        if self.solution is None:
            return None

        return frozenset((frozenset(pair) for pair in self.solution))

    @property
    def people_in_solution(self) -> Optional[FrozenSet[str]]:
        if self.solution is None:
            return None

        people: Set[str] = set()
        for pair in self.solution:
            people.add(pair[0])
            people.add(pair[1])
        return frozenset(people)

    @property
    def people(self) -> FrozenSet[str]:
        return frozenset(self.nodes)

    @property
    def people_not_in_pairs(self) -> FrozenSet[str]:
        return people_rules.get_people_not_in_pairs(
            people=self.people,
            pairs=self.pairs,
        )

    @property
    def people_not_in_solution(self) -> Optional[FrozenSet[str]]:
        if self.solution is None:
            return None

        return people_rules.get_people_not_in_collection(
            people=self.people,
            collection=self.people_in_solution,
        )

    @property
    def people_with_single_connection_in_solution(self) -> Optional[FrozenSet[str]]:
        if self.solution is None:
            return None

        path_people_repeating_sequence = [
            person for pair in self.solution for person in pair
        ]
        return collection.get_non_repeated_items(path_people_repeating_sequence)

    def show(self) -> None:
        self.nodes_positions = networkx.circular_layout(self)
        if self.solution is None:
            self.solution = self.hamiltonian_path()

        pyplot.plot()
        networkx.draw(
            self,
            pos=self.nodes_positions,
            with_labels=True,
        )
        networkx.draw_networkx_edges(
            self,
            pos=self.nodes_positions,
            edgelist=self.solution,
            edge_color="red",
            width=2,
        )
        networkx.draw_networkx_nodes(
            self,
            pos=self.nodes_positions,
            nodelist=self.people_with_single_connection_in_solution,
            node_color="red",
        )
        pyplot.show()
