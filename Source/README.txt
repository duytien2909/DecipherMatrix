# Hướng dẫn chạy chương trình

## Giới thiệu
Chương trình này bao gồm các thuật toán tìm kiếm như BFS, DFS, UCS, và A*, cùng với giao diện người dùng (GUI) để hiển thị kết quả tìm kiếm trong bài toán mê cung.

## Yêu cầu
- Python 3.x (khuyến nghị sử dụng Python 3.8 trở lên)
- Các thư viện cần thiết được liệt kê trong file `requirements.txt`

# Các file chính
- bfs.py: Chứa thuật toán tìm kiếm theo chiều rộng (BFS).
- dfs.py: Chứa thuật toán tìm kiếm theo chiều sâu (DFS).
- ucs.py: Chứa thuật toán tìm kiếm chi phí đồng nhất (UCS).
- astar.py: Chứa thuật toán tìm kiếm A*.
- utils.py: Các hàm trợ giúp chung cho các thuật toán tìm kiếm.
- GUI.py: Chứa giao diện người dùng cho chương trình.
- main.py: Chứa chương trình chính, kết hợp các thuật toán và giao diện.

## Cài đặt
1. **Tạo môi trường ảo** (khuyến nghị nhưng không bắt buộc):
    ```bash
    python -m venv env
    source env/bin/activate      # Trên MacOS/Linux
    .\env\Scripts\activate       # Trên Windows

2. Cài đặt các thư viện cần thiết:
    ```bash
    pip install -r requirements.txt

## Cách chạy chương trình
Để khởi động chương trình, sử dụng lệnh sau:
    ```bash
    python main.py

## Lưu ý
Đảm bảo đã cài đặt đầy đủ các thư viện trong requirements.txt trước khi chạy chương trình.
Nếu gặp lỗi, kiểm tra lại phiên bản Python và các thư viện đã cài đặt để đảm bảo tính tương thích.