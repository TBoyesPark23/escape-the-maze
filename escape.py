from typing import List, Tuple

from mazes import MAZES


class Cell:
    def __init__(self, x, y, reachable):
        self.x = x
        self.y = y
        self.reachable = reachable
        self.parent = None

    def __eq__(self, other):
        if not isinstance(other, Cell):
            return NotImplemented

        return (self.x == other.x) and (self.y == other.y)


class Maze:

    _person = "+"
    _wall = "#"

    def __init__(self, maze: str):
        self.starting_x, self.starting_y = self.find_starting_coordinates(maze)
        self.maze_width = len(maze[0])
        self.maze_height = len(maze)
        self.cells = self.process_maze(maze)
        self.exit = self.find_exit()

    @classmethod
    def process_maze(cls, m: str) -> List[List[Cell]]:
        """Converts a string representation of a maze into Cell objects."""
        return [
            [Cell(x, y, reachable=cell != cls._wall) for x, cell in enumerate(row)]
            for y, row in enumerate(m)
        ]

    @classmethod
    def find_starting_coordinates(cls, maze: str) -> Tuple[int, int]:
        """
        Returns co-ordinates of the char '+' in the given maze. The top left of the
        maze, i.e. maze[0][0], is considered to be co-ordinates (0, 0).
        """
        for y, row in enumerate(maze):
            if cls._person in row:
                return row.index(cls._person), y

        raise Exception(f"Could not find coordinates of character: {cls._person}")

    def find_exit(self) -> Cell:
        """Returns Cell object relating to the exit of the maze."""
        for i, row in enumerate(self.cells):
            if i == 0 or i == self.maze_height - 1:
                reachable_cells = list(filter(lambda c: c.reachable, row))
                if reachable_cells:
                    return reachable_cells[0]

            if row[0].reachable:
                return row[0]

            if row[-1].reachable:
                return row[-1]

        raise Exception("No exit found in maze")

    def get_cell(self, x: int, y: int) -> Cell:
        """Returns Cell object at coordinates (x, y)."""
        return self.cells[y][x]

    def get_reachable_adjacent_cells(self, cell: Cell) -> List[Cell]:
        """
        Returns list of Cells that are adjacent to the given cell and that are
        reachable, i.e. not a wall.
        """
        adj = []

        # have we got a cell to the right?
        if cell.x < self.maze_width - 1:
            adj.append(self.get_cell(cell.x + 1, cell.y))

        # have we got a cell to the left?
        if cell.x > 0:
            adj.append(self.get_cell(cell.x - 1, cell.y))

        # have we got a cell above?
        if cell.y < self.maze_height - 1:
            adj.append(self.get_cell(cell.x, cell.y + 1))

        # have we got a cell below?
        if cell.y > 0:
            adj.append(self.get_cell(cell.x, cell.y - 1))

        return list(filter(lambda c: c.reachable, adj))

    def escape(self) -> List[Cell]:
        """
        Uses a Breadth-first search approach to analyse each cell in the maze.
        """
        print("Solving maze")
        starting_cell = self.get_cell(self.starting_x, self.starting_y)

        # list containing cells to be visited
        queue = [starting_cell]

        # list containing cells we've already visited
        visited = list()

        while queue:
            # sort queue based off "as the crow flies" distance to exit
            queue = sorted(
                queue,
                key=lambda c: abs(c.x - self.exit.x) + abs(c.y - self.exit.y),
            )
            cell = queue.pop(0)

            adj_cells = self.get_reachable_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell in visited:
                    continue

                # link cells (needed to construct path from start to exit once exit
                # found)
                adj_cell.parent = cell

                if adj_cell == self.exit:
                    # construct path by making our way from the exit back to the
                    # starting coordinates via the parent cells
                    path = [adj_cell]
                    while cell != self.get_cell(self.starting_x, self.starting_y):
                        path.append(cell)
                        cell = cell.parent
                    path.append(starting_cell)
                    return list(reversed(path))

                # if adjacent cell is not an exit, then we need to add it to queue so
                # we'll visit it in the next iteration
                queue.append(adj_cell)

            # after checking all adjacent cells, cell is considered visited
            visited.append(cell)

        raise Exception("Cell queue exhausted, no escape found")


def escape():
    """
    Given a string representation of a maze and a starting position, this function will
    return the list of moves required in order to escape the maze.

    The following assumptions can be made about the maze:

      - There is always an exit
      - There is only ever 1 exit
      - The maze is always a valid square or rectangle

    """
    for m in MAZES:
        maze = Maze(m)
        path = maze.escape()
        print(path)


if __name__ == "__main__":
    escape()
