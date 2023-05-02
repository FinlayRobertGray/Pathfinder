import pygame as py
from queue import PriorityQueue
import sys



scr_w = 700
scr_h = 700
rows = int(scr_w * 0.05)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

screen = py.display.set_mode((scr_w, scr_h))

py.display.set_caption('Pathfinder')


class Block():

    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.colour = BLACK
        self.near = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        x = self.x * self.width
        y = self.y * self.width
        return x, y

    def get_row_col(self):
        return self.row, self.col

    def is_open(self):
        return self.colour == ORANGE

    def closed(self):
        return self.colour == RED

    def is_start(self):
        return self.colour == GREEN

    def is_end(self):
        return self.colour == BLUE

    def is_barrier(self):
        return self.colour == WHITE

    def make_start(self):
        self.colour = GREEN

    def make_end(self):
        self.colour = BLUE

    def make_barrier(self):
        self.colour = WHITE

    def make_closed(self):
        self.colour = RED

    def make_open(self):
        self.colour = ORANGE

    def make_path(self):
        self.colour = PURPLE

    def draw(self, screen):
        py.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.width))

    def update_near(self, grid):
        self.near = []
        # check if can go down
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.near.append(grid[self.row + 1][self.col])
        # check if can go up
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.near.append(grid[self.row - 1][self.col])
        # check if can go left
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.near.append(grid[self.row][self.col - 1])
        # check if can go right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.near.append(grid[self.row][self.col + 1])


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Block(i, j, gap, rows)

            grid[i].append(node)

    return grid


def draw_grid(screen, rows, width):
    gap = width // rows
    for i in range(rows):
        py.draw.line(screen, WHITE, (0, i * gap), (width, i * gap))
        for j in range(rows):
            py.draw.line(screen, WHITE, (j * gap, 0), (j * gap, width))


def draw(screen, grid, rows, width):
    screen.fill(BLACK)

    for row in grid:
        for block in row:
            block.draw(screen)

    draw_grid(screen, rows, width)
    py.display.update()


def get_pos_mouse(pos, rows, width):
    size = width // rows
    x, y = pos
    rows = x // size
    cols = y // size

    return rows, cols


def final_path(came_from, current, draw, start, end):
    count = 0
    while current in came_from:
        current = came_from[current]
        current.make_path()
        start.colour = GREEN
        end.colour = BLUE
        count +=1
        draw()
    print(count)


def main_algorithm(draw, grid, start, end):
    count = 0
    queue = PriorityQueue()
    queue.put((0, count, start))
    came_from = {}
    g_score = {block: float("inf") for row in grid for block in row}
    g_score[start] = 0
    f_score = {block: float("inf") for row in grid for block in row}
    f_score[start] = h(start.get_row_col(), end.get_row_col())

    queue_track = {start}

    while not queue.empty():
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()

        current = queue.get()[2]
        queue_track.remove(current)

        if current == end:
            final_path(came_from, end, draw, start, end)
            return True
        for node in current.near:
            temp_g = g_score[current] + 1
            if temp_g < g_score[node]:
                came_from[node] = current
                g_score[node] = temp_g

                f_score[node] = temp_g + h(node.get_row_col(), end.get_row_col())
                if node not in queue_track:
                    count += 1
                    queue.put((f_score[node], count, node))
                    queue_track.add(node)
                    node.make_open()
        draw()
        if current != start:
            current.make_closed()
    return False


def main():
    g = make_grid(rows, scr_w)
    start = None
    end = None
    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()

            if py.mouse.get_pressed()[0]:
                pos = py.mouse.get_pos()
                x, y = get_pos_mouse(pos, rows, scr_w)
                block = g[x][y]

                if block != start and block != end:
                    block.make_barrier()

            if event.type == py.KEYDOWN:
                pos = py.mouse.get_pos()
                x, y = get_pos_mouse(pos, rows, scr_w)
                block = g[x][y]
                if event.key == py.K_s:
                    if not start and block != end:
                        start = block
                        block.make_start()

                elif event.key == py.K_e:
                    if not end and block != start:
                        end = block
                        block.make_end()
                elif event.key == py.K_SPACE and start and end:
                    for row in g:
                        for block in row:
                            block.update_near(g)
                    main_algorithm(lambda: draw(screen, g, rows, scr_w), g, start, end)

                elif event.key == py.K_c:
                    start = None
                    end = None
                    g = make_grid(rows, scr_w)

        draw(screen, g, rows, scr_w)

        py.display.update()


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


if __name__ == '__main__':
    main()
