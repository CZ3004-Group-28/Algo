from consts import WIDTH, HEIGHT, Direction


def is_valid(center_x: int, center_y: int):
    return center_x > 0 and center_y > 0 and center_x < WIDTH - 1 and center_y < HEIGHT - 1


def command_generator(states):
    commands = []

    for i in range(1, len(states)):
        if states[i].direction == states[i - 1].direction:
            if (states[i].x > states[i - 1].x and states[i].direction == Direction.EAST) or (
                    states[i].y > states[i - 1].y and states[i].direction == Direction.NORTH):

                commands.append("F010")
            else:
                commands.append("B010")
        elif states[i - 1].direction == Direction.NORTH:
            if states[i].direction == Direction.EAST:
                # assume the format of turning command is T + backward/forward + degree of turning.
                # backward is 1 and forward is 0.
                # degree of turning is the angle forming with the left most one. For now, assume 20 is left, 60 is right
                if states[i].y > states[i - 1].y:
                    commands.append("T060")
                else:
                    commands.append("T120")
            elif states[i].direction == Direction.WEST:
                if states[i].y > states[i - 1].y:
                    commands.append("T020")
                else:
                    commands.append("T160")
            else:
                raise Exception("Invalid turing direction")
        elif states[i - 1].direction == Direction.EAST:
            if states[i].direction == Direction.NORTH:
                if states[i].y > states[i - 1].y:
                    commands.append("T020")
                else:
                    commands.append("T160")
            elif states[i].direction == Direction.SOUTH:
                if states[i].y > states[i - 1].y:
                    commands.append("T120")
                else:
                    commands.append("T060")
            else:
                raise Exception("Invalid turing direction")
        elif states[i - 1].direction == Direction.SOUTH:
            if states[i].direction == Direction.EAST:
                if states[i].y > states[i - 1].y:
                    commands.append("T160")
                else:
                    commands.append("T020")
            elif states[i].direction == Direction.WEST:
                if states[i].y > states[i - 1].y:
                    commands.append("T120")
                else:
                    commands.append("T060")
            else:
                raise Exception("Invalid turing direction")
        elif states[i - 1].direction == Direction.WEST:
            if states[i].direction == Direction.NORTH:
                if states[i].y > states[i - 1].y:
                    commands.append("T060")
                else:
                    commands.append("T120")
            elif states[i].direction == Direction.SOUTH:
                if states[i].y > states[i - 1].y:
                    commands.append("T160")
                else:
                    commands.append("T020")
            else:
                raise Exception("Invalid turing direction")
        else:
            raise Exception("Invalid position")

    return commands
