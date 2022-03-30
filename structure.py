import pandas as pd
import docker
import os
from multiprocessing import Pool
import tqdm


def pool_func(idx_seq):
    idx, seq = idx_seq

    with open(f'data/fasta/tmp{idx}.fa', 'w') as f:
        lines = f">tmp{idx}\n{seq}"
        f.writelines(lines)
    
    preds_bytes = client.containers.run("centroid_fold", f"centroid_fold -g -1 data/fasta/tmp{idx}.fa", volumes=[f"{os.getcwd()}:/workspaces"])
    preds = [x for x in preds_bytes.decode("utf-8").split('\n')[2:-1]]

    stats = [{**{x.split('=')[0].replace('(',''):x.split('=')[1].replace(')','') for x in pred.split(' ')[1].split(',')}, **{'Centroid':pred.split(' ')[0]}}
    for pred in preds]

    df_stats = pd.DataFrame(stats)
    df_stats['Sequence'] = seq
    df_stats.to_csv(f'data/output/seq{idx}.csv')

    return 


client = docker.from_env()

TARGET = 'ENTER YOUR CSV'

df = pd.read_csv('')
idx_seqs = list(enumerate(df['Sequence'].values))

if __name__ == "__main__":
    with Pool() as p:
        output = list(tqdm.tqdm(p.imap(pool_func, idx_seqs), total=len(idx_seqs)))
