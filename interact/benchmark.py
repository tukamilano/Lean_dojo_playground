import json
from lean_dojo import *
from searchtree2.py import generate_dataset

def main():
    # JSON ファイルを開く(自分のパスに変更)
    with open("/Users/milano/Downloads/leandojo_benchmark_4/random/train.json", "r") as json_file:
        objects = json.load(json_file)

    entire_dataset = []
    entire_dataset2 = []
    # 並列化して処理を行うのあり（というかやるべき）90000個の定理を並列化して処理する
    for object in objects:
        repo = LeanGitRepo(object['url'], object['commit'])
        theorem = Theorem(repo, object['file_path'], object['full_name'])
        dataset, dataset2 = generate_dataset(theorem)
        entire_dataset.extend(dataset)
        entire_dataset2.extend(dataset2)
    
    return entire_dataset, entire_dataset2

