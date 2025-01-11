import heapq
import time
import sys

def ucs(weights, maze, start, rocks, switches):
    initial_rocks_positions = set(rocks)

    start_time = time.time()
    priority_queue = [(0, start, tuple(rocks), "", 0)]  # (tổng trọng lượng, vị trí hiện tại, vị trí đá, hành động, bước đi)
    visited = set([(start, tuple(rocks))])
    nodes_generated = 0

    while priority_queue:
        total_weight, current_pos, current_rocks, path, steps = heapq.heappop(priority_queue)

        if all(rock in switches for rock in current_rocks):
            end_time = time.time()
            return path, {
                'steps': steps,
                'weight': total_weight,
                'nodes': nodes_generated,
                'time': (end_time - start_time) * 1000,
                'memory': (sys.getsizeof(visited) + sys.getsizeof(priority_queue)) / (1024 * 1024)
            }

        possible_moves = get_possible_moves(weights, maze, current_pos, current_rocks, initial_rocks_positions, switches)

        for new_pos, new_rocks, action, rock_weight in possible_moves:
            new_state = (new_pos, tuple(new_rocks))

            if new_state not in visited:
                new_total_weight = total_weight + rock_weight
                new_path = path + action
                new_steps = steps + 1

                heapq.heappush(priority_queue, (new_total_weight, new_pos, tuple(new_rocks), new_path, new_steps))
                visited.add(new_state)
                nodes_generated += 1

    end_time = time.time()
    return None, {
        'steps': 0,
        'weight': 0,
        'nodes': nodes_generated,
        'time': (end_time - start_time) * 1000,
        'memory': (sys.getsizeof(visited) + sys.getsizeof(priority_queue)) / (1024 * 1024)
    }

def get_possible_moves(weights, maze, position, rocks, initial_rocks_positions, switches):
    moves = []
    x, y = position

    directions = [
        ((0, 1), 'r', 'R'),
        ((1, 0), 'd', 'D'),
        ((0, -1), 'l', 'L'),
        ((-1, 0), 'u', 'U')
    ]

    for (dx, dy), move_action, push_action in directions:
        new_x, new_y = x + dx, y + dy

        if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]):
            # Kiểm tra nếu ô tiếp theo là ô trống, công tắc
            if (maze[new_x][new_y] in (' ', '.', '+', '*') or (new_x, new_y) in initial_rocks_positions or (new_x, new_y) in switches) and (new_x, new_y) not in rocks:
                moves.append(((new_x, new_y), rocks, move_action, 1))

            # Nếu ô tiếp theo có đá, kiểm tra điều kiện đẩy đá
            elif (new_x, new_y) in rocks:
                push_x, push_y = new_x + dx, new_y + dy
                rock_index = rocks.index((new_x, new_y))
                rock_weight = weights[rock_index]

                # Kiểm tra giới hạn của vị trí sau viên đá
                if 0 <= push_x < len(maze) and 0 <= push_y < len(maze[0]):
                    # Ô sau viên đá phải là trống hoặc là công tắc và không có đá khác
                    if maze[push_x][push_y] in (' ', '.', '+', '*') and (push_x, push_y) not in rocks:
                        new_rocks = list(rocks)
                        new_rocks[rock_index] = (push_x, push_y)
                        moves.append(((new_x, new_y), tuple(new_rocks), push_action, rock_weight))

    return moves