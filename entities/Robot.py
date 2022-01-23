from entities.Entity import CellState
from consts import Direction


class Robot:
    def __init__(self, center_x: int, center_y: int, start_direction: Direction):
        self.states: [CellState] = [CellState(center_x, center_y, start_direction)]

    def get_current_state(self):
        return self.states[-1]

    def get_start_state(self):
        return self.states[0]

    def update_state(self, x, y, direction: Direction) -> CellState:
        new_state = CellState(x, y, direction)
        self.states.append(new_state)
        return new_state

    def clockwise(self) -> CellState:
        current_state = self.get_current_state()
        new_direction = Direction.clockwise(current_state.direction)
        return self.update_state(current_state.x, current_state.y, new_direction)

    def anti_clockwise(self) -> CellState:
        current_state = self.get_current_state()
        new_direction = Direction.anti_clockwise(current_state.direction)
        return self.update_state(current_state.x, current_state.y, new_direction)

    def move_forward(self) -> CellState:
        current_state = self.get_current_state()

        if current_state.direction == Direction.NORTH:
            return self.update_state(current_state.x, current_state.y + 1, current_state.direction)

        elif current_state.direction == Direction.EAST:
            return self.update_state(current_state.x + 1, current_state.y, current_state.direction)

        elif current_state.direction == Direction.WEST:
            return self.update_state(current_state.x - 1, current_state.y, current_state.direction)

        elif current_state.direction == Direction.SOUTH:
            return self.update_state(current_state.x, current_state.y - 1, current_state.direction)

        elif current_state.direction == Direction.NORTH_EAST:
            return self.update_state(current_state.x + 1, current_state.y + 1, current_state.direction)

        elif current_state.direction == Direction.WEST_NORTH:
            return self.update_state(current_state.x - 1, current_state.y + 1, current_state.direction)

        elif current_state.direction == Direction.SOUTH_WEST:
            return self.update_state(current_state.x - 1, current_state.y - 1, current_state.direction)

        elif current_state.direction == Direction.EAST_SOUTH:
            return self.update_state(current_state.x + 1, current_state.y - 1, current_state.direction)
