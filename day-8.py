data = """......................D....B...h..................
..............................h...................
.............D...3.....X..................9.......
...........C........X....2.hB......v........b.....
....................................O.............
......u.....3.........p...........................
....u......................v....6.................
......................y..D.....Ov.2..............b
.....u..........X...........o........y............
.........................y...B.f...........s......
.7....................C.2.....Bsyp..........t...q.
.u.7...........X............................Oe..t.
...........V........3......6v.s........o....h....t
..E........L.................6..........o......9..
........E......m.2.P.......O...9...8....b.........
..m..........3.......p..........M8................
..1.....................K.p....................b.e
5...............L...........s.6..........S.M......
....5..1.......E.........k.f.........M............
.E..Y..V......l.......T...D.......9....Q..........
..............................M...................
.....5....P................m...x..q......F......e.
................f...c......................x..F...
..V.C...........7.......a....o....8.........F.....
.......4....L.a..g..P.....8......Q....7d..........
...1......4..a............k......t...d............
..........V..........L....m........K....Q........S
..................1....k.....T....................
..........l......a...............F................
...........P...4.......l......x...................
.............c....g........T......................
.....g............c...Q.......................S...
...............l..................A.d.T.U.........
..........................f...0.............d.....
..........G..................A............e.S...x.
.........Y.......q........g....K..................
.....................q.H4...0.................j...
....................HA..............J.............
..Y..........................0...J.......j........
.......................G.JA...................U...
.......5..........................................
...........c..............G.........K.............
...............................G..................
...........................0.j....................
............................H.......k..........U..
.........................H........................
...................................Y....J.........
..................................j...............
..................................................
.................................................."""

# data = """............
# ........0...
# .....0......
# .......0....
# ....0.......
# ......A.....
# ............
# ............
# ........A...
# .........A..
# ............
# ............"""


def parse_map(map_input):
    """Parse the map input into a list of antenna positions."""
    antennas = []
    for y, line in enumerate(map_input):
        for x, char in enumerate(line):
            if char.isalnum():  # Check if the position is an antenna
                antennas.append((x, y, char))
    return antennas


def find_antinode_positions(antennas, map_width, map_height):
    """Find all unique antinode positions."""
    antinode_positions = set()

    # Group antennas by frequency
    freq_map = {}
    for x, y, freq in antennas:
        if freq not in freq_map:
            freq_map[freq] = []
        freq_map[freq].append((x, y))

    # Iterate through antennas of the same frequency
    for freq, positions in freq_map.items():
        n = len(positions)
        for i in range(n):
            for j in range(i + 1, n):
                ax, ay = positions[i]
                bx, by = positions[j]

                # Calculate the midpoint candidate
                if (ax + bx) % 2 == 0 and (ay + by) % 2 == 0:
                    mx, my = (ax + bx) // 2, (ay + by) // 2
                    if is_valid_antinode((ax, ay), (bx, by), (mx, my)):
                        antinode_positions.add((mx, my))

                # Calculate double-distance candidates
                dx, dy = bx - ax, by - ay
                antinode1 = (ax - dx, ay - dy)
                antinode2 = (bx + dx, by + dy)

                # Validate double-distance candidates
                if 0 <= antinode1[0] < map_width and 0 <= antinode1[1] < map_height:
                    if is_valid_antinode((ax, ay), (bx, by), antinode1):
                        antinode_positions.add(antinode1)
                if 0 <= antinode2[0] < map_width and 0 <= antinode2[1] < map_height:
                    if is_valid_antinode((ax, ay), (bx, by), antinode2):
                        antinode_positions.add(antinode2)

    # Final cross-validation to ensure strict alignment with rules
    validated_positions = set()
    for antinode in antinode_positions:
        if is_valid_with_any_pair(antennas, antinode):
            validated_positions.add(antinode)

    return validated_positions


def is_valid_antinode(a, b, antinode):
    """Check if the antinode satisfies the problem's conditions."""
    ax, ay = a
    bx, by = b
    cx, cy = antinode

    # Calculate Manhattan distances
    dist_ac = abs(ax - cx) + abs(ay - cy)
    dist_bc = abs(bx - cx) + abs(by - cy)

    # Check if one distance is exactly twice the other
    return (
        (dist_ac == 2 * dist_bc or dist_bc == 2 * dist_ac)
        and dist_ac != 0
        and dist_bc != 0
    )


def is_valid_with_any_pair(antennas, antinode):
    """Check if the antinode is valid with any unique pair of antennas."""
    for i in range(len(antennas)):
        for j in range(i + 1, len(antennas)):
            if is_valid_antinode(antennas[i][:2], antennas[j][:2], antinode):
                return True
    return False


data = data.splitlines()
# Parse input
antennas = parse_map(data)
map_width = len(data[0])
map_height = len(data)

# Find antinode positions
antinode_positions = find_antinode_positions(antennas, map_width, map_height)

# Display the unique antinodes and their count
print("unique antinodes:", len(antinode_positions))

# Optional: Display the map with antinodes
visual_map = [list(row) for row in data]
for x, y in antinode_positions:
    if visual_map[y][x] == ".":  # Do not overwrite antennas
        visual_map[y][x] = "#"

# # Print the updated map
# print("\nUpdated Map:")
# for row in visual_map:
#     print("".join(row))


#### Part 2
from math import gcd

data = """......................D....B...h..................
..............................h...................
.............D...3.....X..................9.......
...........C........X....2.hB......v........b.....
....................................O.............
......u.....3.........p...........................
....u......................v....6.................
......................y..D.....Ov.2..............b
.....u..........X...........o........y............
.........................y...B.f...........s......
.7....................C.2.....Bsyp..........t...q.
.u.7...........X............................Oe..t.
...........V........3......6v.s........o....h....t
..E........L.................6..........o......9..
........E......m.2.P.......O...9...8....b.........
..m..........3.......p..........M8................
..1.....................K.p....................b.e
5...............L...........s.6..........S.M......
....5..1.......E.........k.f.........M............
.E..Y..V......l.......T...D.......9....Q..........
..............................M...................
.....5....P................m...x..q......F......e.
................f...c......................x..F...
..V.C...........7.......a....o....8.........F.....
.......4....L.a..g..P.....8......Q....7d..........
...1......4..a............k......t...d............
..........V..........L....m........K....Q........S
..................1....k.....T....................
..........l......a...............F................
...........P...4.......l......x...................
.............c....g........T......................
.....g............c...Q.......................S...
...............l..................A.d.T.U.........
..........................f...0.............d.....
..........G..................A............e.S...x.
.........Y.......q........g....K..................
.....................q.H4...0.................j...
....................HA..............J.............
..Y..........................0...J.......j........
.......................G.JA...................U...
.......5..........................................
...........c..............G.........K.............
...............................G..................
...........................0.j....................
............................H.......k..........U..
.........................H........................
...................................Y....J.........
..................................j...............
..................................................
.................................................."""


def parse_map(map_input):
    """Parse the map input into a list of antenna positions."""
    antennas = []
    for y, line in enumerate(map_input):
        for x, char in enumerate(line):
            if char.isalnum():
                antennas.append((x, y, char))
    return antennas


def find_antinode_positions(antennas, map_width, map_height):
    """Find all antinode positions based on the new rule:
    Any grid position that lies on the infinite line formed by at least two antennas of the same frequency is an antinode.
    """
    freq_map = {}
    for x, y, freq in antennas:
        freq_map.setdefault(freq, []).append((x, y))

    antinode_positions = set()

    # For each frequency group
    for freq, positions in freq_map.items():
        # If multiple antennas share the same frequency, include each of them as an antinode
        if len(positions) > 1:
            for ax, ay in positions:
                antinode_positions.add((ax, ay))

            # For every pair of antennas with the same frequency, find all points along the line
            n = len(positions)
            for i in range(n):
                for j in range(i + 1, n):
                    ax, ay = positions[i]
                    bx, by = positions[j]

                    dx = bx - ax
                    dy = by - ay
                    g = gcd(dx, dy)
                    step_x = dx // g
                    step_y = dy // g

                    # Move in the forward direction
                    cx, cy = ax, ay
                    while 0 <= cx < map_width and 0 <= cy < map_height:
                        antinode_positions.add((cx, cy))
                        cx += step_x
                        cy += step_y

                    # Move in the backward direction
                    cx, cy = ax - step_x, ay - step_y
                    while 0 <= cx < map_width and 0 <= cy < map_height:
                        antinode_positions.add((cx, cy))
                        cx -= step_x
                        cy -= step_y

    return antinode_positions


data = data.splitlines()
# Parse input
antennas = parse_map(data)
map_width = len(data[0])
map_height = len(data)

# Find antinode positions
antinode_positions = find_antinode_positions(antennas, map_width, map_height)

# Display the unique antinodes and their count
print("unique updated antinodes:", len(antinode_positions))

# Optional: Display the map with antinodes
visual_map = [list(row) for row in data]
for x, y in antinode_positions:
    if visual_map[y][x] == ".":  # Do not overwrite antennas
        visual_map[y][x] = "#"

# # Print the updated map
# print("\nUpdated Map:")
# for row in visual_map:
#     print("".join(row))
