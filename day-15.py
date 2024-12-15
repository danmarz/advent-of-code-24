def simulate_warehouse(map_lines, moves):
    # Convert map to a mutable structure
    warehouse = [list(row) for row in map_lines]

    # Find robot position
    robot_r, robot_c = None, None
    for r in range(len(warehouse)):
        for c in range(len(warehouse[r])):
            if warehouse[r][c] == "@":
                robot_r, robot_c = r, c

    direction_map = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}

    def is_wall(r, c):
        return warehouse[r][c] == "#"

    def is_box(r, c):
        return warehouse[r][c] == "O"

    def is_empty(r, c):
        return warehouse[r][c] == "."

    rows = len(warehouse)
    cols = len(warehouse[0])

    # Normalize moves by removing any newlines
    moves = moves.replace("\n", "")

    for move in moves:
        dr, dc = direction_map[move]
        nr, nc = robot_r + dr, robot_c + dc

        # Check boundaries and conditions
        if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
            # Out of bounds, skip
            continue

        if is_wall(nr, nc):
            # Movement blocked by wall
            continue
        elif is_empty(nr, nc):
            # Just move the robot
            warehouse[robot_r][robot_c] = "."
            warehouse[nr][nc] = "@"
            robot_r, robot_c = nr, nc
        elif is_box(nr, nc):
            # Attempt to push chain of boxes
            chain = []
            cur_r, cur_c = nr, nc

            # Collect all consecutive boxes in the direction of the push
            while 0 <= cur_r < rows and 0 <= cur_c < cols and is_box(cur_r, cur_c):
                chain.append((cur_r, cur_c))
                cur_r += dr
                cur_c += dc

            # Now (cur_r, cur_c) should be the cell after the last box
            if not (0 <= cur_r < rows and 0 <= cur_c < cols):
                # Pushing out of bounds, can't push
                continue

            if not is_empty(cur_r, cur_c):
                # The cell after chain of boxes is not empty, can't push
                continue

            # If we are here, we can push.
            # Steps:
            # 1) Remove robot from old position
            warehouse[robot_r][robot_c] = "."
            # 2) Robot moves into the first box's old position
            first_box_r, first_box_c = chain[0]
            warehouse[first_box_r][first_box_c] = "@"
            # Update robot coordinates
            robot_r, robot_c = first_box_r, first_box_c

            # 3) For each subsequent box, move it into the position of the next box
            # chain[i] moves to chain[i+1]'s old position, and the last box moves into (cur_r, cur_c)
            # Before moving them, clear their old positions
            # Actually, we don't need to pre-clear them if we overwrite carefully:

            # Move boxes forward:
            # The first box is now occupied by the robot, so no need to put a box there.
            # chain[1] should move into chain[0]'s old position, but chain[0]'s old position is now occupied by robot.
            # Careful! The description:
            # The robot attempts to move into chain[0]'s cell.
            # The chain[0] box moves into chain[1]'s cell.
            # ...
            # The chain[-1] box moves into (cur_r, cur_c).

            # Correct approach:
            # After pushing:
            # - The robot ends up at chain[0]'s old position.
            # - chain[0] box moves to chain[1]'s old position.
            # - chain[1] box moves to chain[2]'s old position.
            # ...
            # - chain[-2] box moves to chain[-1]'s old position.
            # - chain[-1] box moves to (cur_r, cur_c).

            # Let's do this from the end:
            # Place last box in the empty cell
            warehouse[cur_r][cur_c] = "O"
            # Shift all other boxes forward
            for i in range(len(chain) - 1, 0, -1):
                prev_r, prev_c = chain[i - 1]  # from
                curr_r, curr_c = chain[i]  # to
                warehouse[curr_r][curr_c] = "O"  # move box forward
            # The first box position is now occupied by robot, so we do not place a box there.

            # We have successfully pushed.

    # After all moves, calculate the sum of GPS coordinates for boxes
    total = 0
    for r in range(rows):
        for c in range(cols):
            if warehouse[r][c] == "O":
                gps = 100 * r + c
                total += gps
    return total


data = """##################################################
#..O.O..#..O.O.O.O.......##O..OOO.....O...O..#..O#
#.O.O.#.....O..O......O.O.OOO.......OO.O.....#...#
#OO........O.....OO......##OO.#OO.OO..O....OOO...#
#......O...O..O.#....O...O.....O..#.O.O.O...#O...#
#OOO.OO.OO...####O.#O...O..OO...O#.O..#.OO.O...O.#
#O#...OOOO......O#O#....#OO...O.....O.O.OOO.OOO..#
#O.O...O.#OO......#...........O...OO.O..O#.#OO...#
#O.....O.O.O.#...OO..O#....OO.O.O....#.........O.#
#.O.#O.O#...O#..O.O.#.O.OO..O..O...O.O...OO.O...O#
#..#..O.#.O..##......OO...........O.....O...#.#..#
#.OO#.........O...O.....OO.O...OO............O#.O#
##.O.OO.O...O.O..O..OO.#....O.#....O......OOO...O#
#..OO..O.O..O..O..O...O..O.....#OO.....O...#OOO.O#
#.......O.#O.OO..#......O..OO.......O..O.O....OO##
#.....O.........O...#.O..O..#OO.O...O.O.#....O...#
#.OO##O#..O.#..O......OO..OO.OO.....O..OO#O.O..O##
#.O....O...#O.O..O#....O#O...OO.....O....O.......#
#...OOO....#O.OO...#.OO#O...O#O..#..#.O..O....#..#
##....O.OO.O#..........O#.OOO.#....#...O#....OO..#
#.#OOO..OO..O.......#.OO.O..#O.#.OO....OO.O.....O#
#.O......#..O.#.O..........#O..O.OO...#O...O#....#
#.#....O.O....O.......O..OOO..OO...OO.#OOO.O.O.#.#
#.O.#.O.O....OOO...O...O#......OO##.O..OO.....O..#
#.OO.......#O.OO#..#....@O...O....OOO.O..OO......#
#O..#..#OO...O#OO.......OO..##..O.#.O.O..O.O..OO.#
#.#.O.OO.........OO#.O..O.O...OOO.O......O#...OO.#
#.OO...#..OO.##......O#.O.OO....O..O#.......O.OO##
#OO..O.O.O....O#.O..O......#...OO#.O..O.O..O..OOO#
#...OO....OOO.....O..O..O....OO......OOO.........#
#O...#.....O...O..OO..O.OO....O.O..O....O....O.O.#
#.....OOOO..#..#.O.OO.......O....OO#.O...O..O..O.#
##.OO...O.#O......#O.O#O#..O#..O.....O....OO..O.##
#..O..OOO...OO.OO.#O#.OOO......O...OO...O.O......#
#.OO.O..O.O.O#..O.#.O.OOO...O..OO.O##.O.#...#...O#
#........#...O##.....OO....O.O....OO#.O.O.O.#OO.O#
#.O..O.O.#...O.......#...#..O...O.#.........#..O##
#...........O.....O..OO.......#..#...O...#..O.##O#
#.OOO..O..OO....#..OOOO......O...##..#.......O...#
##..#O..OOO.#O...O..OO...O....OO..#..#.OO.O.OO...#
##O....#...OO#.O.O...O...O.O..O.......O.....O..#.#
#........#.O##...O#..O..O.#O........O#..OO#.O.O###
#....#.O............O..O...OO....OOO...OO...#....#
#.#O.....#...OO.OO.........#.#.OOO.OO.O...O#.O.#.#
##....#..OO...O...O..#O..O.O..O.O..O..O.OO.......#
#...........OO.O.O...O......O...O.OOO.....O..O...#
##O.O..O.O...O.....O.O.O.O.OO.#O.O.O..#.....#....#
##.O.......#O.#...O#O#O..O..#O..O....OO.O.O......#
#O...O.O.........O......O.......O......#..O.....##
##################################################"""

data = data.splitlines()
moves = """^>>^v><^>v>>^v^^^v<>>v><vvv<>v^>>v><<<>^<<v^>vvvv^v^>v^>>^<v><>vv^>^>^v<^v^v<<<<^<>v<<>vv<>^vv<^v><^^>^>^v>>^>^v>>>v<<^>^>^<^<><^vvv<<^vvv>v<v<<>v^><<v^<>v^v^^^>v^<^v<vv^v^>>^^<<>^><<<>>>^v^>vv><<>>v>vv<<>^v<>>v<v^<>><>>^<v<>^<^^<^v>v^<vvv^<v<v^>vv>>^^^>v><^<vv<>>><v>>>^v>><v^>vv<v>vvv<vv>>>^<v<^vv^<^<<v^^vv<^>^<<<v<v<^><v<<^^v^v<>>>^v^<<<vvvvv<<^><^v<>v>^v>>>><v>v^><^v^^<<><v^>^<v<>v><v^^^^<^v>^><>^^<^>^<<^<<^v>^v^^v><>v^^^<^^<>vv<v<<><>v^<vv>^vv><vvvvv<^v<vvvv^vv^v^>>vv>^<v>^^v<^v><^v^^v^^v>vvvv^v^^>^^v^^^v>v><>^<v<<^><v>^v^<vvvv>>v^v^v>v^<vv>>^>^>>^>><>^<v<<^v^<>^><^<vv>^^^vv>v>^^vv^>><^v<v<v><v<>>vv>>v<v<>vv<vvv^<><^>v<^^^<>^v<>>v>^>>^^v>vv>vv^><<^v<<^><<v<v^vv<<^v<^<>^>>^<<><^vv<v<<<v^v<<>^>v<<v<^v>>vv^^>v^><><><<vv<^><>v^vv><<v<vvv<>^<^^vv<<<>^^<>^vv>>vvv<<^<v>^^><<^><vvv^>^^>^<^^>v><<<<<vv^><>>vv<^<<^^v<>v<>v<<v>v^^v<>>><<^^>v>vv^^^<^<>^^><^>vvvv>vv^<v^<>^<<^^>^^^>^<^<v^<<v<><v^>v^>^>^>v<^<^><<<>><>>>^^<<>^v>^^>>v^v<^^<v>v^v<v>^vv^^^<>^v^^v<>v<>vv<^^<<>vv^>>^^^vv<^^^<><>^<<><>^v
<v<^v<<^vv^>^vv>^vvv<^<<>^>>^^>^v<^<>v^^<<^v<v><>>^<^<<v<^v<^^<<v<<^^^^><><v<^^^v>><<^<<>>><>^v>vv>>v^<>v^<^v>v^>>^v<v<v<>^<<^>>><><^<^v<<^>v^^^<><<>>><<^vv>>v^<vv<<>^^<<v>>v><>^<<>^^><<><>v>v^<^v^<^>vvv<>v>>>>>>^vvv>v^<^v<>v>v^><^vv<vv<v>>v<^>v>^>^<v^^^<<>^><v>^>><^<vvv>>v^v^>^<vv^<v^>>v<>>>v^>v<v<^^>^><^>><v^><^v^^<>vv>>^^^>v^<><^<><^^<v^v^<<<^<vv>v>^^>v<^<<v^>^>v<<<>^>><^v<vv>v^v^^^^<vv^><>v^>v>><<v<<>v<>v^>v><v^^^v^<v<^<>^v<v<v>v^v<^^v<v^>v<v^v^>><^>><v><>>^<><v^<<<v<><<^^><><<v><vvv<v><>>^>>>vv<^^^>^<<<<^^^v<vv^<>vv>>^^^^vv>v<^>><<v^^^v>vv^v><^v><v^<<<v<>^v>vv^^>v<v^<<>^>><<^v^^>^>>^^><<^<<>^>>v>v<^<v^^^v<^^>>^^^<>^>><<v><<v>vv<>>>^vv<<><v^>>>vvv^>vv><v<<>^^>^v<^^>v>v^<^>^<v<v<>>><vv<vv^<<>^v<v<^^<vv>vv^>v<<>^<>v<^>v^<vv<><<>^v<>>^^<^><vv>^^^<^v<<^>^^<<<vvv><^v<^^^v>>v>><v<><>><v>^<>>vvv<v>v^^<v<>>><>v>^>>><v<v<<>v^>>^>^v>^><^v>^<v>v<vv^><>v<v>^v>>^v><v<<^>v>^^<<^v<^<vv<>^<><vv^v<<v>>^v<<^>>^<^>^><v^><^>>v<v^<^v<^^v>^<v<^vvv<v^>vvv><^v<v<v<v^^>^<^>^^>v<^^^<^^>^v>><v^<<><>>v^^v^v^v
<<<>>>^>><><>^^>>^<<vv>vvvv<><^<^v^v<>>>><^<>v><^vv<^v>>v<<<^^>^<<><>^^><<^><<<<^^v^^>v<<vv>^>>^^^v>^<v><<^><<vv^<><^>^><vv>v^<<v<>v^>^<><<>>>v^>^>v<v><><<v<<>>^vv>>><<^^>vvv^<vv<v<<>><<^^v>>><v<<<^<^v>v^>v>>vv^^^v>>v^><<<>v><^<^v<<<^^<^v<<^^v<>^^<>^>^<v^^^^^^>v<<v>^vv<>v<>vv>v<>v<^^v><^<vv<^<>>^<v<>v^<>v><>v<^v>>v>^^><v<vvv^^<v>>v^><vv<<<>>^<v>v^vv>><^<<v>^^^>>>v><>>vv>^^<vv<vv><v^v>^v<>vvvv<>^v<>>^<><vv^><>>>^^^^>>vv^v^<>><^^><^^>><<<v<>^vvv^>vv><>v>v^<^v^<vv<><<<v<vv<v>^>v^>><<^>^>^vv>^<v>v^>v<<>>><<vv^<<v>v>^<<<<<<>>vv^^^<<v<<<^<<<v^v<^<v>>>vv>v<>>>^<>^>^v<>vv>>v<<^>v>^vv>vvv^<>><<vv<^^><<^>vvv><v^v><><<v^^vv>^<>>v^>^^>v>>>v>vv^><>>><<<<<>^>vv^<<^^<^>^<>^>v<v<<>v^v>>>^v^v>^v>^<<v>^vvv>>vv<>v><v><v^<>v^v^>v<><vv><^^vv^v<vvv>^<<^^>^>v^^>^^<>^>>>>v^<^>><>^v>v>v>><^vv^v^<^<v<<<v><v>vv<<<>>>>^v<<v^^<^^><>^^<^^v^v<>><><>><>v>>v^v^><^<^v^>>><vvv<>>><v><v^^v^><vvv>>^^>>>^><<<>v>^^v<v<<v<<><^<>^^vv^<^><v><^>^<>v><vv^^^v<<^<>^^>^^v<^v<vv<<<><v><v><v<<^^v<v>>^>^^<>^vvvvv^^^>><<^<><v>^>^<v>>>v
<^<^^<v^v>^>vv^v><>^>^>^^<vv<^><^v^><^v^><^><<<^^v>v>^>^><vv>^^^v^>^v^<v<<<<<>>v>>>vv><<<v>v<<><<v<v^>>^v<<v<<^vv<<^<^>><^^v>vvv>>v>><^vv>^<<<^>v<^<><^v>^<<v^<<v^>>v>>v<<^^v^^><^>v^v>^<<<<v^v^<>>v^>v^^v^<v^^<^>v<v>>v^v>>^^<>><vv^<>v<><^^>^^^^vvv>vvv>^><><^><<<>^v^<>v^>^^>>^vv>^<>>>>v<vv^vvv>><^^<<>^>^^>><<^<^>^^v<vv>^^>^v>v^>^^<<v>>>^<vv^vv^>v><>v><<vv^>>^vvv<<^v^<vvvv>^<^<^<^<vv<>>^<vv>v^>v^><<^^><^v<vv<>>^<v^<>^>v^<<<v^>>>>><<<vvv>v<^vvv>v><^^^<v^v^>v>^<>v^<>>^vvv<v^<v<^>^<v<v<>v<<>^<<>^^^^v<v<^v<v<<>^>^vv^>v>v>vv^>vvv>v^vv><^>vv^><^^v<^>v<>^>^<v<>^vv^^<<<<>^^^v^^^<>v<>^<>><v>>v>^>v^>^>^<v>^<^<>^<<<v<<^><^<v^>><>>v^^v>v<^^><><v<^<<^v>>^v^>^<<<vvvv>^><^><vv^v>^^^>v><>v>^>^v>^v^<^v>>v^v^><^^<^^<v^v^<v^>^^>v>><<v><vv^^><<^^><>v>><<<^<<>>v><>v^<<<vv>^<<<>vv<<v<>v<vv^v^>^>v^^>^vv^^><v<^><<>v^<v^>^v<v>v>>^vv<v<>v>>v^v^^^>>^vv^^><<<^<^v>v^v<<>^vvv<v<v^^vv<>v^><v><<^>^<^><>>>>>v<v<<<^vv<^^v^v>vv<^<>>>^>>>v^>^v^^^>^>^<>^^<v>>>><<><<vvv>vv><v^^<^v>>v<<>vv^^<<><vv<^>^v>v^v^vv^vv<><v<<<^<vvvvv>>
v^v<><v>v><><v>v^^^<^v>>^v>v^><v^v^><<>>>><><^>v<^^^>v>v><^^v<v^<><<<^v<><^<<^^>>^>^>><^>><<^^v^^>><>>v<v<vv<><<>>vv>vv^vvv<<>>vv<^^>><<vv<><v^<v^<>>^>^^v>^>>v<<<<>>>v<^^v>>v>^><>^<v<v><>v>>^>vv<^^v<<>v>>^<^^>><^<v>>v<>v>^^>v^v<^<^^<v>v^<^<v^^>^<<^^>>v^v^^v<vv<<v<^v<>^v^<^^<>^^>>^<^v><>v<v><^^^<vv<<^^v^<<^v^^v>^v^<<^vv>v>^v^v<^v<vv>v<^><>><^v><v<vv^<>v>>^^^>v>v^v^>v>><>><<<vv<v^<^v^>>>v<v>><v>v^>^<>>>>><v^<^v>^<^<^^>>><v^><v^^^<>v^^>v^vv<>^<<v>^>>^<^>^^>^^>>^<v>v>><<>^>^>^v>><^^<^><v^v<<^>>vv>v>>vv<v<>^><><<<><><<^<>>>v>^^v<<>v^>v><<vvv><>>v<<^<>><<>^><>^v<<^vv<^<^<>>vv<^v^>v><v><^v^v>^<><>^>>>v^><>>^<<^v<v^vv^><<v^>v^^><>v>><v^<<v><^>>vv^>^><^v>v^><>><>>>v>^^>^<v<vvv>vvv<><v<vv>>>>^^^><<>^<^^<^vv<>v>^>>>vv^>>>v>vv<<>^vvv^<><><>v<^<>>^<><><>v^vv>^v>vv^vv^^<^<^>>v<^<v<^<vv>^<>><v<^><<><<^v>>vv^>v<<vv>^<>^v>^>v<<<<>>^>>^^^^v<<^^><v^v^^vv<v<^^v^v^v<v^^>>^>v^>^^><^<^<^v>^^v>><>>^>>v>v^^^<^^>>>^<v<<<>^^v^v>>>>^^v^><>><v<^vv<><><v^>>v<<>>>>vv^>^^><><v<^>vvv>^>>v<<<>><^<^^^^^<^>^^^v<><^^^v<vv
<<^<^>>^^<<>v^^<<^<v^<v>^>^<vv>^<v<v<>><>^<><^<v<<^<v^<<<vv^vv<>>^^^<v<^v^>^vv<>^^<><^^>>v^v<><^>v^><^^^>v^>vv<vvvv<<^^>^v^>^>^^^v^<<v<vvv^^v>^^v>^^>^><><vv^^<v^<>v<vv^^^>>^^<<v>><<<v><<><^<<vv<^<^<v>^<^<v><<><v<<<>^^^^><^^v^<>v>v^<^v>^^vv><><vvvvv<>><v>^vv^^^v><<<<^<<<^<v^>^>>^v<<>vvvv>^>^v<<v^>>^>v^>v^^^<v^v<vv<<><v^^<^^^v<v<v<<v^vv<<<^^<>^vvvvv^<vvv><^<^^^^<<^>v<^vv><<<v^>vv<v^<<^^^v<v>^v>>v^>><><<v<<v^<^>><^<vv^v^<v>^v<<>v^<<>vv<>>>^<v>v^^<^>^v<>^>v^v>^<>vv^vvvv>v^<<>v<v>>><^^<<^^^<vvv>^v<^>^vvv^<>^v>><v<>v^<>^v^^^v<v^<<>vvv^^<v><vvv^^^^>>v^^<^>^><>^v^<v>v<^<v<<<><vv<v>v><^>>>^v<v<^<^^v^>^<v><^^>v><^v<<<<v^v<v^vv^>v>>^^<<v^<>^v>^>v<v^v><^v^v<v^^>vv<>^>>^v<^<><><>^>v^v<><>^v<^>^<v^<vv^^>>><v<>v<><<<^^>vv<><<^vvv<>^^^^>vv<<><>^^>v>^^^<vv>vvvv<<^^<v^<^>^>>><^>v<v^^><^^vv><v><<v<^<>v^^v<<vv^<>v<<<^<^><^v^^<^v><><<vv><v<v^<<>v>><<><>^><><<>>>^v^vv<vv^v><<^^<^^>^^^<v<<<^v<v^<<<<>v<vv^vv^>>>><>vv^>^<^<v<^v>>><^><<>v^v<>^v^>>v^v^^v^>vvv^<<v<^v<><>v^><v<v>>>^v<<>v<<>v>v>>^>><v>v^><vv<vv^<<v
><^>v><v<<<><^>v<^<^v><v^<v^>^<vv^^<^^<vv>vv<v><<v><^^^v<^v^<<<<v^<<^^vv^<^^^v<v^<><>>v><v<^><>><^>^><^v^^<^<<>><>>^v><>vvv^^v<vvv<>v^^>^v<<<><v^>^>>v>^<vv<<vv^^>v>^^<^>^>v><v^v>^<>>><^^v<>^^<>^v^v><>v<>v^>v<^>vv^v^>^<vv^<v^v>v<<v><^^<^^<<^^<^<<>>^<v^<>>>v^^<^^v><>><>>>><<^><>>^<v^v>><^<>v>>>^>><>>^^<v^^>^v<>>v^^v>vv^v>^<^^^<>^<v^^^<vvvvv<<<>vv<v<>v>v<^<^^<v<^^^<>^>>v>^<><v<<><<^>^^v<>v^<^vv<<<v>><><^>>^>v><>v>v>^v>^<v>>^^^<<<^>^^>>><^><^v^v<^>^^^v>v<>v<<<^<^<><>><>^^>>^<><v>^<^v<vvv^<><v>^<v>v>v<<>^v>v^><>><^v>vv>v^<><^^<v<v<vv<><^^v>^^^><<>v<^<<><^^><<>>v>^><v>^v<<^<vv<<^<vv^^^<vv>>v^v<^><>^<v^vv><><<^><^^><v^^v<^><>^v>><<^v^>v^^v^^><<vv^<>^<>v^>^^>>v>v^^vv>>><^>>^^<v><<^>^>>><>vvv^<^vv><^>^^<><<>v^^v<^vvv>^>>vv^^<>v^^>^^<vv<<v^>>^<<v<v<^v<<^<^>>^^v<>v^<v<<<v><^vv<^^><^v>^<<<vv>v<v>>vvv<><><vv>^v^v^v<^v><^<v^>><<vv><<vvv^vvv^<<v>^v>^^><^^vv^^<<>^v<>^^v<^<v^^v>v<>^>^<^^>>>v><>^<v<<v><>^^>><vv<^^^^^v^^v^^v^<^>vv><v<<<^^^<>v>^vv<>^<^v^>^^<>>^<><^<>><>^v<^>vvv^<^<<<<^v><vv<v<><^>><<<v^v>
<>vv>>><>>^>^<<><^>><>v^^<^>>v><v<v^>>><v>^<^<>^vvv<>^^v<v<^<<v>v^v^<><^v>>v^>v^v^v>><<v<>>v<>>^<><>v^<^^>v^>^v^>v><^>^^v>^v<>v^<>><><v>v>><<><v<v^^v^><<^>^<vv>v^<^v>v>^<<<v<^v<v^v^v^<<v^vv^^<<v^v>v<vv^>^^vvv^^^^v>^<^<vv>>>^^<^>^><v^>^^vv^^^vvv>v^v^v<^<^vvv<><<>>>>^<v^v<^v<>vv^<^<<^v>><^v<><^>^v^>^^>^>vvvv^^^>><^^<<^v>v<>^^^>v^v>^<vv<<<<>^>^>^>^^<<^vvv^<<<^><><^>><^>>^><^<v>^^<<<<>v>v><><<vv<^>^>v<v<>v>v>^^vv^>v>v>^>^>v>^^v<><vv^^v^^v>^^^<>^><^^v>v>^^>>^<<>vv>^vvv>^v^>v<vv^<<<v<<v^<v><v^v^^>v>^><vv<v^<v><<^<^<v^<>^^<v>^>>^^><>vv^><>v>>v>^^v<<v^<>>^v>>v^>v^>^>vv<>>>^<<v<><<<<^vv>v>><^<>^>vv>v<>^<><<><<v>^^vv^<<v<vv<^^>><<<>>^>>v>>>>>^<vvv^<<>vv<^<vv^^<^^v^<>^<>^^>^^>>v>v><<^<>^v<<<<v>^<^v^v>^^v>v<^>>>vv<>>v^^^^><>vv<v>><<v<<<>v^v^>vv<<v<^>v>vv<>^>^v>^<>>>>^^<><^^<<v<v^>^^>^vv^<v<v<>^vvv>v<^v^^v<>v<^>>vv^^^^^^>>vv<><vv>>v><><v>vvv>>^>^^vv^v^^^>^>^v^^^v<v>>^v<>^v^^^>^v^<v^><^vv<v^v<>vv><>vvv>><^v>v<v>^vv><v<<>v<v<^v<v>vv>^<<>v>><>^<v<><<>^<>>^^><<vvv^>v^^v><<<>v<<^v^^>^<vvvvv><^>v^^<<^>>v
v<>>^^<<>v>^vv<><>vvv><>>^v><v^>vv>>>>^<v<<v<v<vv<>><^<^v>vv<><<<<v^<^>v<^v<>v<^^>>^v><><^^<<^^<<><<vv^<>^^vv>v^<v<<v><^vv>>v>^<>>v>v^>><>v>v^>v^^>>^v<<v^<>><>^^<<v^>vv^<v^^v<v><^^^v^<^>^>v<<vvv<v^<^^v>>^><v^<<vv<><^<v^<><>^><^>>^v^vv^<<vv>v<>>^>^^^v^<>v^>v^^^>v<><><<^><v^<<<v^><>^<<><^v^<<v>^<>>^<^v<<v<>v^><v<v<^v^vvv<^^><<^<><vvv<^^v^>^v>^^<>>><v<<>^^<<<v><v<>^v>^^<v^><v<<<><<v<<vv>v><>>><^>v><<<^^v>>vvvv<<v>>^^^^^<^<^v^<v^v<<vv>>v^^>vv>^^v<vv>><>><^<>><v^>>^>^<vv^>v^>vvvvv<^^><>^^>^^v>>>vv>^<<v^v>>v^v^<v^<<^v<>^^^^<^v><<^vvv>^<v><v^><>><v<<>^^v>>>>><><>>>vv^<vvv><vv>v^<>^^v^>>v>>^^<<>v^<>v>^v>><v>^>v<<><<>^><vv^>v>>v>vv^v>vv<<v^>v<>^<v>>><v>^^^>vv>^>vv^><^v^v<vvv<<v>^<^vvv^<>v>^^^<^v^>^>>>v^<><>><vvv^<<<vvv>v^<<>v>^v<><v^vv<>^<><><^>^^^^v^v><<v<<vv^v<v<<<<v^v<v>^^^><vv^^<<<<>v><<<^^>>^^^^>^vv><<v>>>v^>^vv<vvv^<<<^><v^<>^^<>^<<<vv>v>^^>^vv<^<<^<<^<><<v^>^v<v>>>>v>><^<v><<<^>^<v<^>v<vvv>v^vv<v<^^>><v^v<v<vv^v^^><<^><v<>^<^v^><v^>v^v>>^vv^<<^v^<>v<^<^^v^<>^<>^><^>^^^^v<^v^^v><<vv^<<<<v
>>>>v<>>v^>^>>^<<v^<<<^<>v<^^<v>^^>^^<^<<v^<<^><>>>v<v>><^^>^<<<^<>^<v<^>>^>v><<^v<<<v^vvv<><><><<<>^<><^v<><v^<>^v<vvv^^<v<v^>v>>v<v^v>vvv<^v^^^^^v>v<^^^vvv<v>^>>>^vv^>><>^>^<>^^v<^v<v^v^><^^^^><^v^><<<>><<<<>^<^>v<<v<<<vv^^<<^>>v>^>><<<<^><^v<>^>^<>^>^<>^<<vv^>^<>vv>^v>>><^<^^v^>>^v>vv>v^^>^<<<<v><vv<<<^v<<vv<<^^<<>^vv><>v^><<v<v><^^><^><<<^^v<<vv><<><>v<<v>^>vv>^<^>^>><<<^><>vv^<>v>v^>^v<<^><<<v<^^^>^v<^^^>><<^v^^<v^^<^>v<v<<vvv<>^<^v<<^<<><>^<><>^^vv<>v<vv>^vv^<^v>v<<v><>^><^>v<<<<^>^>v<vv^>^^<^<>>^v>v>>v<>v>>^>>^<<^^<>><<vv>v^>v>vvv>^^<vv>vv<vv>><>>v>^>v<><^><<^v^>^><>vv<^<>^v>>vv<><^v>>^>v>v^>^^v<>>^^>^^^v<v><>vv^vv^^<<><>^>>v<vv>><^>>v>^<^<>^><v>^<>^v<>v<<<<v>^vvv^<^>v^vv<><<><v<>v<<v>><>v<>v>v<vv>^vv><^<^^v<><<><^^v<<>v<>v<>^><v^v>>v<><vvv^>><<vvv<>^<><^v>^v^v^><>v>vv<>>^^>vvv^vv<<^v<>^v^vv<v>v>>>><v><v^v>^^vv<<>v<^<vv<^>^<vv>^<^<v<>>v^^><^^>>>^v><<v><vv<<>^vv>vv^^^^v><^^v>>v<>vvv>^v>v^<v^>vv><><v<<vv^v>^^v<v>vv^^v^^<^^^vv<^^>>>vv<><<><><><v<<><>>v>^>>^<<>><v^>^<^^^>^><^vv><^<^
vv<>><<>vv^>v^^v>><^>^v^>v<<^<^>vv>^^v^><><v<^<><<^v>><>vv>v^<<><vv<<^vv<v^<^vv<^^<^>v^v^<><^>v><>^<<>^<v^><v>^^<^>>>>>>v><^^><v^^><<^v^v>v>>><^^v>>v>><<<><<v<vvv<^^<<>^^<vvv<^^^^^^<<><v<^>v>>>^>^^^<<<<<<v^<v>v>>v<^<v<^^vv<^^<<^<<><v<<<<v<<v^^^^^^v<^v<^^^>^^>^v>>vvv>v<>>v>v<^<v^<>>v<<><<<>^^<v^v>>^<v>>><v>^<vvv<v<v><>^v^^<>>>>v<vv<<>v>>>><^v<^^<v>>^v^<<vvv>vvvv>^v><v>><<v<<>^<^^^v>v<v><^<^<>v<vv<^>>^>><<>>>vvv^<>^v^<>^<<^<v^^<v<<<vv>vvv>v^<<><>^>v>v<v<<<>>v>>><v^>^v^v^v>>>^v^<v>^>^^><>vv<^v><><>v>^<^v>^>>^<<^>^^><<^v<^v^<>^v<^^>vv<<vvvv>v>v^<>^<<v><^<vv>>^<<>v^<v^<<v^^^v<^<<^<>>vv<<^><^>v<>>>>>>><v<^^>>><vv<v<>v^>><^><^>v^>^><<vv>>>^><vv<<v>><v<<<><>v>^><vv^>>^^v<<v>vv^><^v^><>^v^^v>^^<>>^vvv<<v<>v><>vv>^^>>v>^>v<^^<vv<>>v<v<vv^^<>>v>v<>^v<^vv>^vv^vvv<^v><>><vv><<^<v<>>>>>>vv<>^v<<<^<<vv><^<<<^^<v^<>^^<v^<v>>^<^<<>>>^^v<^>^v>^<^vvv>>v<^<vv<^>^^^>><>^<>v^><>>^^v^<v<v>^>><v^^>^>v<v>v<><><v>><<v^<vv>vv<^>^v^^v<v^>v^><<>^v>^^<^v^><v<><<><<v>v^>^vvv>v<><<>^^<>^<><>^<>v^><v^><><><>>^<vv^><v>
^v^><<>vvv^v>><>vvvv<<vv^v^v>><>v<<^v>^v^<^^><><>^>>^^v^v>v<^<>vvv^v^>v^v^><>^<><<><v^<^>^>vv>v>><>v<><><v^>^>><<^<^<<<^<>^><v^^v^<^<v>^<>^>^^>^^>^><<><>^<v>^>><v><<^<><v^v><v<>>v^>v^^>vv^v^>v^><vvv<^<v><^><>>v>>>v<>^>v^v^^^v<<v>><v>>^^v<vv^^^^v><<<^v>^>>>^v^>vv>^^>vv<^^^v<<<><<v^>>>v^<v>>v>vv><><<v><>^<v<<v<>v^vv^><>>><vvv><<>><^<<<>v><v^>^<v<<vvv><^<>^><vvv<<<vv^^<v<<>v<<<^>>^^v><vv>v><^<><<^^^<>^^^>v^v>v><^<<^v<>v^>^>>^^^<^<>v<^^v<^>^^^>^<^v>v>^^<v<^^v<<^vv>v<v^<v<>>v^v^<^>>>><<^<>vv<v<<v^>>>^v><^^>>v>^v<v>^>v^>>^^vv>v^v<<^^^^v<^^><>^vv>>^<^<>v<^^^<^v<^<><<^v>v^<>^v<>^<>v>><vv<^<^^v>>><>^^^v<^>>>^v<v>>v<>>><vv>^<^><v<v^>^<^<><<^v>><<<^>^vv^^v>^vv<>v<<<^<>vvv<<<<^<>>vv>v^<<v^^><<>vv<vv>^^^^<v^<^>><<^^v<vv<v>>v^v^vv<><vv^^>^^<v^v>vv^^v><<<>>^^<^<v^^>v><^>v<><v><^>v><<^>>>>>^>v^^v><^v>^>v^>^>^^>^^v<^>^^>^<<^v^^vvv><<>vv^>^^vv>^vv^v>><>><vv><<><>>vvv^^vv<<><v<^^^<<^vvv>^vv>^v<>^^^vv><^v>v^<v<v>vvvv>>^^^<v<<^>^<>^<^><<>v^v^v^<v^><vvvvvv^<>><<<>vv<<v^^v>v<v<^^<<^^><^^<<<<v><<^<>>v<>><vv<<
<>v^^<>>>>v^^>vv>v>v^^^^^vv<v^^v<<>><>^v<>^v>vv^><>v>><><^<^>>^^v^<<^><^>>>>>>>v><vv^^v^>^<>>^vv><vv>v^v>^^<>>><v^<<^<>vvv^><><^<<<^<>^>>>>v^^^>^^^<<>^<v<>v<><^v^^v<><>>^v^>^><<^v^^>v>>>v^>^>><^<^v><^<^^<^>v^^<^v^<^^^><>><^^<<>><^v^v>vvv>vv^<<^vv><<><>vv<>v>^>vv<>v<^^<<vv<^<>v^vvvv><v>^<>^v<^vv<v^v<^^>v^^<<vvv<^v>v><^>>^>^^<>vv<><^<^<^vvv<v^>^<>^<>v>vvv>v<<v><<<<>vv^v<>>^^v>^^v>v<>v>^v>>><<><<^v^^>^^v^^v^v<v>^<v>><v<^>^<>>v^^><v<>v>>^>^<><v><><v^<<^v^v^^^^<v^<vv>>vv<<<><^vv^<^^v>v^^>v<>><><><<>><^<<<^>v<^^^>^^v>vv<^>><><v>>^v><^<>v^>>^^<>^vv>>^^^^v<>><^<><>v>^v<<>^<v<^v^v^>vv>>>>>^>>>vvv<<<<^<<^<>><vv<v<<vv<v>>^<v<<<<^><<>v>v>v>^<<^^^<>^vv<>^v>vv>>>vv^^v<<>vvv^>^<<v>^v>>vvv>><>vvv>>^^v<^^v>^v>vv>>><vvv><vv>>v<<^v^<<<>^^>vv^><^v<>vv<<^<v^^v>^<<v<^>>><^^<v<^v^v^^^<<><^v<>^<<<v>^v><<<^v<vv<v^<v^^vv^<><<<>>^<><>^^v<>v^><><^^>vv^v>v>^v>^<>>vvv^>^vv^><><^^v<<^vv>^^><v>^<v^<v<<vv>^><^<v<<^vvv<><>^>^<^vv<^>vv>vv>^><<<>v<<^vv<>vv<^>>v<>vv^<v>^v<v<>>^<^^v^vv<><>>v>><vv>><v^<><>v^>v^><^^v<>v<^v^>
v>><^v>>vvv^<>^v<^<^v^v>>^^vv<<v<v>>v<^><<<v>^<<<<<^v<vv^v<v>v<v^>>><^>^^^vvvv><<vvv^><v>><>><v<>>^v<vv^><v><^^<>^>v<^<>^vvv^v^^<<^vv<<v^vv<>^vvv^<v<>><vv>v><>^><v<>^<vv<v>vvv^^>v<v<><vv>>v^^><<>^>^^>^>^^v<<v<>>>>^>>>v><v^<<<<^^>v<^^^>^^vv<><vvv><^<<>>>^<<vv^<<vv^v^<^^vv>v<^^<>^><<>^<>^>>><>v<>vv>^><>^<^>>^^>vv^v>>v>^^v><><^^v^^^^v>>>><>>vv^^v<^v>v^>^<v<<>v><vv>>v<<>^<<<>^<v>vvvv>v^<v<<<^^vvv>^>v<<>^^<<>v<v^v<>vv<^><vv<>^<v^><v><v^^^v>^vv<v>^^v<^^>v<><vvv<><<<>^vv>>v>^<v><^vv^>v^>>v>v^^<<v<>>v<>v^><<<^v<v><v><^v^><>^^>v^<v^<>v<^>^<<^^><><v<vv>v<>v<<^v><<><><^^^<v^^<v^<^vv^<v>v><<^<vvv><>^<<^^v^^><>><><>><^<><vv<>>^<v>v><^>^vv<<^vv>>><>v^>^vv>^vvv<^^>v>^v^^^^<v^<v><^^^v<v><<>^^><<<<v<>v><<>^>^vv^<^>^<<<<<vv<<^<vv<<<v>^<<>^>^v>^>>vvv^>vv^<^v<>>v^^<v<^v^^v^v^v<<>><v>^>><vv^^<^>>><><^>^v^^<^>><<<>^^>v<><^<>^^v^>^v<v>v<<<^<><v<<>v<<<v^<<<<^^>^><vvvv<^^>>^v^^v^<^>><<><><v<>^^v^vvv<<<v<v^^>^>^v>>>><<vv^v<v^>>><v>v><>vv^<><>><^v>^>^v>v<^<>>^vv<vv>vv^^^<<^v^<><>v^vvv^>^>^^>^>^^><<^^vvv<<vv>^<><
^vv><>^<v^v>vv^v>>vv<<<v^v<><>^v<<v>^>><><^>vvv<^v>>>vv><<^^<v<^<><^vv^^^^><>><v<>>>>vvv^>>vvv<^<<>><>v>^vvvv>v^vv>v^<>v^^>>v<>v<<^vv^^<v>^>^^<^v<<^v^vvv>^<<v>v<<^<><><v^>v>^<^<<^>>>^^^<v^^<v>>>>v>>v^<^^><>><^^<^v^>^>>v^<v>^><<^<^<<^v<vv<<>>^v>^^<^^>vvv>v<>v<>v<<>^<^<<><<>v>^^>v<^vv^<^<>>vvv>><<vv>>vv>vvv^^^^>>>^^>^^>^><<vv><>>^<^^^<v<^^^>vvvv^>^>><^^>><vv>v^<>v^<v><vv^v>^<^>^>^^v>^v<<vv<><v<<v^^^^<><v<>^>>^><^<^>vvv>><^><^<<v^<>^v^^^<>^^<^v>>>v<v>v<<<^>>>^>^^^^^<<v>^v>vv^^>><vv>v<^^v^><^^<^><v^vvvvvv<^v<>^v^v>>v^^^>v<vv>>>>>>>>^>><<<<><<<v<<><^v>^><^^<<vv^>v<v^v<<<^>^vv>><>v<><>^v>v<^<<<<<^>vv^>vv^v>^v<^v^^>v>^>>v>>v^v^v>>v<v^<<^><<>vvvv<><><v^>>^<v><<vvv<><><v>>^v<<v^<>^^v>><^v>v<<><>^v^^v<^<<>>>^^>^<>^v>^v^><>v>v<^>>vv^<><<vv>^v<^vv<^^v<>^^vvv^v<<<v^v<^<^^<v>^vv>v^>^>v><>v>>^>>^v>>v^v<^^^v>>v^<>>v>><>vv<v>v<^<>v^>^><><v>v<>>>>><vvv<<<>><vvvv^^<v<>>^^>v^v^>^^<v^>><v>v^^><v>v>^^>^^v<^<^<<^<^vv^>v<v^<^^v><v<^><^^^v<vv>^v<^^<>><v^^v<v^<<^>^>^<<>^<^><>v<vv^v^^>^v<^^^>^<><<>^^<>>>v<<v^>>>
>v^^^>v<>^v<v>>^^^<v<>><>vv^<v>^<><<vvv>>>^<>^vv^<<<^>v^^<>><v>vvv>>vv^vv<^^><^^<<^v^^><<^^><v>v^>><<>^vv>^<><<^^<<vvvv<^vv^^<^v><v^^v<v^^v><<<^^<><<<^<^v><>>>v><<><v<^<><^vv<v<<<>v>>^<v^>>^^<<>^<>v^>><>>^^^vv^v<>^>^v<^<^>v^<v>><<<v<^^v<^^^<>><v^>>><^><^<v><^v^>><v^>>>^><<>>^<^^>v<<>v^^v^<<<>^<>><>^vv^^<^^>v<><<^>><^v<>><>v^v><>^<^>^<<v>>v^^<v<v^<<<><<<^<<^^v<>v<^<v<v>^>>>v<v<^>^<<<>><^^^>>vvvvv^><<<^^v>^>>^^><<>>><<v>>v^<><><v>>v>>>v>>>vvv>vv<^<>^><><v<v<><v^<<^<^^v<^<^v><>><>v>v>v^<>><v><<vv^v^^^<<>vvv^^v^v^v^<<^<>^v^^<vv^v<>^>^>^>>v><<^<>^^<^<>v^>v<>><>v>^<v^^><>>^<<v^<><>^><<<<<<^^^>><^^>^^v<<<v>^<<<>v^^^v^^^^vv><>><v<^^>>>v^<^<<>^^>v^^<v>>v^^v<<^><<^vv<>v>>vv^<v>><v^v^<<vvv^<><<^<^^><><v>^<^^<v<vv<^^^^>^<>v^^vv<^<vv^<>^^<v^^<^>^><^>^v>v^<>>^^>><vvv<>v<v^^>v<vv><v>^><vv<^>>>^>^<>v^^v>^>>><>vv>v^vv<<^<<v<^<<v>><><><v<<^^^vv>>>v^v^<>^>><>>>vv>><^vvv<v^><>v>>v<<>^vvv>>^vvv^v>>>>^v><^^^>^^><^v^v^<v<^<v<^^>vv><v<^v>v<^^vvvv>><vvv^<^v^<v<><><vv>>v>^<><v<<^vvvv>>>v^>>v<<>^^<<><^^^<><v^v^v
<><>vv>v>vv<<>>v>><^<<^>^>><>^>v<^^^^^<^>>>>v>^><^^>v<<<^^v>>><>>^v<v><>v^^>^^vv^v<>^v<^^>v<^<<>^><>v<<>^^<v>v<><^<vv<v^v<vv<<^v<v<<<><>>^^>v<<>>v^>><>><>^vv<<v^vv><><<<v<v><v<<^>>^<>vv^<v^<<><<>>^>>v>>>v><>^>v><v<v>><>^<<^<^^<vvv>v<<^>^v>>>>^>>^>>v<^<vvv><>><vvv<>^^^^^>v>>>>>><<<<v<<<>><>><>>vv<><>v<><<^^<vvv>^<^<^^^>><vv^>>^v<>v^^v^^^<vvv><<<<<v<v<>^<>>vv^><^<^^^^<>v<<vv<>vv>><<^vv>>>>^vv^>><v>v^><v>v<^>v>v^v>><^<>v>>v<>vv^<<vv>>>^vv^>v^<>^^v^<>v<v^<<>><v^>^^v<^>>>>>v>>><>^><^v<>>v>>v<><><<>^v^<<^^v>>vv>v>^<>^vv>^^>^v^<>>vv^^^<>^<^^<<<^vv><<v<^v>v>>>^v>><>^^>>v<^><<>^<^^>^><v<v^>>v>><v<v<>^<vv<<<<vv>v>vv>>><>^^v>^^>v<vv<>v<v^>^vv^>^<>><><vv^<^^v><v^^<<v^^v^>><>>v<>v^<<^v<>>^v<<vvvv>v^>^>v><<<v>^>^>v><v^><<^>>>^^>v>>>^<<><v<^>^>>^v>v><v>^>^>vv>^>>^^>v><>vvv<>v^^<^^^>^<><^>>>vv<<><v>v<>v<<^>^^>v^^<v<<<>vv<>>vv^>v>><vv>>vvv^>vv<<<^>^^v>^^<v<>v>>^v>>^v>^v>>^>^<^v<^>><vv^<>>>^<v^<vv><vv<<>>v^><v^<<v<>^>^vv^<v<^>>><<<^^>>vv><v><><><^>v>vvv^><<<<<>v^^<^v<^>^>^^^^v<<^^^v^v<<^><^^<^>^v>><>>v^
>><v<^^^<>>^>^v<>>>^v>>><><vv>><^^^^^>><v>v><^^^<<v><vvv>vv<><^v<<^>v<^<><v<>v^<v^<^><^v>^><<<^v><><^<<>vvvv>^v^>><><<>v>^^>^vvv^^^<<v^>^^^<<v^^>^v^^vv<>vv^v<><v<>^v<><v^>^^<^><^>v<><^v<<><^vv<<<<^^^>>>^^^^<v^^^v^>^v<^v>v>v^><^>v<<>>^><><>^<^v>><<v<<<^^>>v><<v^^><vvvvvv<v^<>><>^>>>v^>v<vvv^<^^>^>^v<v>v>>^>v<^v>^>^<v^^<>^><<<<<>vv<^v<^v<^<^><>v^<<<<v>v>><^<v^v<v^>^><v>><<<>v^><<^>v^<>^<v<<v<<<>^<<>vv<>^^v>>v>^^v^><><vv^<v<>>^>><^^>>>>^<^>>>><vvv>^vv<>vv^<v><^<>^>^^>^<<^><<>>>^>>v^>v>^^^>^vv><>><vvv>v>>v>^<v^v>^><<<v^>^>vv<>v^^^>^^v>>vv<>>^v>v>^^<<vv><v<^>vvv^><<v><<v^>>^^^^>vv^<<><<>vvv<<v^^v^v<<v>^>>^v^<^>v>^<>>>v>v^^v<<v><>><<><^vvvv<<>^v>><^><v^vv>>>>^>><v<>>><<^^>v^^><>v>vv^>>>>>><vvv<^>>vv<>^<<v>^<<>v>>v^v^>^^>^>vv^v^>^><v>>v<^>^v^>^<^<v<<^vv<^><vv<^<<>v<<vv^>^v^>>v^v^<<<>^<^>>^<<v>>^>vv>v^^>v>>>>><^^<><>v<^^<v<v<v<v>>^<^<<>^vv<vv^>^v^>v^<<v<^v>^>vv>^<v^^^^<^<v^^<v<^<v^>v<^><>><vvvvv^><v<>v>>^>>v>>v>^<vv>v><>>^>>^<<vv^^><^v<<>^<v^^v>^^v>v><<v>^v<v^<>^>v^^>v>>^<^^>vv>v<>^v<vvvvv<^^v
<>>^vvv^<^^v^v<<v<v><><>^^>v<<v<<<v<<^<^^>vv^^<^>v><v^^^v>vv<>>>vv^^<><<v<>^v^>vvv><>v^vvv>>^<>>vv^v>><vv<^^<><>>v>v^<><v><^<><^v>v>v><^>^^^v^<^<v<><><vvvv<<>v><^^<><^v^<^>v>v>vv<vv<<><^<^><<v^v^v<v<><<^^vvv>><<vv^<>^<v^>v^^>^>v>vvv<<><^>^^^>v<^vvv>v<^^>v^^^>>>><vvv^<<<<^<v>><><^<v<>v>v^^^^<v><v<>v<v<^^v<<^><^v<v<v^vv>^>v^^v^^>>><^vvv>>>^^^>>v<^<v<>^v<vv<^^<<v<v><<v^^v<^<>>^v^>^<><v<<v<>vv^^^v<v<<<v<><>>v>v><<<>>^>v<v^^v>vvvv><><>><^^v>vvv^v>^v>^^^^<v<^^>v<>>vv>><vv^v<^>^<^v>^v>vv<><^>><^<^^^^<^>^>vv<v<vvvvvvv<^<><^<<<vv<^<>^vv>^^<^><>>v^<vv<<<><><v^^>>^^^v<<<^>^v^<vv>v>^v^<vv^^v<v>>v^<<^>^><><<^^^<^^>>^^>vv<v^v^vvv>>v<v^v<<>v<vv><v^v<<>>vv^^^>^^v^>^<><>^v^<><vv<^v>>v^v^^>^vv>vv^^><v>vvv<v><<>v<v^vv^v^><v<^v<v<^>^<>v<v^v>v<v^<v<^^<>^>>v<<>><>>>v^<><<<<<^<v<<>><><v><<<<^<^^<^>>^^><<^v><^>^vv><>v<v>v<><v^<>v<vvv^^<<<>^^v><>>v<v><<^v<>><v^v>><<<v><v<vv^^^vv>>^^<<><<^>v^<v^^^>v><v<>>>^vv<^^>^<>^v<v>>v^<>^v<>^^<<>v<>^^><v^<^^^<<^>>v<><v^<>>v<v^v<>v>^>>^v<^^v<<^><^v>^>v<v<<v^^v>^<>^^v<v>v><<
^<<v><>><<^vv^^<<<>v<^<><^><<^><^<<<^<>^^<>><v^v^vvv^v<^<>>^v<<^>>v<>v>v<^v^v^v>^<^v<^^>>v^<v>^<>^<<<>><<^^><>>v>^v^>><^v>^<<vv^v<<v^<<>^^>^<<><<^v>>^v^v>^<<^<v>v^v>>v^>^>v>^v^v<v<^^>>v><^>^^>^^^v<vv>^>^^v<^^>^><>><<>v^vvv><<><^<vv^<>v><v^<^<>>v<<>>v>>^><v>v>^^^<^^><^>>>^v^^^<>><>>>v^vvv^v<vv^^vv^<v^<<<^^>^v>v<v^v<>><^>>v<<^>^>>v^<<^>>><vv><^<><^>>^>>^vv^<>v<^^>v>>><<>><<^<^v>^>^>^v^>>><^><<><^<<><<<>v^^^^vv<>vv<<^>>^<vv<v<^v>^><v>>><^vvv>^<v><>^v^^<vvvv>>v^^v<>^^>^<>><><v<^^vv<^<<<><^^<^^^^<vv<v><^^<>><>>^<vvv>><^^>^^><^<><v^<><>>^<v<^^<vvv<>^^<<^<^^^>><^^>v<v><>^^^^>^^^><v>><v^>v>^^>^v<><<^<>vv<>^^><^vv<v<>><>>>^<<<v>>><>v>^<>^<>^<v^<<v^^v<<<<v^<<>>^>v>>v>>>>^<v^vv<<v>^><^^^^^><<^>^^<<<<v>v<^vvv<<v><v>><vv>>vv<^^<^^vvv^^^^v<<<^<^>v^vv<<^>vv>^<v><>^>vv^>v>v<>^<<>^^v>^^v>>>^<v><v<vvv<vv<<vvv^^<<<<^^v>vv>>^><v^^>>>><>>^v^^<><v^>^v^^v<><^>^>><^<<^>>>vv<v<^>v>vv^><v<>v>>^^>^>vv>vv<<^><^vv^>v<<>^^<<><>^v>vv^v^><<^<<<v^>^^<>>v>^^<><^<^<>^<v>>v><>>><>>v><v>>v>^v<<>v^<>^vvv<vv><><<<^<<^<>v^><""".replace(
    "\n", ""
)

result = simulate_warehouse(data, moves)
print("part 1 result:", result)


#### Part 2
dirs = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1),
}


def resize_grid(grid):
    _mappings = {
        "#": "##",
        "O": "[]",
        ".": "..",
        "@": "@.",
    }
    # new_grid = []
    # for line in grid:
    #     new_line = list("".join(_mappings[c] for c in line))
    #     new_grid.append(new_line)
    new_grid = [list("".join(_mappings[c] for c in line)) for line in grid]
    return new_grid


def get_robot_pos(grid):
    rows, cols = len(grid), len(grid[0])
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == "@":
                return (i, j)


def update_grid(grid, visited, move):
    cells = []
    match move:
        case "^":
            cells = sorted(visited, key=lambda x: x[0])
        case "v":
            cells = sorted(visited, key=lambda x: x[0], reverse=True)
        case "<":
            cells = sorted(visited, key=lambda x: x[1])
        case ">":
            cells = sorted(visited, key=lambda x: x[1], reverse=True)
    dy, dx = dirs[move]
    for cell in cells:
        y, x = cell
        ny, nx = y + dy, x + dx
        grid[ny][nx] = grid[y][x]
        grid[y][x] = "."
    return grid


def get_adjs_and_edges(grid, pos, move, part=1):
    y, x = pos
    dy, dx = dirs[move]

    adjs = set()
    if part == 1 or move in "<>":
        while True:
            ny, nx = y + dy, x + dx
            if grid[ny][nx] in ".#":
                return [(ny - dy, nx - dx)], adjs
            y = ny
            x = nx
            adjs.add((y, x))
    else:
        edges = []
        queue = [(y, x)]
        while queue:
            y, x = queue.pop(0)
            if (y, x) in adjs:
                continue
            adjs.add((y, x))
            ny, nx = y + dy, x + dx
            if grid[ny][nx] in ".#":
                edges.append((y, x))
            elif grid[ny][nx] == "[":
                queue.append((ny, nx))
                queue.append((ny, nx + 1))
            elif grid[ny][nx] == "]":
                queue.append((ny, nx))
                queue.append((ny, nx - 1))

        return edges, adjs - {(pos[0], pos[1])}


def moving(grid, pos, moves, part):
    for move in moves:
        """
        # zip looks nice but way too slow
        ny, nx = (a + b for a, b in zip(pos, self.dirs[move]))
        """
        ny = pos[0] + dirs[move][0]
        nx = pos[1] + dirs[move][1]

        if grid[ny][nx] == ".":
            pos = (ny, nx)
        elif grid[ny][nx] == "#":
            continue
        else:
            edges, adjs = get_adjs_and_edges(grid, pos, move, part)
            blocked = 0
            dy, dx = dirs[move]
            for cell in edges:
                ny, nx = (cell[0] + dy, cell[1] + dx)
                if grid[ny][nx] == "#":
                    blocked += 1
            if blocked == 0:
                grid = update_grid(grid, adjs, move)
                pos = (pos[0] + dy, pos[1] + dx)
    return grid


def get_coords_sum(grid, part=1):
    target = "[" if part == 2 else "O"
    rows, cols = len(grid), len(grid[0])
    # _sum = 0
    # for r in range(rows):
    #     for c in range(cols):
    #         if grid[r][c] == target:
    #             _sum += 100 * r + c
    _sum = sum(
        100 * r + c for r in range(rows) for c in range(cols) if grid[r][c] == target
    )
    return _sum


part = 2
moves = list(moves)
grid = [list(row) for row in data]

grid = resize_grid(grid)

pos = get_robot_pos(grid)
grid[pos[0]][pos[1]] = "."

grid = moving(grid, pos, moves, part)
result = get_coords_sum(grid, part)
print("part 2 result:", result)
