from consts import WIDTH, HEIGHT, Direction


def is_valid(center_x: int, center_y: int):
    return center_x > 0 and center_y > 0 and center_x < WIDTH - 1 and center_y < HEIGHT - 1


def command_generator(states, mode):
    commands = []

    for i in range(1, len(states)):
        steps = "00"
        if states[i].direction == states[i - 1].direction:
            if (states[i].x > states[i - 1].x and states[i].direction == Direction.EAST) or (
                    states[i].y > states[i - 1].y and states[i].direction == Direction.NORTH):

                if mode == 0:
                    commands.append("FW10")
                else:
                    commands.append("FS10")

            elif (states[i].x < states[i-1].x and states[i].direction == Direction.WEST) or(
                    states[i].y < states[i-1].y and states[i].direction == Direction.SOUTH):
                if mode == 0:
                    commands.append("FW10")
                else:
                    commands.append("FS10")

            else:
                if mode == 0:
                    commands.append("BW10")
                else:
                    commands.append("BS10")

            if states[i].screenshot_id != -1:
                commands.append("SNAP{}".format(states[i].screenshot_id))
            continue

        else:
            if abs(states[i].x - states[i-1].x) in [2, 4]:
                steps = "30"
        # assume there are 4 turning command: FR, FL, BL, BR (the turn command will turn the car 90 degree)
        # FR00 | FR30: Forward Right;
        # FL00 | FL30: Forward Left;
        # BR00 | BR30: Backward Right;
        # BL00 | BL30: Backward Left;
        if states[i - 1].direction == Direction.NORTH:
            if states[i].direction == Direction.EAST:
                if states[i].y > states[i - 1].y:
                    commands.append("FR{}".format(steps))
                else:
                    commands.append("BL{}".format(steps))

            elif states[i].direction == Direction.WEST:
                if states[i].y > states[i - 1].y:
                    commands.append("FL{}".format(steps))
                else:
                    commands.append("BR{}".format(steps))
            else:
                raise Exception("Invalid turing direction")

        elif states[i - 1].direction == Direction.EAST:
            if states[i].direction == Direction.NORTH:
                if states[i].y > states[i - 1].y:
                    commands.append("FL{}".format(steps))
                else:
                    commands.append("BR{}".format(steps))

            elif states[i].direction == Direction.SOUTH:
                if states[i].y > states[i - 1].y:
                    commands.append("BL{}".format(steps))
                else:
                    commands.append("FR{}".format(steps))
            else:
                raise Exception("Invalid turing direction")

        elif states[i - 1].direction == Direction.SOUTH:
            if states[i].direction == Direction.EAST:
                if states[i].y > states[i - 1].y:
                    commands.append("BR{}".format(steps))
                else:
                    commands.append("FL{}".format(steps))
            elif states[i].direction == Direction.WEST:
                if states[i].y > states[i - 1].y:
                    commands.append("BL{}".format(steps))
                else:
                    commands.append("FR{}".format(steps))
            else:
                raise Exception("Invalid turing direction")

        elif states[i - 1].direction == Direction.WEST:
            if states[i].direction == Direction.NORTH:
                if states[i].y > states[i - 1].y:
                    commands.append("FR{}".format(steps))
                else:
                    commands.append("BL{}".format(steps))
            elif states[i].direction == Direction.SOUTH:
                if states[i].y > states[i - 1].y:
                    commands.append("BR{}".format(steps))
                else:
                    commands.append("FL{}".format(steps))
            else:
                raise Exception("Invalid turing direction")
        else:
            raise Exception("Invalid position")

        if states[i].screenshot_id != -1: # take picture command
            commands.append("SNAP{}".format(states[i].screenshot_id))

    commands.append("FIN") # issue the stop signal

    compressed_commands = [commands[0]]

    for i in range(1, len(commands)):
        if commands[i].startswith("BW") and compressed_commands[-1].startswith("BW"):
            steps = int(compressed_commands[-1][2:])
            if steps != 90:
                compressed_commands[-1] = "BW{}".format(steps + 10)
                continue

        if commands[i].startswith("BS") and compressed_commands[-1].startswith("BS"):
            steps = int(compressed_commands[-1][2:])
            if steps != 90:
                compressed_commands[-1] = "BS{}".format(steps + 10)
                continue

        elif commands[i].startswith("FW") and compressed_commands[-1].startswith("FW"):
            steps = int(compressed_commands[-1][2:])
            if steps != 90:
                compressed_commands[-1] = "FW{}".format(steps + 10)
                continue

        elif commands[i].startswith("FS") and compressed_commands[-1].startswith("FS"):
            steps = int(compressed_commands[-1][2:])
            if steps != 90:
                compressed_commands[-1] = "FS{}".format(steps + 10)
                continue

        compressed_commands.append(commands[i])

    return compressed_commands
