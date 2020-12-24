import os
import numpy as np
import random
import csv
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


def plotAndSelect():
    path = "G:/usslab_blur_attack/20201129"
    dataRange = {
        0:(2,5),1:(2,5),2:(2,5),3:(2,5),
        4:(2,5),5:(2,5),6:(2,5),7:(2,5),
        8:(2,5),9:(2,5),10:(2,5),11:(2,5),
        12:(2,5),13:(2,5),14:(2,5),15:(2,5),
        16:(2,5),17:(2,5),18:(2,5),19:(2,5),
        20:(4,8),21:(9,11),22:(3,7),23:(3,9),
        24:(6,10),25:(6,10),26:(8,12),27:(5,10),
    }
    dataDetail = {
        0:(1,37),1:(1,50),2:(1,60),3:(1,65),
        4:(1,72),5:(1,80),6:(2,48),7:(2,61),
        8:(2,67),9:(2,76),10:(2,86),11:(3,77),
        12:(3,83),13:(3,70),14:(3,65),15:(3,51),
        16:(4,71),17:(4,76),18:(4,81),19:(4,64),
        20:(5,64),21:(5,71),22:(5,76),23:(5,81),
        24:(6,64),25:(6,71),26:(6,76),27:(6,81),
    }
    groupName = {
        1:"white noise",
        2:"people talking",
        3:"sine wave",
        4:"ultrasonic attack",
        5:"metal box defense",
        6:"metamaterial defense",
    }
    os.chdir(path)
    csvFiles = os.listdir()
    sdf = pd.DataFrame(columns=['filename','rad/s','group','db'])
    print(sdf.head())
    # sns.set_theme()
    for csvFile in csvFiles:
        num = int(csvFile[csvFile.find('_')+1:csvFile.find('.')])
        chosen = list(dataRange[num])
        df = pd.read_csv(csvFile, index_col=0, usecols=[0,4])
        df = df[(df.index>chosen[0])&(df.index<chosen[1])]
        # print(df.columns.unique())
        res = df.mean().iloc[0]
        sdf = sdf.append({'filename':csvFile,'rad/s':res,
            'group':groupName[dataDetail[num][0]],'db':dataDetail[num][1]}, ignore_index=True)
        print(sdf.head())
        # fig = plt.figure(figsize=(6,6))
        # sns.lineplot(data=df)
        # plt.show()
    os.chdir('G:/python')
    sdf.to_csv('sts.csv')


def plotWhatIWant():
    df = pd.read_csv('sts.csv',index_col=0,usecols=[0,2,3,4])
    df1 = df[df["group"].isin(["white noise","people talking","sine wave","ultrasonic attack"])]
    # df2 = df[df["group"].isin(["ultrasonic attack","metal box defense","metamaterial defense"])]
    # print(df.head())
    # sns.set_theme()
    fig = plt.figure(figsize=(5,3))
    sns.lineplot(x="db",y="rad/s",hue="group",style="group",markers=True,dashes=True,data=df1)
    plt.savefig("fig1.jpg")
    plt.close()
    # fig = plt.figure(figsize=(5,3))
    # sns.lineplot(x="db",y="rad/s",hue="group",style="group",markers=True,dashes=False,data=df2)
    # plt.savefig("fig2.jpg")
    # plt.close()
    # print(df.head())


if __name__ == "__main__":
    # plotAndSelect()
    plotWhatIWant()
