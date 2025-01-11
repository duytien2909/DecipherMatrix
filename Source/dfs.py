import time
import sys

def dfs(weights, maze, start, rocks, switches):
    start_time = time.time()
    stack = [(start, tuple(rocks), "", 0, 0)]  # (vị trí Ares, vị trí đá, đường đi, tổng trọng lượng, số bước)
    visited = set([(start, tuple(rocks))])  # Trạng thái đã thăm
    nodes_generated = 0

    while stack:
        current_pos, current_rocks, path, total_weight, steps = stack.pop()
        possible_moves = get_possible_moves(weights, maze, current_pos, current_rocks)

        for new_pos, new_rocks, action, rock_weight in possible_moves:
            new_state = (new_pos, tuple(new_rocks))

            if new_state not in visited:
                new_total_weight = total_weight + rock_weight
                new_steps = steps + 1
                new_path = path + action
                
                stack.append((new_pos, new_rocks, new_path, new_total_weight, new_steps))
                visited.add(new_state)
                nodes_generated += 1

                # Kiểm tra nếu tất cả các đá đã ở vị trí đích (switches)
                if all(rock in switches for rock in new_rocks):
                    end_time = time.time()
                    return new_path, {
                        'steps': new_steps,
                        'weight': new_total_weight,
                        'nodes': nodes_generated,
                        'time': (end_time - start_time) * 1000,
                        'memory': (sys.getsizeof(visited) + sys.getsizeof(stack)) / (1024 * 1024)
                    }

    # Nếu không tìm thấy lời giải
    end_time = time.time()
    return None, {
        'steps': 0,
        'weight': 0,
        'nodes': nodes_generated,
        'time': (end_time - start_time) * 1000,
        'memory': (sys.getsizeof(visited) + sys.getsizeof(stack)) / (1024 * 1024)
    }

def get_possible_moves(weights, maze, position, rocks):
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
            # Nếu ô tiếp theo là ô trống, công tắc
            if maze[new_x][new_y] in (' ', '.', '+', '*') and (new_x, new_y) not in rocks:
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