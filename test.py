import ipdb

class GameObject:
    def __init__(self, body_color) -> None:
        self.position = 1
        self.body_color = body_color


class Apple(GameObject):
    def __init__(self, body_color):
        super().__init__(body_color)
        ipdb.set_trace()

apple = Apple('jashil')



def move(self):
        x, y = self.get_head_position()
        if self.direction == UP:
            new_coordinat = (x, y-GRID_SIZE)
            if new_coordinat[1] < 0:
                new_coordinat = (x, 480)
        if self.direction == DOWN:
            new_coordinat = (x, y+GRID_SIZE)
            if new_coordinat[1] > 480:
                new_coordinat = (x, 0)
        if self.direction == LEFT:
            new_coordinat = (x-GRID_SIZE, y)
            if new_coordinat[0] < 0:
                new_coordinat = (640, y)
        if self.direction == RIGHT:
            new_coordinat = (x+GRID_SIZE, y)
            if new_coordinat[0] > 640:
                new_coordinat = (0, y)

        if new_coordinat in self.positions:
            self.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        else:
            self.positions.insert(0, new_coordinat)
            if len(self.positions) > self.length:
                self.last = self.positions[-1]
                self.positions.pop(-1)


