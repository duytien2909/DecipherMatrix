import tkinter as tk
from PIL import Image, ImageTk
import time
import sys
import os

# Kích thước mỗi ô
CELL_SIZE = 40

# Lấy đường dẫn file input và output
if len(sys.argv) != 3:
    print("Usage: python GUI.py <input_file_path> <output_file_path>")
    sys.exit(1)
input_file_path = sys.argv[1]   # Lúc này chỉ mới là input-xx.txt
output_file_path = sys.argv[2]  # Lúc này chỉ mới là output-xx.txt
input_file_path = os.path.join('inputs', input_file_path)  # Tạo đường dẫn "inputs/input-xx.txt"
output_file_path = os.path.join('outputs', output_file_path)  # Tạo đường dẫn "outputs/output-xx.txt"

# Khởi tạo các biến
player_pos = None
rock_positions = []
goal_pos = []
map_data = []
rock_weightList= []
total_move=0
total_push=0
is_paused = False  # Biến để kiểm soát trạng thái tạm dừng
isEnd = False # Biến kiểm tra chạy xong chương trình chưa
isReset=False # Biến cho biết map đã được reset khi đang chạy vòng lặp.
# Đọc dữ liệu từ file
def read_map_from_file(file_path):
    global player_pos, rock_positions, goal_pos, map_data
    rock_positions = []  # Danh sách lưu trữ vị trí của các viên đá
    goal_pos = []  # Danh sách lưu trữ vị trí của các điểm đích
    map_data.clear()
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            rock_numbers = lines[0].strip().split()  # Lấy danh sách số để hiển thị lên viên đá
            
            max_length = max(len(line.strip()) for line in lines[1:])  # Tìm chiều dài tối đa của các dòng
            
            for row_index, line in enumerate(lines[1:]):  # Lưu row_index
                row = list(line.strip())
                
                # Thêm khoảng trống vào hàng ngắn hơn
                if len(row) < max_length:
                    row += [' '] * (max_length - len(row))
                    
                map_data.append(row)
                
                for col, char in enumerate(row):
                    if char == '@' or char =='+':
                        player_pos = [row_index, col]  # Lưu vị trí nhân vật
                    elif char == '$' or char == '*':
                        rock_positions.append((row_index, col))  # Lưu vị trí viên đá
                    if char == '.' or char== '*' or char == '+':
                        goal_pos.append((row_index, col))  # Lưu vị trí điểm đích
            print(goal_pos)
            return rock_positions, rock_numbers  # Trả về danh sách vị trí đá và danh sách số
    except FileNotFoundError:
        print(f"File {file_path} không tồn tại.")
        return [], []

# Đọc hành động từ file
def read_actions_from_file(file_path):
    actions = []
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            for i in range(0, len(lines), 3):
                method_name = lines[i].strip()  # Dòng đầu tiên là tên phương pháp
                # Dòng thứ hai không quan trọng
                if i + 2 < len(lines):
                    action_steps = lines[i + 2].strip()  # Dòng thứ ba là các bước di chuyển
                    actions.append((method_name, action_steps))
        return actions
    except FileNotFoundError:
        print(f"File {file_path} không tồn tại.")
        return []

# Vẽ bản đồ
def draw_map(canvas, method_name=None):
    # Xóa nội dung cũ trước khi vẽ lại
    canvas.delete("all")
    for row in range(len(map_data)):
        for col in range(len(map_data[row])):  # Sử dụng len(map_data[row]) để đảm bảo không vượt quá chỉ số
            x0, y0 = col * CELL_SIZE, row * CELL_SIZE  # x0 là vị trí cột, y0 là vị trí hàng
            x1, y1 = x0 + CELL_SIZE, y0 + CELL_SIZE
            if map_data[row][col] == '#':  # Bức tường
                canvas.create_rectangle(x0, y0, x1, y1, fill="brown")  
            elif map_data[row][col] == ' ':  # Ô trống
                canvas.create_rectangle(x0, y0, x1, y1, fill="lightgrey")
            elif map_data[row][col] == '.' or map_data[row][col] == '*' or map_data[row][col] =='+':  # Điểm đích
                canvas.create_oval(x0 + 10, y0 + 10, x1 - 10, y1 - 10, fill="red")  # Vẽ ô điểm đích
            elif map_data[row][col] == '@' or map_data[row][col] =='+':  # Nhân vật
                canvas.create_rectangle(x0, y0, x1, y1, fill="lightgrey")
            elif map_data[row][col] == '$' or map_data[row][col] == '*':  # Viên đá
                canvas.create_rectangle(x0, y0, x1, y1, fill="lightgrey")
            else:
                canvas.create_rectangle(x0, y0, x1, y1, fill="lightgrey") # Vẽ ô hiện thuật toán
    
    if method_name:
        canvas.create_text(
            (len(map_data[0]) * CELL_SIZE) // 2, 
            len(map_data) * CELL_SIZE + (CELL_SIZE *0.5),  # Vị trí y của tên thuật toán ở giữa dòng cuối
            text=method_name, 
            fill="black", 
            font=("Arial", 16, "bold")
        )

    # Ô chứa tổng số move
    canvas.create_text(
            (len(map_data[0]) * CELL_SIZE) // 2, 
            len(map_data) * CELL_SIZE + (CELL_SIZE * 1.5),  
            text=f"total move is: {total_move}", 
            fill="green", 
            font=("Arial", 16, "bold")
    )

    # Ô chứa tổng số push
    canvas.create_text(
            (len(map_data[0]) * CELL_SIZE) // 2, 
            len(map_data) * CELL_SIZE + (CELL_SIZE * 2.5),  
            text=f"total push is: {total_push}", 
            fill="green", 
            font=("Arial", 16, "bold")
    )

# Hàm reset map
def reset_positions():
    global player_pos, rock_positions
    player_pos = None
    rock_positions = []
    
    for row_index, row in enumerate(map_data):
        for col_index, char in enumerate(row):
            if char == '@' or char =='+':
                player_pos = [row_index, col_index]  # Đặt lại vị trí nhân vật
            elif char == '$' or char == '*':
                rock_positions.append((row_index, col_index))  # Đặt lại vị trí viên đá

def place_elements(canvas, player_img, rock_img, rock_numbers, method_name=None):
    # Xóa nội dung cũ trước khi vẽ lại
    canvas.delete("all")
    draw_map(canvas, method_name)

    # Vẽ nhân vật
    px, py = player_pos
    canvas.create_image(py * CELL_SIZE + CELL_SIZE // 2, px * CELL_SIZE + CELL_SIZE // 2, image=player_img)

    # Vẽ viên đá
    for (rx, ry), number in zip(rock_positions, rock_numbers):
        canvas.create_image(ry * CELL_SIZE + CELL_SIZE // 2, rx * CELL_SIZE + CELL_SIZE // 2, image=rock_img)
        # Hiển thị số lên viên đá
        canvas.create_text(ry * CELL_SIZE + CELL_SIZE // 2, rx * CELL_SIZE + CELL_SIZE // 2, text=number, fill="white", font=("Arial", 16, "bold"))

# Kiểm tra di chuyển có hợp lệ không
def can_move_to_position(x, y):
    if map_data[y][x] == '#':
        return False
    return True

# Hàm di chuyển nhân vật
def move_player(action,rock_numbers):
    global total_push,total_move
    dx, dy = 0, 0
    if action == 'U' or action == 'u':
        dy = -1
    elif action == 'D' or action == 'd':
        dy = 1
    elif action == 'L' or action == 'l':
        dx = -1
    elif action == 'R' or action == 'r':
        dx = 1

    new_x = player_pos[1] + dx
    new_y = player_pos[0] + dy

    if (new_y, new_x) in rock_positions:
        rock_index = rock_positions.index((new_y, new_x))
        new_rock_x = rock_positions[rock_index][1] + dx
        new_rock_y = rock_positions[rock_index][0] + dy

        if can_move_to_position(new_rock_x, new_rock_y):
            # Cập nhật vị trí viên đá và nhân vật
            rock_positions[rock_index] = (new_rock_y, new_rock_x)  # Cập nhật vị trí viên đá
            player_pos[0] = new_y
            player_pos[1] = new_x
            total_move+=1
            total_push+=int(rock_numbers[rock_index])
    elif can_move_to_position(new_x, new_y):
        player_pos[0] = new_y
        player_pos[1] = new_x
        total_move+=1

def pause_or_resume():
    global is_paused
    is_paused = not is_paused

def reset_map():
    global actions,isReset
    rock_positions, rock_numbers = read_map_from_file(input_file_path)  # Đọc lại bản đồ
    actions = read_actions_from_file(output_file_path)  # Đọc lại hành động
    reset_positions()  # Đặt lại vị trí nhân vật và đá
    draw_map(canvas)  # Vẽ lại bản đồ
    isReset=True
    print(isReset)


# Tạo cửa sổ tkinter
root = tk.Tk()
root.title("Ares")

# Đọc bản đồ từ file
rock_positions, rock_numbers = read_map_from_file(input_file_path)
    
# Đọc các hành động từ file
actions = read_actions_from_file(output_file_path)

# Kiểm tra nếu map_data không rỗng trước khi tạo canvas
if map_data:
    canvas = tk.Canvas(root, width=len(map_data[0]) * CELL_SIZE, height=(len(map_data)+3) * CELL_SIZE)
    canvas.pack()
    # Tải ảnh nhân vật và viên đá
    player_image = Image.open("images/player_image.png")
    player_image = player_image.resize((CELL_SIZE, CELL_SIZE), Image.LANCZOS)
    player_img = ImageTk.PhotoImage(player_image)

    rock_image = Image.open("images/rock_image.png")
    rock_image = rock_image.resize((CELL_SIZE, CELL_SIZE), Image.LANCZOS)
    rock_img = ImageTk.PhotoImage(rock_image)

    button_border_ps = tk.Frame(root, highlightbackground = "black",  highlightthickness = 2, bd=0) 
    pause_button = tk.Button(button_border_ps, text="Pause", bg='grey', fg='black', command=pause_or_resume, width=22,height=3, font=("Arial", 14))
    pause_button.pack(side=tk.LEFT)

    button_border_rs = tk.Frame(root, highlightbackground = "black",  highlightthickness = 2, bd=0) 
    reset_button = tk.Button(button_border_rs, text="Reset", bg='grey', fg='black', command=reset_map ,width=22,height=3, font=("Arial", 14))
    reset_button.pack(side=tk.LEFT)

    button_border_ps.pack(side=tk.LEFT)
    button_border_rs.pack(side=tk.LEFT)
    
    # Hiện thị các phương pháp tìm kiếm và bản đồ
    print(actions)
    current_action_index = 0  # Khởi tạo chỉ số hành động
    while not isEnd:
        if current_action_index < len(actions):
            method_name, action_steps = actions[current_action_index]
        if canvas.winfo_exists():
            draw_map(canvas, method_name)
        reset_positions()
        print(method_name)
        # Di chuyển nhân vật theo các bước
        solution_found = True  # Biến để kiểm tra có giải pháp hay không
        for action in action_steps:
            while is_paused:
                if not root.winfo_exists():  # Kiểm tra nếu cửa sổ đã bị đóng
                    break  # Thoát khỏi hàm để tránh vòng lặp vô hạn
                root.update()  # Cập nhật giao diện để cho phép các nút hoạt động
                time.sleep(0.1)  # Đợi một khoảng thời gian ngắn để tránh treo máy

            if(isReset):
                root.update()
                print("call reset complete")
                break
            print(action)
            if action == 'N':  # Nếu gặp "No solution found"
                solution_found = False
                break
            move_player(action,rock_numbers)
            # print(f"total move is: {total_move}")
            # print(f"total push is: {total_push}")
            if canvas.winfo_exists():  # Kiểm tra nếu canvas vẫn tồn tại
                draw_map(canvas, method_name)  # Vẽ lại bản đồ sau mỗi di chuyển
            else:
                break
            place_elements(canvas, player_img, rock_img, rock_numbers,method_name)  # Gọi hàm để vẽ nhân vật và viên đá
            canvas.update()
            time.sleep(0.3)  # Đợi một chút để người chơi thấy nhân vật di chuyển

        total_move=0    # Sau 1 thuật toán thì reset giá trị tổng bằng 0    
        total_push=0    # Reset giá trị tổng bằng 0 để bắt đầu tính toán thuật toán khác
        print('\n')
        current_action_index += 1  # Tăng chỉ số sau khi xử lý xong
        if(isReset):
            current_action_index=0  #Đặt lại giá trị đọc khi reset
            isReset=False
            continue

        if current_action_index > len(actions):
            isEnd=True
        time.sleep(1)

    root.destroy()
root.mainloop()