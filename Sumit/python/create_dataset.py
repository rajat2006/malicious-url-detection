import pandas as pd
benign_set = pd.read_csv('dataset/benign_url.csv')
malicious_set = pd.read_csv('dataset/malicious_url.csv')[['url']]
malicious_set.insert(1, 'label', 1)

min_length = min(len(malicious_set), len(benign_set))
dataset = malicious_set.append(benign_set, ignore_index=True).sample(frac=1).reset_index(drop=True)
#dataset = malicious_set[:min_length].append(benign_set[:min_length], ignore_index=True).sample(frac=1).reset_index(drop=True)
dataset.to_csv('final_dataset.csv',index=False)