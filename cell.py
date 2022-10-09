from typing import List


class Cell:

    def __init__(self, row, column):
        self._row: int = row
        self._column: int = column
        self._neighbours: List['Cell'] = list()

    @property
    def row(self) -> int:
        return self._row

    @property
    def column(self) -> int:
        return self._column

    def __hash__(self):
        return hash((self.row, self.column))

    def __eq__(self, other: 'Cell') -> bool:
        return other.row == self.row and other.column == self.column

    def __repr__(self) -> str:
        return f'Cell({self.row}, {self.column})'

    def __str__(self) -> str:
        return self.__repr__()

    @property
    def neighbours(self) -> List['Cell']:
        return self._neighbours

    def add_neighbour(self, cell: 'Cell'):
        if cell not in self._neighbours:
            self._neighbours.append(cell)
