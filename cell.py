class Cell:

    def __init__(self, row, column):
        self._row: int = row
        self._column: int = column

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
