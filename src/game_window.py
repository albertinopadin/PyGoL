import arcade
from arcade import color, draw_rectangle_filled
from cell_grid import CellGrid


WINDOW_TITLE        = "PyGoL"
ROWS                = 90
COLUMNS             = 150
CELL_SIZE           = 4
CELL_MARGIN         = 4
SCREEN_WIDTH        = (CELL_SIZE + CELL_MARGIN) * COLUMNS + CELL_MARGIN
SCREEN_HEIGHT       = (CELL_SIZE + CELL_MARGIN) * ROWS + CELL_MARGIN
BACKGROUND_COLOR    = color.DARK_SLATE_GRAY
ALIVE_COLOR         = color.GREEN
ALPHA_ON            = 255
ALPHA_OFF           = 0


def create_sprite_list_and_grid(rows, columns):
    sprite_list = arcade.SpriteList()
    sprite_grid = []

    for row in range(rows):
        sprite_grid.append([])
        for col in range(columns):
            # cell_sprite = arcade.SpriteCircle(CELL_SIZE, ALIVE_COLOR, soft=True)
            cell_sprite = arcade.SpriteCircle(CELL_SIZE, ALIVE_COLOR, soft=False)
            x = col * (CELL_SIZE + CELL_MARGIN) + (CELL_SIZE/2 + CELL_MARGIN)
            y = row * (CELL_SIZE + CELL_MARGIN) + (CELL_SIZE/2 + CELL_MARGIN)
            cell_sprite.center_x = x
            cell_sprite.center_y = y
            sprite_list.append(cell_sprite)
            sprite_grid[row].append(cell_sprite)

    return sprite_list, sprite_grid


class PyGoL(arcade.Window):
    
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(BACKGROUND_COLOR)
        self.sprite_list, self.sprite_grid = create_sprite_list_and_grid(ROWS, COLUMNS)
        self.cell_grid = CellGrid(ROWS, COLUMNS)
        self.randomize()

    
    def randomize(self):
        self.cell_grid.randomize()
        for x in range(ROWS):
            for y in range(COLUMNS):
                if self.cell_grid.grid[x][y] == 1:
                    self.sprite_grid[x][y].alpha = ALPHA_ON


    def on_draw(self):
        arcade.start_render()
        self.sprite_list.draw()

    
    def on_update(self, delta_time):
        self.cell_grid.update()
        for x in range(ROWS):
            for y in range(COLUMNS):
                if self.cell_grid.grid[x][y] == 1:
                    self.sprite_grid[x][y].alpha = ALPHA_ON
                else:
                    self.sprite_grid[x][y].alpha = ALPHA_OFF


def main():
    window = PyGoL(SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE)
    window.center_window()
    arcade.run()


if __name__=='__main__':
    main()
