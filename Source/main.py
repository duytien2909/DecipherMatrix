from bfs import bfs
from dfs import dfs
from ucs import ucs
from astar import astar
from utils import read_maze, write_output, print_maze, print_solution
import subprocess


def main():
    # Đọc input
    input_file = input("Nhập tên tệp input (ví dụ: input-01.txt): ")

    # Đọc mê cung và các thông tin từ tệp input
    weights, maze, start, rocks, switches = read_maze(f'inputs/{input_file}')

    # In mê cung
    print(f'\nMê cung {input_file}\n')
    print_maze(maze)
    
    # Tạo một dictionary để lưu trữ kết quả của mỗi thuật toán
    results = {}

    # Chạy các thuật toán và lưu kết quả vào dictionary results
    solution_bfs, stats_bfs = bfs(weights, maze, start, rocks, switches)
    results['BFS'] = (solution_bfs, stats_bfs)

    solution_dfs, stats_dfs = dfs(weights, maze, start, rocks, switches)
    results['DFS'] = (solution_dfs, stats_dfs)

    solution_ucs, stats_ucs = ucs(weights, maze, start, rocks, switches)
    results['UCS'] = (solution_ucs, stats_ucs)

    solution_astar, stats_astar = astar(weights, maze, start, rocks, switches)
    results['A*'] = (solution_astar, stats_astar)

    # Ghi kết quả ra tệp output
    output_file = input_file.replace('input', 'output')
    write_output(f'outputs/{output_file}', results)

    # In lời giải của từng thuật toán
    print("\nKết quả:")
    for algo, (solution, _) in results.items():
        print(f"\n{algo}")

        print_solution(solution)

    # Chạy GUI    
    subprocess.run(['python', 'GUI.py', input_file, output_file])
        
if __name__ == "__main__":
    main()