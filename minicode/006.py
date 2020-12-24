# coding:utf-8
import os
import csv
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def extractFilename(folderPath):
    os.chdir(folderPath)
    filenames = os.listdir()
    with open(
        os.path.split(folderPath)[-1] + ".csv", "w", newline="", encoding="utf-8"
    ) as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["class", "confidence", "S", "L", "theta", "delta"])
        for filename in filenames:
            if filename[-4:] == ".csv":
                continue
            filename = os.path.splitext(filename)[0]
            information = filename.split("-")
            csv_writer.writerow(information)
        f.close()


def concatenateCsv(folderPath):
    os.chdir(folderPath)
    filenames = os.listdir()
    with open("all.csv", "w", newline="", encoding="utf-8") as fw:
        lines = []
        title = True
        for filename in filenames:
            if filename == "all.csv":
                continue
            with open(filename, "r") as fr:
                csv_reader = csv.reader(fr)
                if title:
                    lines.extend(csv_reader)
                    title = False
                else:
                    next(csv_reader)
                    lines.extend(csv_reader)
                fr.close()
        csv_writer = csv.writer(fw)
        csv_writer.writerows(lines)
        fw.close()


def csvSwarmPlot(csvfile):
    df = pd.read_csv(csvfile)
    figsize = (12, 4)
    col = ["confidence"]
    for y in col:
        fig = plt.figure(figsize=figsize)
        sns.swarmplot(x="class", y=y, data=df, size=1)
        plt.savefig(y + ".png")
        plt.close()


def merge():
    with open("../class.csv", "r") as f:
        csv_reader = csv.reader(f)
        iden = dict()
        for x in csv_reader:
            iden[int(x[0])] = int(x[1])
        for x in range(1000):
            if x not in iden:
                iden[x] = -1
        f.close()
    os.chdir("../result/2")
    with open("original_class.txt", "r") as f:
        img2cls = f.readlines()
        img2cls = [x.split(",") for x in img2cls]
        for x in img2cls:
            x[0] = x[0].replace("jpg", "csv")
            x[1] = int(x[1].strip("\n"))
            x.append(iden[x[1]])
            x.append(bigclass[x[2]])
        f.close()
    ddf = None
    for x in img2cls:
        print(x[0])
        df = pd.read_csv(x[0], index_col=0)
        df["imgNum"] = x[0][:-4]
        df["oriIdx"] = x[1]
        df["oriBigClass"] = x[3]
        bc = df["class"].apply(lambda y: bigclass[iden[y]])
        df["bigClass"] = bc
        if ddf is None:
            ddf = df
        else:
            ddf = pd.concat([ddf, df], ignore_index=True)
    ddf.to_csv("all.csv")
    print(ddf.tail())


def main():
    os.chdir("G:/python")
    csvfile = "all.csv"
    df = pd.read_csv(csvfile, index_col=0, usecols=[0, 7, 8, 9, 10])
    df = df.drop_duplicates()
    print(df.shape)
    df.to_csv("duplicates.csv")
    # df = df.groupby(["oriBigClass", "bigClass"]).size().unstack(fill_value=0)
    # fig = plt.figure(figsize=(10, 8))
    # sns.heatmap(data=df, square=True, cmap="YlGnBu", annot=False, linecolor="black")
    # plt.savefig("../result/heatmap_small.png")
    # plt.close()
    # df.to_csv("../result/sts.csv")


if __name__ == "__main__":
    bigclass = [
        "dog",
        "cat",
        "bird",
        "boat",
        "bottle",
        "airplane",
        "bigcar",
        "bicycle",
        "ox",
        "sofa",
        "sheep",
        "fish",
        "tv",
        "smallcar",
        "motorbike",
        "horse",
        "chair",
        "train",
        "table",
        "undefined",
    ]
    """
    workSpace = "D:/boat"
    folders = os.listdir(workSpace)
    folders = [folder for folder in folders if folder.find('.')==-1]
    for folder in folders:
        extractFilename(workSpace + '/' + folder)
    """
    # concatenateCsv("D:/boat/csv")
    # csvSwarmPlot("D:/boat/csv/all.csv")
    # merge()
    main()
