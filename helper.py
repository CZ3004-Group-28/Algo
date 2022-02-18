from consts import WIDTH, HEIGHT, Direction


def is_valid(center_x: int, center_y: int):
    return center_x > 0 and center_y > 0 and center_x < WIDTH - 1 and center_y < HEIGHT - 1


def command_generator(states):
    commands = []

    for i in range(1, len(states)):
        if states[i].direction == states[i - 1].direction:
            if (states[i].x > states[i - 1].x and states[i].direction == Direction.EAST) or (
                    states[i].y > states[i - 1].y and states[i].direction == Direction.NORTH):

                commands.append("FW10")

            elif (states[i].x < states[i-1].x and states[i].direction == Direction.WEST) or(
                    states[i].y < states[i-1].y and states[i].direction == Direction.SOUTH):
                commands.append("FW10")

            else:
                commands.append("BW10")
        elif states[i - 1].direction == Direction.NORTH:
            if states[i].direction == Direction.EAST:
                # assume there are 4 turning command: FR, FL, BL, BR (the turn command will turn the car 90 degree)
                # FR00: Forward Right;
                # FL00: Forward Left;
                # BR00: Backward Right;
                # BL00: Backward Left;
                if states[i].y > states[i - 1].y:
                    commands.append("FR00")
                else:
                    commands.append("BL00")
            elif states[i].direction == Direction.WEST:
                if states[i].y > states[i - 1].y:
                    commands.append("FL00")
                else:
                    commands.append("BR00")
            else:
                raise Exception("Invalid turing direction")
        elif states[i - 1].direction == Direction.EAST:
            if states[i].direction == Direction.NORTH:
                if states[i].y > states[i - 1].y:
                    commands.append("FL00")
                else:
                    commands.append("BR00")
            elif states[i].direction == Direction.SOUTH:
                if states[i].y > states[i - 1].y:
                    commands.append("BL00")
                else:
                    commands.append("FR00")
            else:
                raise Exception("Invalid turing direction")
        elif states[i - 1].direction == Direction.SOUTH:
            if states[i].direction == Direction.EAST:
                if states[i].y > states[i - 1].y:
                    commands.append("BR00")
                else:
                    commands.append("FL00")
            elif states[i].direction == Direction.WEST:
                if states[i].y > states[i - 1].y:
                    commands.append("BL00")
                else:
                    commands.append("FR00")
            else:
                raise Exception("Invalid turing direction")
        elif states[i - 1].direction == Direction.WEST:
            if states[i].direction == Direction.NORTH:
                if states[i].y > states[i - 1].y:
                    commands.append("FR00")
                else:
                    commands.append("BL00")
            elif states[i].direction == Direction.SOUTH:
                if states[i].y > states[i - 1].y:
                    commands.append("BR00")
                else:
                    commands.append("FL00")
            else:
                raise Exception("Invalid turing direction")
        else:
            raise Exception("Invalid position")

        if states[i].screenshot_id != -1: # take picture command
            commands.append("SNAP{}".format(states[i].screenshot_id))

    commands.append("FIN") # issue the stop signal
    return commands
