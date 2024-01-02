import pandas as pd
import ast
import pickle

# Block or Target
a = 'Target'

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
# print(block_shapes[0], len(block_shapes[0]))
