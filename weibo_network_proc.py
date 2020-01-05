import pandas as pd
import numpy as np


file_name = "./weibo_network/weibo_network.txt"
line_count = 1

with open(file_name, 'r') as f:
    line = f.readline()
    while line:
        if line_count == 1:
            element = line.split()
            N = int(element[0]) # total user number
            M = int(element[1]) # total following number
            in_out_degree = np.zeros((2, N))
            line_count += 1
        else:
            element = line.split()
            uid = int(element[0])
            k = int(element[1])
            in_out_degree[0, uid] = k
            for i in range(k):
                in_out_degree[1, int(element[2*i + 2])] += 1
            line_count += 1
        line = f.readline()
        if not line_count % 10000:
            print('currently processing: {}'.format(line_count))

df = pd.DataFrame(in_out_degree.transpose(), columns=['In-degree', 'Out-degree'])
df.to_csv('./weibo_network_inout_degree.csv')
