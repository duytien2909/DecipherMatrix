def read_maze(file_path):
    """
    Đọc file input và trả về mê cung dưới dạng ma trận.
    """
    with open(file_path, 'r') as f:
        weights = list(map(int, f.readline().strip().split()))  # Đọc danh sách trọng lượng
        maze = [list(line.rstrip()) for line in f]  # Đọc ma trận mê cung, chỉ loại bỏ khoảng trắng cuối dòng
    
    # Xác định vị trí bắt đầu của Ares (@) và vị trí các công tắc (.)
    start = None
    switches = []
    rocks = []
    
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == '@':  # Vị trí bắt đầu của Ares
                start = (i, j)
            elif cell == '.':  # Công tắc
                switches.append((i, j))
            elif cell == '$':  # Đá
                rocks.append((i, j))
            elif cell == '*':  # Đá trên công tắc
                rocks.append((i, j))
                switches.append((i, j))
            elif cell == '+':  # Ares trên công tắc
                start = (i, j)
                switches.append((i, j))
    
    return weights, maze, start, rocks, switches

def write_output(filename, results):
    """
    Ghi kết quả của nhiều thuật toán vào tệp output.
    """
    with open(filename, 'w') as f:
        for algo, (solution, stats) in results.items():
            # Ghi tiêu đề của thuật toán
            f.write(f'{algo}\n')
            # Ghi thống kê kết quả của thuật toán
            f.write(f'Steps: {stats["steps"]}, Weight: {stats["weight"]}, '
                    f'Node: {stats["nodes"]}, Time (ms): {stats["time"]:.2f}, '
                    f'Memory (MB): {stats["memory"]:.2f}\n')
            
            # Ghi chuỗi đường đi của thuật toán nếu có, ngược lại thông báo không có giải pháp
            if solution:
                solution_str = ''.join([str(action) if isinstance(action, str) else ''.join(map(str, action)) for action in solution])
                f.write(solution_str + '\n')
            else:
                f.write('No solution found\n')

def print_maze(maze):
    """
    In mê cung sau khi tìm được lời giải, bao gồm tọa độ của Ares, đá và công tắc.
    """
    ares_position = None
    rocks = []
    switches = []

    # Tạo bản sao của mê cung để có thể chỉnh sửa và đánh dấu
    maze_with_marks = [list(row) for row in maze]

    # Duyệt qua mê cung để tìm tọa độ của Ares, đá và công tắc
    for x, row in enumerate(maze):
        for y, cell in enumerate(row):
            if cell == '@':  # Tìm Ares
                ares_position = (x, y)
                maze_with_marks[x][y] = '@'  # Đánh dấu Ares
            elif cell == '$':  # Tìm đá
                rocks.append((x, y))
                maze_with_marks[x][y] = '$'  # Đánh dấu đá                    
            elif cell == '.':  # Tìm công tắc
                switches.append((x, y))
                maze_with_marks[x][y] = '.'  # Đánh dấu công tắc
            elif cell == '*':  # Tìm đá và công tắc
                rocks.append((x, y))
                switches.append((x, y))
                maze_with_marks[x][y] = '*'  # Đánh dấu đá trên công tắc
            elif cell == '+':  # Tìm Ares và công tắc
                ares_position = (x, y)
                switches.append((x, y))
                maze_with_marks[x][y] = '+'  # Đánh dấu Ares trên công tắc
            

    # In bản đồ
    for row in maze_with_marks:
        print(''.join(row))

    # In ra tọa độ của Ares, đá và công tắc
    print(f"\nAres Position: {ares_position}")
    print(f"Rocks Positions: {rocks}")
    print(f"Switches Positions: {switches}")

def print_solution(solution):
    if solution:
        solution_str = ''.join([str(action) if isinstance(action, str) else ''.join(map(str, action)) for action in solution])
        print(f"Solution Path: {solution_str}")
    else:
        print("No solution found")

def get_solution(solution):
    if solution:
        solution_str = ''.join([str(action) if isinstance(action, str) else ''.join(map(str, action)) for action in solution])
        return solution_str
    else:
        return None