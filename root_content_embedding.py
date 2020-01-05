import torch
import numpy as np
from transformers import BertTokenizer, BertModel
import gc
import pandas as pd

root_content_dir = 'root_content.txt'
weibo_index_list = []
count = 0

tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
model = BertModel.from_pretrained('./bert-base-chinese')
model.eval()
embeddings = None

with open(root_content_dir, encoding='utf-8') as f:
    line = f.readline()
    while line:
        line = line.replace('\n','')
        weibo_index = [line]
        weibo_index_list.append(weibo_index)
        weibo_content = f.readline()

        weibo_content = weibo_content.replace('\n', '')
        tokenized_weibo_content = tokenizer.tokenize(weibo_content)
        if len(tokenized_weibo_content) > 510:
            tokenized_weibo_content = tokenized_weibo_content[:510]
        tokenized_weibo_content = ['[cls]'] + tokenized_weibo_content + ['[sep]']
        indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_weibo_content)  # step 3
        segments_ids = [1] * len(tokenized_weibo_content)  # step 4
        tokens_tensor = torch.tensor([indexed_tokens])
        segments_tensors = torch.tensor([segments_ids])
        with torch.no_grad():  # step 5
            encoded_layers, _ = model(tokens_tensor, segments_tensors)
        token_vecs = encoded_layers[-1][0]
        sentence_embedding = torch.mean(token_vecs, dim=0)
        sentence_embedding = sentence_embedding.unsqueeze(0)
        if embeddings is None:
            embeddings = sentence_embedding
        else:
            embeddings = torch.cat((embeddings, sentence_embedding), dim=0)

        count += 1
        if count % 1000 == 0:
            print("currently extracting sentence embedding of {}".format(count))
        line = f.readline()
        gc.collect()

feature_name = ["features-"] * 768
for i in range(768):
    feature_name[i] = feature_name[i] + str(i)

np_embeddings = embeddings.numpy()
df1 = pd.DataFrame(weibo_index_list, columns=['PostID'])
df2 = pd.DataFrame(np_embeddings, columns=feature_name)
df = pd.concat([df1, df2], axis=1)
df.to_csv("root_content_embeddings.csv")
