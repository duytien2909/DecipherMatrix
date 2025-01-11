from collections import deque
import time
import sys

def bfs(weights, maze, start, rocks, switches):
    initial_rocks_positions = set(rocks)  # Lưu trữ vị trí ban đầu của đá

    start_time = time.time()
    queue = deque([(start, tuple(rocks), "", 0, 0)])  # (vị trí Ares, vị trí đá, đường đi, tổng trọng lượng, số bước)
    visited = set([(start, tuple(rocks))])  # Trạng thái đã thăm (vị trí Ares, vị trí đá)
    nodes_generated = 0

    while queue:
        current_pos, current_rocks, path, total_weight, steps = queue.popleft()  # Lấy trạng thái hiện tại

        possible_moves = get_possible_moves(weights, maze, current_pos, current_rocks, initial_rocks_positions, switches)

        for new_pos, new_rocks, action, rock_weight in possible_moves:
            new_state = (new_pos, tuple(new_rocks))

            if new_state not in visited:
                new_total_weight = total_weight + rock_weight
                new_path = path + action
                new_steps = steps + 1

                queue.append((new_pos, new_rocks, new_path, new_total_weight, new_steps))  # Thêm trạng thái mới vào ngăn xếp
                visited.add(new_state)  # Đánh dấu trạng thái đã thăm
                nodes_generated += 1

                # Kiểm tra nếu tất cả các đá đã ở vị trí đích (switches)
                if all(rock in switches for rock in new_rocks):
                    end_time = time.time()
                    return new_path, {
                        'steps': new_steps,  # Tổng số bước thực hiện
                        'weight': new_total_weight,  # Tổng chi phí (di chuyển + khối lượng đá đã đẩy)
                        'nodes': nodes_generated,  # Tổng số nút đã tạo ra
                        'time': (end_time - start_time) * 1000,  # Thời gian đã sử dụng
                        'memory': (sys.getsizeof(visited) + sys.getsizeof(queue)) / (1024 * 1024)  # Bộ nhớ đã sử dụng
                    }

    # Nếu không tìm thấy lời giải
    end_time = time.time()
    return None, {
        'steps': 0,
        'weight': 0,
        'nodes': nodes_generated,
        'time': (end_time - start_time) * 1000,
        'memory': (sys.getsizeof(visited) + sys.getsizeof(queue)) / (1024 * 1024)
    }

def get_possible_moves(weights, maze, position, rocks, initial_rocks_positions, switches):
    moves = []
    x, y = position

    directions = [
        ((0, 1), 'r', 'R'),  # Di chuyển phải, đẩy đá sang phải
        ((1, 0), 'd', 'D'),  # Di chuyển xuống, đẩy đá xuống
        ((0, -1), 'l', 'L'),  # Di chuyển trái, đẩy đá sang trái
        ((-1, 0), 'u', 'U')   # Di chuyển lên, đẩy đá lên
    ]

    for (dx, dy), move_action, push_action in directions:
        new_x, new_y = x + dx, y + dy

        if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]):
            # Kiểm tra nếu ô tiếp theo là ô trống, công tắc
            if (maze[new_x][new_y] in (' ', '.', '+', '*') or (new_x, new_y) in initial_rocks_positions or (new_x, new_y) in switches) and (new_x, new_y) not in rocks:
                moves.append(((new_x, new_y), rocks, move_action, 1))  # Di chuyển thì chi phí là 1

            # Nếu ô tiếp theo có đá, kiểm tra điều kiện đẩy đá
            elif (new_x, new_y) in rocks:
                push_x, push_y = new_x + dx, new_y + dy  # Vị trí sau viên đá
                rock_index = rocks.index((new_x, new_y))
                rock_weight = weights[rock_index]

                # Kiểm tra giới hạn của vị trí sau viên đá
                if 0 <= push_x < len(maze) and 0 <= push_y < len(maze[0]):
                    # Ô sau viên đá phải là trống hoặc là công tắc và không có đá khác
                    if maze[push_x][push_y] in (' ', '.', '+', '*') and (push_x, push_y) not in rocks:
                        new_rocks = list(rocks)
                        new_rocks[rock_index] = (push_x, push_y)  # Cập nhật vị trí của đá
                        moves.append(((new_x, new_y), tuple(new_rocks), push_action, rock_weight))  # Đẩy đá thì chi phí là trọng lượng viên đá

    return moves