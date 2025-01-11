import heapq
import time
import sys

def astar(weights, maze, start, rocks, switches):
    start_time = time.time()
    open_list = []
    heapq.heappush(open_list, (0, start, tuple(rocks), "", 0))  

    visited = set([(start, tuple(rocks))])
    nodes_generated = 0
    g_scores = {(start, tuple(rocks)): 0}
    
    while open_list:
        f_score, current_pos, current_rocks, path, total_weight = heapq.heappop(open_list)

        # Kiểm tra nếu tất cả các viên đá đã được đẩy vào công tắc
        if all(rock in switches for rock in current_rocks):
            end_time = time.time()
            return path, {
                'steps': len(path),
                'weight': total_weight,
                'nodes': nodes_generated,
                'time': (end_time - start_time) * 1000,
                'memory': (sys.getsizeof(visited) + sys.getsizeof(open_list)) / (1024 * 1024)
            }

        possible_moves = get_possible_moves(maze, current_pos, current_rocks, weights)
        for new_pos, new_rocks, action, weight_increase in possible_moves:
            new_state = (new_pos, tuple(new_rocks))
            new_g_score = g_scores[(current_pos, tuple(current_rocks))] + weight_increase  
            
            if new_state not in visited or new_g_score < g_scores.get(new_state, float('inf')):
                g_scores[new_state] = new_g_score
                new_f_score = new_g_score + heuristic(new_pos, new_rocks, switches, weights)
                
                heapq.heappush(open_list, (new_f_score, new_pos, new_rocks, path + action, total_weight + weight_increase))
                visited.add(new_state)  
                nodes_generated += 1
    
    # Nếu không tìm thấy lời giải
    end_time = time.time()
    return None, {
        'steps': 0,
        'weight': 0,
        'nodes': nodes_generated,
        'time': (end_time - start_time) * 1000,
        'memory': (sys.getsizeof(visited) + sys.getsizeof(open_list)) / (1024 * 1024)
    }

def heuristic(posAres, posStone, posSwitch, weights):
    # Tổng hợp khoảng cách từ Ares đến tất cả các viên đá
    total_distance = 0
    
    # Tạo danh sách chứa các viên đá và trọng số tương ứng
    stones_weight = list(zip(posStone, weights))
    
    # Sắp xếp theo trọng lượng (nếu cần)
    stones_weight = sorted(stones_weight, key=lambda x: x[1], reverse=True)
    
    # Tính tổng khoảng cách từ Ares đến tất cả các viên đá
    for stone, weight in stones_weight:
        total_distance += abs(posAres[0] - stone[0]) + abs(posAres[1] - stone[1])
    
    # Tính khoảng cách từ tất cả các viên đá đến các công tắc
    for stone, weight in stones_weight:
        min_distance_to_switch = float('inf')
        for switch in posSwitch:
            distance = abs(stone[0] - switch[0]) + abs(stone[1] - switch[1])
            min_distance_to_switch = min(min_distance_to_switch, distance)
        # Cộng chi phí vào tổng khoảng cách, nhân với trọng số của viên đá
        total_distance += min_distance_to_switch * weight

    return total_distance

def get_possible_moves(maze, position, rocks, weights):
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
        
        # Kiểm tra điều kiện cho ô tiếp theo
        if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]):
            # Nếu ô tiếp theo là ô trống, công tắc hoặc Ares đứng trên công tắc
            if maze[new_x][new_y] in (' ', '.', '+') and (new_x, new_y) not in rocks:
                moves.append(((new_x, new_y), rocks, move_action, 1))  
            
            # Nếu ô tiếp theo có đá, kiểm tra điều kiện đẩy đá
            elif (new_x, new_y) in rocks:
                push_x, push_y = new_x + dx, new_y + dy
                rock_index = rocks.index((new_x, new_y))
                rock_weight = weights[rock_index]
                
                # Kiểm tra điều kiện cho vị trí sau viên đá
                if 0 <= push_x < len(maze) and 0 <= push_y < len(maze[0]):
                    if maze[push_x][push_y] in (' ', '.', '+','*') and (push_x, push_y) not in rocks:
                        new_rocks = list(rocks)
                        new_rocks[rock_index] = (push_x, push_y)
                        moves.append(((new_x, new_y), tuple(new_rocks), push_action, rock_weight))

    return moves