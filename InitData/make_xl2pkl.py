import pandas as pd
import ast
import pickle
import numpy as np

# Block or Target
a = 'Block'
# a = 'Target'

b = 0
if a == 'Target':
    b = 1

def read_excel_block_shape_data(file_path):
    df = pd.read_excel(file_path, header=None)
    block_shapes = []

    for i in range(1, len(df), 7 + b):
        shape = [ast.literal_eval(row.values[0]) for _, row in df.iloc[i:i+5+b, :].iterrows()]
        if a == 'Target':
            for _ in range(8):
                shape.insert(0,[0] * 35)
        block_shapes.append(shape)
    return block_shapes

file_path = f"{a}_Shape.xlsx"
block_shapes = read_excel_block_shape_data(file_path)

with open(f'{a}_Shape_data.pkl', 'wb') as f:
    pickle.dump(block_shapes, f)
    
# # check all block make correct
# for i, matrix in enumerate(block_shapes):
#     if isinstance(matrix[0], tuple):
#         matrix = [list(m[0]) for m in matrix]
#     matrix_flat = [element for row in matrix for element in row]  # 2D 배열을 1D 리스트로 평탄화
#     matrix_sum = sum(matrix_flat)  # 각 원소 전체의 합
#     print(f"block_shapes[{i}] : {matrix}, sum : {matrix_sum}")

# # b sequence
# # 엑셀 파일 읽기
# file_path = 'option_sequence.xlsx'
# df = pd.read_excel(file_path)

# # 'option a'와 'option b'의 인덱스를 배열로 저장
# option_a_indices = df.iloc[:, 1].tolist()  # 2열이므로 인덱스는 1
# option_b_indices = df.iloc[:, 3].tolist()  # 4열이므로 인덱스는 3

# # 배열을 각각 pickle 파일에 저장
# with open('b1_sequence.pkl', 'wb') as b1_file:
#     pickle.dump(option_a_indices, b1_file)

# with open('b2_sequence.pkl', 'wb') as b2_file:
#     pickle.dump(option_b_indices, b2_file)

# print("Data saved to b1_sequence.pkl and b2_sequence.pkl.")
