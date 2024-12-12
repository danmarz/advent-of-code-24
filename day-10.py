lines = """3456782987078721223458762106567889430671098769654
4349891276129850312369643487656976521589123658723
3232010125034765409874554998540125102479034567014
2101326734535676332123667887030434234328798598323
3210417898743980123011256770121898985215657685412
4398506987652098834500349843210763876004034556702
0347615456901127985678932352107652187123126549811
1256789347810036376547101461458943098014987430910
2187693210211245217832106570367892367123470121321
0096540124300354308943067689256701451234565123438
1454431035445475217652108212101610450965434034589
2563224546766986700543299103454321345876123127676
3470110450897867891056782456969010216789007098787
2989323761210568782344321327878543100218218989896
1056109894323479653451450018967632321307127676125
0347234765012988598560561009878901430456034565034
1218945678967893467621872323451010569210183034789
2301856521050012332132965410067129878345892123654
2545665430541003343045894890128934565456734301203
1238756767632174956556787761238981250349845210312
0019567898948985867843295454345670361238896901498
1123498787656876768930176321054865476766767810567
2345019698343403452343289830238956789857654329801
1276520501232312301450109321107678900348943210762
0989431452301659412567018450234543211234510345643
7871012369498748703698107567892454322365431239652
6982321078543237654899216012301898723670121238701
5983430347670100102765345985432385610184210321981
4676521257881243211255435876987894321095103430870
3676598766999356980346126785456765467656712561561
2189432105438767898987065490308701378345899874432
3008710219127346710897654301219652109234710923653
3219623478033235021588923218789543212121023014567
4988510565454104134676517809654194501033454321098
5675432109567893245785406945403087672122569498545
4789323678652107896690345236712121088011078567632
3291014569743456987501210189874534599187563458901
2104349878898543210012981065963678678296782768940
1001256763278787620125878874052169501345891857434
3210389854109696787434569943141054322321710996523
4389876703010545896563430812232189810430601087012
0478945012321032398654321001145670798510512989802
1567032129834121067743433234030321667623403676501
2432143018765012159812387105321434598787954565410
3654976576544167841003098076101340125697801894321
4567889487637650932342127689234256734676512387212
9654112390128941013234534548940189836785003456101
8741001498037432100105677637654302345494176543212
7632110567126501211012988921013211012343289810101""".splitlines()

grid = [list(map(int, line)) for line in lines]


#### Part 1
def find_trailheads_and_scores(grid):
    # grid is a list of lists of integers (heights)
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Directions for exploring adjacent cells (no diagonals)
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # Identify trailheads (cells with height 0)
    trailheads = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                trailheads.append((r, c))

    def is_valid(nr, nc):
        # Check if coordinates are within the bounds of the grid
        return 0 <= nr < rows and 0 <= nc < cols

    def dfs(start_r, start_c):
        # This function explores all possible hiking trails starting from a given trailhead.
        # It returns a set of all distinct coordinates of height 9 reachable from this start.

        # visited states: to avoid re-exploring the same cell multiple times from the same start
        visited = set()
        # reachable_9s: to record all reachable height-9 cells
        reachable_9s = set()

        # We can use a stack or recursion; here we use a stack for clarity
        stack = [(start_r, start_c)]

        while stack:
            r, c = stack.pop()

            # If we reach height 9, record it
            if grid[r][c] == 9:
                reachable_9s.add((r, c))
                # Even after reaching 9, we don't continue further because there's no 10
                # But we can just continue to pop from stack, no new nodes will be added for height 9
                continue

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if is_valid(nr, nc):
                    # Check if we can ascend by exactly 1
                    if grid[nr][nc] == grid[r][c] + 1:
                        # Use a visited check to prevent re-adding the same cell multiple times
                        # Although strictly ascending means no cycles,
                        # visited can still limit redundant paths.
                        if (nr, nc) not in visited:
                            visited.add((nr, nc))
                            stack.append((nr, nc))

        return reachable_9s

    # Compute the score for each trailhead
    trailhead_scores = []
    for r, c in trailheads:
        reachable_9s = dfs(r, c)
        score = len(reachable_9s)
        trailhead_scores.append(score)

    return trailhead_scores


# Find scores for trailheads in the example grid
scores = find_trailheads_and_scores(grid)
# print("Trailhead scores:", scores)
print("Sum of scores:", sum(scores))


#### Part 2
def find_trailhead_ratings(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # Identify trailheads
    trailheads = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                trailheads.append((r, c))

    def is_valid(nr, nc):
        return 0 <= nr < rows and 0 <= nc < cols

    def count_paths_from(r, c, start_r, start_c, memo):
        # If we are at a 9-cell, that represents a complete trail
        if grid[r][c] == 9:
            return 1

        if (r, c) in memo:
            return memo[(r, c)]

        current_height = grid[r][c]
        total_paths = 0
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if is_valid(nr, nc) and grid[nr][nc] == current_height + 1:
                total_paths += count_paths_from(nr, nc, start_r, start_c, memo)

        memo[(r, c)] = total_paths
        return total_paths

    trailhead_ratings = []
    for start_r, start_c in trailheads:
        memo = {}
        rating = count_paths_from(start_r, start_c, start_r, start_c, memo)
        trailhead_ratings.append(rating)

    return trailhead_ratings


ratings = find_trailhead_ratings(grid)
# print("Trailhead ratings:", ratings)
print("Sum of ratings:", sum(ratings))
