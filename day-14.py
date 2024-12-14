# Dimensions of the space
WIDTH = 101  # 11
HEIGHT = 103  # 7

# Number of seconds to simulate
T = 100

# Example input (replace these lines with your actual input)
data = """p=63,14 v=-55,-32
p=98,35 v=6,-38
p=51,46 v=4,46
p=22,3 v=5,-47
p=19,31 v=50,-1
p=44,64 v=-19,-85
p=6,9 v=34,-54
p=99,20 v=23,-12
p=32,56 v=84,-96
p=80,78 v=-10,47
p=18,88 v=91,64
p=4,34 v=39,-49
p=43,64 v=-18,-28
p=73,74 v=26,-88
p=37,19 v=39,-40
p=38,27 v=49,-95
p=96,34 v=35,94
p=21,90 v=-51,-42
p=67,16 v=-74,-61
p=50,82 v=84,68
p=42,45 v=83,98
p=95,62 v=71,81
p=37,58 v=-62,7
p=63,90 v=47,75
p=33,82 v=-43,31
p=24,66 v=-29,-66
p=98,49 v=57,1
p=22,20 v=-22,-75
p=93,48 v=5,-60
p=16,3 v=63,86
p=91,81 v=-38,-86
p=5,83 v=-22,83
p=89,27 v=99,42
p=54,5 v=-89,11
p=79,60 v=35,52
p=42,50 v=-44,28
p=50,34 v=-36,65
p=65,92 v=9,-85
p=5,53 v=-70,-84
p=6,68 v=-68,8
p=78,98 v=81,69
p=6,37 v=-95,-68
p=7,11 v=-87,16
p=0,65 v=61,-43
p=37,38 v=-99,28
p=79,74 v=20,42
p=20,22 v=-6,26
p=48,96 v=58,45
p=88,93 v=-57,3
p=72,86 v=-73,-85
p=74,32 v=27,68
p=89,66 v=71,-67
p=7,102 v=-50,55
p=42,16 v=-90,85
p=62,99 v=46,-70
p=15,32 v=96,57
p=96,61 v=52,-15
p=56,55 v=92,44
p=45,46 v=-81,-71
p=11,73 v=6,-51
p=53,61 v=2,9
p=64,100 v=97,73
p=35,49 v=-53,14
p=86,35 v=80,-46
p=38,27 v=-91,87
p=89,97 v=8,53
p=58,58 v=-1,16
p=53,55 v=10,22
p=84,82 v=-39,61
p=62,50 v=-55,74
p=72,31 v=-81,92
p=71,60 v=-65,66
p=47,81 v=97,-30
p=88,3 v=-68,23
p=38,37 v=40,-81
p=37,81 v=39,98
p=25,23 v=68,-69
p=22,10 v=-79,-68
p=47,0 v=-33,-62
p=24,25 v=31,-83
p=22,57 v=95,-6
p=81,5 v=-36,33
p=72,89 v=72,39
p=26,12 v=23,27
p=5,7 v=-44,-19
p=55,90 v=-36,92
p=90,66 v=53,1
p=19,99 v=24,16
p=15,87 v=87,-56
p=33,30 v=-9,-22
p=68,71 v=65,-52
p=97,6 v=-41,69
p=0,42 v=88,38
p=24,23 v=95,-32
p=38,26 v=-71,41
p=59,9 v=26,96
p=21,81 v=95,-6
p=49,16 v=21,62
p=71,51 v=-29,-80
p=42,57 v=-20,10
p=61,88 v=25,7
p=65,50 v=-20,-73
p=17,15 v=6,-31
p=54,94 v=65,-26
p=30,6 v=58,19
p=40,64 v=49,-99
p=53,54 v=27,-37
p=59,67 v=-37,89
p=53,90 v=-9,-82
p=8,20 v=-87,-17
p=21,65 v=86,-14
p=78,27 v=13,-87
p=83,67 v=99,75
p=66,14 v=59,-92
p=85,85 v=16,69
p=90,102 v=-76,-63
p=30,82 v=94,49
p=18,13 v=88,-2
p=51,77 v=-83,2
p=6,3 v=13,-71
p=50,52 v=-72,-16
p=52,16 v=-63,-54
p=100,23 v=-14,-98
p=22,55 v=-21,-15
p=50,53 v=83,-30
p=99,23 v=-42,38
p=26,56 v=95,-96
p=80,101 v=-84,74
p=48,81 v=-69,-14
p=67,66 v=91,-73
p=98,67 v=43,67
p=12,33 v=51,-97
p=29,68 v=-16,52
p=92,16 v=6,-84
p=26,53 v=-88,66
p=29,49 v=43,73
p=55,77 v=37,53
p=43,37 v=83,-16
p=37,74 v=85,45
p=22,30 v=-42,72
p=64,35 v=-49,36
p=83,49 v=-57,-67
p=66,50 v=83,28
p=26,87 v=86,2
p=70,63 v=35,51
p=40,99 v=86,-55
p=92,83 v=43,53
p=26,49 v=4,-45
p=26,16 v=56,-30
p=76,3 v=-75,11
p=9,20 v=13,87
p=60,43 v=8,-44
p=93,39 v=61,-53
p=24,54 v=-77,53
p=63,41 v=18,28
p=94,28 v=-39,86
p=13,31 v=-32,72
p=26,102 v=-44,-47
p=47,74 v=57,45
p=23,85 v=39,-4
p=70,10 v=-65,-55
p=10,53 v=18,97
p=34,26 v=-52,-17
p=62,71 v=45,8
p=63,10 v=58,-62
p=89,60 v=-97,-26
p=58,67 v=74,60
p=1,101 v=-39,-19
p=47,24 v=66,27
p=95,52 v=-49,-89
p=59,28 v=83,-2
p=54,42 v=47,-96
p=6,75 v=49,-51
p=63,4 v=-8,-93
p=11,92 v=2,-23
p=36,37 v=20,15
p=10,10 v=-97,-19
p=17,16 v=-42,5
p=73,69 v=-28,-64
p=21,5 v=58,5
p=70,49 v=39,-72
p=6,59 v=-87,89
p=73,75 v=-65,1
p=9,92 v=87,-29
p=31,51 v=85,6
p=24,76 v=-65,21
p=91,75 v=-30,-79
p=75,20 v=72,-16
p=32,70 v=-43,45
p=68,21 v=-91,-3
p=100,19 v=61,37
p=22,0 v=41,18
p=5,3 v=69,-41
p=36,61 v=-62,-59
p=48,73 v=-63,-94
p=43,84 v=11,-79
p=40,14 v=57,34
p=19,51 v=77,95
p=70,33 v=15,61
p=30,46 v=-67,79
p=66,87 v=14,27
p=1,63 v=82,-18
p=9,60 v=10,70
p=81,48 v=24,-50
p=31,68 v=86,67
p=28,54 v=66,-66
p=22,35 v=99,85
p=1,26 v=-37,85
p=13,65 v=15,45
p=92,5 v=-83,49
p=63,21 v=-18,5
p=73,99 v=-33,83
p=33,49 v=-71,-36
p=70,27 v=-37,-83
p=70,12 v=44,-46
p=28,12 v=49,-54
p=73,102 v=19,-76
p=13,38 v=49,35
p=75,88 v=-38,2
p=42,53 v=-90,-14
p=93,84 v=-96,-87
p=37,94 v=49,90
p=17,46 v=-88,-96
p=52,32 v=-66,-29
p=51,34 v=-97,99
p=59,81 v=28,24
p=74,60 v=-93,14
p=18,24 v=59,-68
p=91,15 v=-15,32
p=94,60 v=77,15
p=71,28 v=-10,-90
p=94,88 v=60,-91
p=25,38 v=16,-78
p=84,22 v=-76,-26
p=80,18 v=17,-47
p=5,3 v=86,84
p=87,71 v=-57,-50
p=95,84 v=16,-85
p=14,16 v=41,-76
p=24,65 v=14,-88
p=47,50 v=67,-96
p=18,41 v=-80,51
p=32,37 v=-64,60
p=59,12 v=27,70
p=41,64 v=-82,80
p=26,35 v=61,-28
p=43,87 v=48,61
p=54,2 v=92,-32
p=11,29 v=-96,-8
p=76,29 v=17,-68
p=68,20 v=27,87
p=72,38 v=-92,-31
p=21,88 v=-50,53
p=13,15 v=-85,99
p=28,57 v=72,-29
p=54,49 v=3,2
p=41,21 v=29,-93
p=41,96 v=-16,-57
p=62,27 v=64,-9
p=71,16 v=82,-25
p=36,23 v=-99,13
p=65,63 v=-99,-33
p=96,15 v=-3,49
p=2,5 v=70,-64
p=12,78 v=-56,-91
p=90,3 v=-80,-4
p=19,33 v=49,-2
p=46,8 v=-38,-81
p=95,69 v=-67,-87
p=67,92 v=-7,-65
p=86,101 v=-57,18
p=24,91 v=48,39
p=0,67 v=70,-44
p=65,59 v=48,-57
p=60,99 v=-63,83
p=99,61 v=80,15
p=23,41 v=77,65
p=6,73 v=3,31
p=86,91 v=71,-49
p=67,49 v=56,-97
p=4,14 v=15,-18
p=41,4 v=39,26
p=88,41 v=33,57
p=79,30 v=63,-38
p=14,92 v=3,91
p=47,7 v=75,-27
p=67,55 v=-28,-88
p=94,8 v=19,-94
p=69,76 v=-65,-36
p=70,98 v=82,91
p=7,87 v=-4,68
p=53,89 v=-73,-93
p=94,31 v=70,-61
p=1,68 v=43,74
p=85,10 v=-57,48
p=5,101 v=86,16
p=16,27 v=-87,-83
p=92,9 v=15,70
p=100,13 v=49,-29
p=20,24 v=59,93
p=35,19 v=-52,-84
p=3,96 v=97,77
p=55,15 v=74,41
p=87,88 v=80,16
p=81,33 v=-57,87
p=91,93 v=-17,19
p=23,68 v=-15,45
p=91,56 v=7,-96
p=30,31 v=-34,-90
p=0,59 v=88,-29
p=73,50 v=-76,83
p=63,17 v=-19,-69
p=23,89 v=-42,2
p=77,45 v=91,14
p=13,4 v=89,85
p=8,12 v=43,-77
p=29,12 v=19,45
p=66,36 v=11,-39
p=80,32 v=12,-14
p=25,19 v=28,38
p=52,95 v=65,-12
p=79,82 v=-2,61
p=68,27 v=-19,-16
p=24,74 v=-33,-28
p=24,1 v=-6,-27
p=92,39 v=34,-96
p=91,1 v=-30,92
p=42,83 v=21,-50
p=70,10 v=-57,-19
p=23,20 v=49,-76
p=75,100 v=17,61
p=36,76 v=94,39
p=24,76 v=87,74
p=44,10 v=-17,4
p=55,11 v=28,34
p=68,89 v=-67,52
p=5,10 v=42,-77
p=80,83 v=81,-80
p=68,69 v=10,96
p=57,88 v=-64,71
p=40,68 v=-90,30
p=17,74 v=68,-58
p=57,11 v=84,-24
p=61,30 v=29,57
p=29,88 v=20,54
p=92,6 v=-86,-11
p=17,50 v=4,-74
p=27,4 v=-52,-70
p=11,55 v=14,-81
p=73,83 v=-93,68
p=10,50 v=14,7
p=16,6 v=-60,-3
p=15,101 v=69,69
p=44,15 v=-83,51
p=11,7 v=-23,-25
p=9,19 v=41,71
p=72,56 v=-33,-61
p=22,50 v=-15,14
p=19,8 v=76,-78
p=67,32 v=-11,-46
p=32,13 v=-51,99
p=74,99 v=-30,-42
p=56,37 v=65,13
p=13,94 v=-41,-49
p=32,26 v=76,-54
p=74,44 v=44,57
p=20,72 v=-24,-35
p=20,12 v=-4,40
p=29,50 v=58,-58
p=56,55 v=48,43
p=67,40 v=45,-67
p=43,17 v=29,-10
p=25,33 v=-11,35
p=31,43 v=-79,87
p=56,1 v=81,-52
p=83,90 v=44,54
p=95,38 v=15,21
p=38,52 v=10,-23
p=5,3 v=-13,-85
p=100,95 v=-97,-37
p=92,49 v=17,-59
p=68,49 v=-56,7
p=77,4 v=-47,85
p=26,74 v=40,-50
p=70,7 v=-71,10
p=89,8 v=34,-48
p=4,93 v=33,91
p=11,22 v=24,-52
p=38,34 v=2,-75
p=35,72 v=67,-80
p=80,79 v=82,-95
p=90,64 v=-95,30
p=20,31 v=-42,-9
p=94,24 v=60,-2
p=15,37 v=-88,-97
p=6,94 v=51,98
p=67,99 v=-23,57
p=21,78 v=51,-80
p=57,101 v=74,33
p=33,83 v=30,10
p=44,55 v=-64,-7
p=52,100 v=-26,-34
p=92,7 v=71,48
p=34,101 v=21,4
p=9,56 v=96,88
p=97,6 v=-61,-87
p=77,31 v=90,57
p=3,6 v=88,34
p=35,52 v=-75,1
p=29,28 v=31,-17
p=38,59 v=-16,36
p=7,1 v=-87,85
p=25,36 v=-42,-76
p=81,6 v=53,77
p=66,1 v=56,-22
p=85,19 v=80,78
p=70,15 v=72,63
p=92,9 v=-46,64
p=100,42 v=-48,14
p=9,25 v=-59,-23
p=69,4 v=51,-91
p=77,85 v=-45,5
p=54,80 v=-7,72
p=63,1 v=34,-47
p=69,80 v=99,76
p=6,52 v=-46,-21
p=23,75 v=-7,52
p=89,40 v=43,21
p=85,88 v=-57,1
p=90,52 v=6,-89
p=10,93 v=96,76
p=3,68 v=79,-6
p=9,93 v=-59,54
p=68,78 v=-72,52
p=79,95 v=-92,-33
p=52,46 v=42,85
p=18,51 v=-51,80
p=76,51 v=-49,41
p=87,92 v=-98,12
p=44,19 v=57,-24
p=15,69 v=13,67
p=93,81 v=-58,10
p=5,80 v=33,-87
p=41,40 v=85,-82
p=99,45 v=-2,7
p=84,101 v=21,-79
p=31,63 v=29,75
p=17,54 v=-69,-22
p=25,38 v=77,-82
p=1,16 v=-31,-39
p=84,85 v=-48,53
p=46,80 v=44,-13
p=49,85 v=-55,99
p=66,77 v=54,-21
p=7,92 v=-51,48
p=61,48 v=63,36
p=87,46 v=-85,-8
p=20,80 v=-17,-42
p=70,80 v=52,-88
p=55,100 v=58,41
p=48,10 v=-81,-40
p=29,80 v=-11,-24
p=50,34 v=-71,-23
p=5,24 v=-40,-1
p=39,29 v=-80,-55
p=35,66 v=48,-43
p=26,57 v=-78,-96
p=6,30 v=52,73
p=15,97 v=24,91
p=69,21 v=64,97
p=97,25 v=81,-46
p=13,1 v=15,93
p=17,36 v=17,20
p=50,54 v=64,-43
p=83,94 v=27,-56
p=65,57 v=-83,74
p=98,87 v=80,2
p=52,20 v=-67,-18
p=87,77 v=-22,82
p=87,63 v=98,74
p=21,67 v=-66,-72
p=82,65 v=26,24
p=48,77 v=23,-61
p=89,63 v=54,-13
p=90,3 v=-57,-71
p=12,19 v=36,-1
p=29,29 v=87,6
p=2,94 v=60,3
p=12,4 v=65,-21
p=99,65 v=10,-93
p=39,90 v=-35,-11
p=57,99 v=64,-3
p=23,20 v=-36,-69
p=0,41 v=15,37
p=56,44 v=-10,66
p=94,84 v=81,18
p=51,25 v=75,-76
p=23,70 v=-33,90
p=68,76 v=-29,74
p=92,23 v=43,20"""

robots = data.splitlines()

# robots = [
#     "p=0,4 v=3,-3",
#     "p=6,3 v=-1,-3",
#     "p=10,3 v=-1,2",
#     "p=2,0 v=2,-1",
#     "p=0,0 v=1,3",
#     "p=3,0 v=-2,-2",
#     "p=7,6 v=-1,-3",
#     "p=3,0 v=-1,-2",
#     "p=9,3 v=2,3",
#     "p=7,3 v=-1,2",
#     "p=2,4 v=2,-3",
#     "p=9,5 v=-3,-3",
# ]


# Parse input
positions = []
for line in robots:
    # Format: p=X,Y v=DX,DY
    parts = line.split()
    # Extract position (X, Y)
    px, py = parts[0][2:].split(",")
    px, py = int(px), int(py)
    # Extract velocity (DX, DY)
    vx, vy = parts[1][2:].split(",")
    vx, vy = int(vx), int(vy)
    positions.append((px, py, vx, vy))

# Simulate after T seconds
final_positions = []
for px, py, vx, vy in positions:
    # Calculate new position after T seconds
    new_x = (px + vx * T) % WIDTH
    new_y = (py + vy * T) % HEIGHT
    final_positions.append((new_x, new_y))

# Determine the center lines (these are not inclusive for any quadrant)
center_x = WIDTH // 2
center_y = HEIGHT // 2

# Quadrants:
# Q1: x > center_x and y < center_y
# Q2: x < center_x and y < center_y
# Q3: x < center_x and y > center_y
# Q4: x > center_x and y > center_y

q1 = q2 = q3 = q4 = 0
for x, y in final_positions:
    if x == center_x or y == center_y:
        # On a dividing line, ignore
        continue
    elif x > center_x and y < center_y:
        q1 += 1
    elif x < center_x and y < center_y:
        q2 += 1
    elif x < center_x and y > center_y:
        q3 += 1
    elif x > center_x and y > center_y:
        q4 += 1

# Compute safety factor
safety_factor = q1 * q2 * q3 * q4

print("Safety Factor:", safety_factor)


#### Part 2
WIDTH = 101
HEIGHT = 103

positions = []
velocities = []
for line in robots:
    splitline = line.strip().split(" v=")

    # get the comma separated numbers from the first part of the line
    position = splitline[0].replace("p=", "").split(",")

    # convert to a complex number and add to the list
    positions.append(complex(float(position[0]), float(position[1])))

    velocity = splitline[1].split(",")
    velocities.append(complex(float(velocity[0]), float(velocity[1])))


# make sure we wrap around the position the grid
def wrap(p):
    if p.real < 0:
        p = p + WIDTH
    elif p.real >= WIDTH:
        p = p - WIDTH

    if p.imag < 0:
        p = p + HEIGHT * 1j
    elif p.imag >= HEIGHT:
        p = p - HEIGHT * 1j

    return p


def walk_1(pos, vel):
    pos += vel
    pos = wrap(pos)
    return pos


for i in range(0, 10000):
    finalpositions = []
    for p, v in zip(positions, velocities):
        finalpositions.append(walk_1(p, v))

    dictionary = {}

    for pos in finalpositions:
        if dictionary.get(pos) is None:  # blank space
            dictionary[pos] = 1
        else:  # robot already there
            dictionary[pos] += 1

    # Top
    q1 = 0
    for y in range(HEIGHT // 4):
        for x in range(WIDTH):
            q1 += dictionary.get(x + y * 1j, 0)

    # Bottom
    q2 = 0
    for y in range(3 * HEIGHT // 4):
        for x in range(WIDTH):
            q2 += dictionary.get(x + y * 1j, 0)

    # Left side
    q3 = 0
    for y in range(HEIGHT // 4, 3 * HEIGHT // 4):
        for x in range(WIDTH // 4):
            q3 += dictionary.get(x + y * 1j, 0)

    # Right side
    q4 = 0
    for y in range(HEIGHT // 4, 3 * HEIGHT // 4):
        for x in range(3 * WIDTH // 4, WIDTH):
            q4 += dictionary.get(x + y * 1j, 0)

    # Middle
    mid = 0
    for y in range(HEIGHT // 4, 3 * HEIGHT // 4):
        for x in range(WIDTH // 4, 3 * WIDTH // 4):
            mid += dictionary.get(x + y * 1j, 0)

    centre_mass = mid / (q1 + q2 + q3 + q4)

    if centre_mass > 0.5:
        print("Seconds 'til Christmas tree:", i + 1)
        # print("WEIGHT:", centre_mass)
        for y in range(HEIGHT):
            string = ""
            for x in range(WIDTH):
                string = string + str(dictionary.get(x + y * 1j, "."))
            print(string)
        break

    positions = finalpositions
