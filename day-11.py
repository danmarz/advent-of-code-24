data_string = "475449 2599064 213 0 2 65 5755 51149"
# data_string = "125 17"

stones = [int(stone) for stone in data_string.split()]
blinks = 25
# print(stones)


#### Part 1
def blink(stones, num):
    for _ in range(num):
        res = []
        for stone in stones:
            if stone == 0:
                res.append(1)
            elif len(str(stone)) % 2 == 0:
                stone_string = str(stone)
                res.append(int(stone_string[: len(stone_string) // 2]))
                res.append(int(stone_string[len(stone_string) // 2 :]))
            else:
                res.append(stone * 2024)
        stones = res
    return len(stones)


res = blink(stones, blinks)
print(f"number of stones after {blinks} blinks: {res}")


#### Part 2
from collections import defaultdict

blinks = 75


def optimized_blink(stones, num):
    # Initialize the count dictionary
    stone_counts = defaultdict(int)
    for stone in stones:
        stone_counts[stone] += 1

    for _ in range(num):
        new_counts = defaultdict(int)
        for stone, count in stone_counts.items():
            if stone == 0:
                new_counts[1] += count
            elif len(str(stone)) % 2 == 0:
                stone_string = str(stone)
                left = int(stone_string[: len(stone_string) // 2])
                right = int(stone_string[len(stone_string) // 2 :])
                new_counts[left] += count
                new_counts[right] += count
            else:
                new_stone = stone * 2024
                new_counts[new_stone] += count
        stone_counts = new_counts

    # Total number of stones is the sum of all counts
    return sum(stone_counts.values())


res = optimized_blink(stones, blinks)
print(f"number of stones after {blinks} blinks: {res}")
