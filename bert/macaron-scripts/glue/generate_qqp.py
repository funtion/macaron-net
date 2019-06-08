import argparse
import csv
import os

import torch

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data", type=str,
                        help="path of data")
    parser.add_argument("--output", type=str, required=True,
                        help="path of output")
    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.mkdir(args.output)
    elif not os.path.isdir(args.output):
        raise FileExistsError(f"{args.output} is not a directory")
    labels = []
    with open(os.path.join(args.data, "train.tsv"), "r", encoding="utf-8") as fi, open(
            os.path.join(args.output, "train.txt"), "w", encoding="utf-8") as fo:
        reader = csv.reader(fi, delimiter="\t", quotechar=None)
        for line in reader:
            if line[0] == "id" and line[1] == "qid1" and line[2] == 'qid2' and line[3] == 'question1' and line[4] == 'question2' and line[5] == 'is_duplicate':
                continue
            if len(line) != 6:
                # print(line)
                continue
            fo.write(f'{line[3]}\n{line[4]}\n')
            labels.append(int(line[5]))
    torch.save(torch.LongTensor(labels), os.path.join(args.output, "train_labels.pt"))
    labels = []
    with open(os.path.join(args.output, "valid.txt"), "w", encoding="utf-8") as fo:
        with open(os.path.join(args.data, "dev.tsv"), "r", encoding="utf-8") as fi:
            reader = csv.reader(fi, delimiter="\t", quotechar=None)
            for line in reader:
                if line[0] == "id" and line[1] == "qid1" and line[2] == 'qid2' and line[3] == 'question1' and line[4] == 'question2' and line[5] == 'is_duplicate':
                    continue
                if len(line) != 6:
                    # print(line, 'valid')
                    continue
                fo.write(f'{line[3]}\n{line[4]}\n')
                labels.append(int(line[5]))
    torch.save(torch.LongTensor(labels), os.path.join(args.output, "valid_labels.pt"))
    with open(os.path.join(args.output, "test.txt"), "w", encoding="utf-8") as fo:
        with open(os.path.join(args.data, "test.tsv"), "r", encoding="utf-8") as fi:
            reader = csv.reader(fi, delimiter="\t", quotechar=None)
            for line in reader:
                if line[0] == "id" and line[1] == "question1" and line[2] == 'question2':
                    continue
                if len(line) != 3:
                    # print(line, 'test')
                    continue
                fo.write(f'{line[1]}\n{line[2]}\n')


if __name__ == '__main__':
    main()
