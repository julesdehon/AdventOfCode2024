from pathlib import Path

Vector = tuple[int, int]


MOVE = {"^": (0, -1), ">": (1, 0), "v": (0, 1), "<": (-1, 0)}


def process_move(move: str, board: list[list[str]], pos: Vector) -> Vector:
    (x, y) = pos
    (dx, dy) = MOVE[move]

    to_process = [pos]
    to_push = list()
    while len(to_process) > 0:
        next_x, next_y = to_process.pop()
        c = board[next_y][next_x]

        if c == "#":
            return pos

        if c == ".":
            continue

        to_push.append((next_x, next_y))
        to_process.append((next_x + dx, next_y + dy))

        if dx == 0:
            if c == "[" and (next_x + 1, next_y) not in to_push:
                to_process.append((next_x + 1, next_y))
            if c == "]" and (next_x - 1, next_y) not in to_push:
                to_process.append((next_x - 1, next_y))

    board_copy = [[c for c in row] for row in board]
    for x1, y1 in to_push:
        board[y1][x1] = "."
    for x1, y1 in to_push:
        board[y1 + dy][x1 + dx] = board_copy[y1][x1]

    board[y][x] = "."

    return x + dx, y + dy


def find_robot(board: list[list[str]]) -> Vector:
    height = len(board)
    width = len(board[0])
    for x in range(width):
        for y in range(height):
            if board[y][x] == "@":
                return x, y

    raise ValueError("Could not find robot")


def board_str(board: list[list[str]]) -> str:
    return "\n".join("".join(line) for line in board)


def sum_of_gps_coords(board: list[list[str]]) -> int:
    result = 0
    height = len(board)
    width = len(board[0])
    for x in range(width):
        for y in range(height):
            if board[y][x] == "O" or board[y][x] == "[":
                result += 100 * y + x

    return result


def widen_board(board: list[list[str]]) -> list[list[str]]:
    height = len(board)
    width = len(board[0])
    widened_board = []
    for y in range(height):
        row = []
        for x in range(width):
            if board[y][x] == "#":
                row += ["#", "#"]
            elif board[y][x] == "O":
                row += ["[", "]"]
            elif board[y][x] == ".":
                row += [".", "."]
            elif board[y][x] == "@":
                row += ["@", "."]
            else:
                raise ValueError

        widened_board.append(row)

    return widened_board


def main() -> None:
    raw_board, raw_moves = (
        Path("input/input.txt").read_text("utf-8").strip().split("\n\n")
    )
    board = [list(s) for s in raw_board.split("\n")]
    moves: list[str] = [c for c in [line for line in raw_moves.split("\n")]]

    position = find_robot(board)
    for move in moves:
        position = process_move(move, board, position)

    print(sum_of_gps_coords(board))

    widened_board = widen_board([list(s) for s in raw_board.split("\n")])
    position = find_robot(widened_board)
    for move in moves:
        position = process_move(move, widened_board, position)

    print(sum_of_gps_coords(widened_board))


if __name__ == "__main__":
    main()
