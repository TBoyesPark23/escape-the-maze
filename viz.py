from PIL import Image

from escape import Maze
from mazes import MAZES

WHITE_RGB = (255, 255, 255)
BLACK_RGB = (0, 0, 0)
BLUE_RGB = (51, 153, 255)


class MazeVisualiser:
    def __init__(self, maze: Maze):
        self.maze = maze
        self.escape_path = maze.escape()

    def escape_gif(self, fname: str):
        print(f"Creating escape gif: {fname}")
        # create new image using maze dimensions with a white background
        img = Image.new(
            "RGB", (self.maze.maze_width, self.maze.maze_height), color=WHITE_RGB
        )
        pixels = img.load()

        # loop through maze cells setting black pixels where cell is not reachable
        for y, row in enumerate(self.maze.cells):
            for x, cell in enumerate(row):
                if not cell.reachable:
                    pixels[x, y] = BLACK_RGB

        # create the frames for the gif
        frames = [img]
        for cell in self.escape_path:
            frame = frames[-1].copy()
            pixels = frame.load()
            pixels[cell.x, cell.y] = BLUE_RGB
            frames.append(frame)

        # resize so they're not frames for ants
        frames = [
            frame.resize(
                (self.maze.maze_width * 10, self.maze.maze_height * 10), Image.BOX
            )
            for frame in frames
        ]

        frames[0].save(
            fname,
            format="GIF",
            append_images=frames[1:],
            save_all=True,
        )


def main():
    for i, m in enumerate(MAZES):
        maze_visualiser = MazeVisualiser(maze=Maze(m))
        maze_visualiser.escape_gif(f"escape_{i}.gif")


if __name__ == "__main__":
    main()
