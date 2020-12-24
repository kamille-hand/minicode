import os
import csv
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == "__main__":
    folderpath = 'D:/DL/result/CAM_alpha/blur_params_csv/'
    filenames = os.listdir(folderpath)
    os.chdir(folderpath)
    # with open('sts.csv','w',encoding='utf-8',newline='') as f1:
    #     csv_writer = csv.writer(f1)
    #     csv_writer.writerow(['','class_index','value','percentage',str_handle,'S','L','theta','delta'])
    #     for filename in filenames:
    #         if filename.find('.txt')!=-1:
    #             # print(filename)
    #             with open(filename,'r') as f:
    #                 ll = f.readlines()
    #                 target_line = ll[0] + ll[-4] + ll[-3] + ll[-2] + ll[-1]
    #                 target_line = target_line.replace('\n','\t').split('\t')[:-1]
    #                 target_line[0] = filename.strip('.txt')
    #                 # print(target_line)
    #                 csv_writer.writerow(target_line)
    #                 f.close()
    #     f1.close()
    filenames = [filename for filename in filenames if filename[-3:]=='csv']
    for filename in filenames:
        sts = pd.read_csv(filename)
        str_handle = 'cls_name'
        class_name = sts[str_handle]
        c = class_name.value_counts(ascending=False)
        c = c[c.array > 100]
        for fre_class in c.index:
            s = sts.loc[class_name==fre_class]
            print(s.head(1))
            sns.kdeplot(s.iloc[:,-1],label=fre_class,shade=True)
        plt.xlim(0,360)
        plt.savefig(f'{filename[:-4]}_kde_delta.jpg')
        plt.close()
        for fre_class in c.index:
            s = sts.loc[class_name==fre_class]
            print(s.head(1))
            sns.kdeplot(s.iloc[:,-2],label=fre_class,shade=True)
        plt.xlim(0,10)
        plt.savefig(f'{filename[:-4]}_kde_theta.jpg')
        plt.close()
        for fre_class in c.index:
            s = sts.loc[class_name==fre_class]
            print(s.head(1))
            sns.kdeplot(s.iloc[:,-3],label=fre_class,shade=True)
        plt.xlim(0,10)
        plt.savefig(f'{filename[:-4]}_kde_L.jpg')
        plt.close()
    #    sns.kdeplot(s.iloc[:,-2])
    #    plt.savefig(f'{filename[:-4]}_{fre_class}_theta.jpg')
    #    plt.close()
    #    sns.kdeplot(s.iloc[:,-3])
    #    plt.savefig(f'{filename[:-4]}_{fre_class}_L.jpg')
    #    plt.close()
    # fig = plt.figure(figsize=(8,4))
    # sns.jointplot(x=s['delta'],y=s['theta'],kind='kde')
    # plt.savefig('water_bottle.png')
    # plt.show()

    # chosen_class = class_name.isin(fre_class)
    # print(s)
    # fig_size = (8,4)
    # fig1 = plt.figure(figsize=fig_size)
    # sns.swarmplot(x=sts[str_handle].loc[chosen_class],y=sts['theta'].loc[chosen_class])
    # fig1.savefig('theta.png')
    # fig2 = plt.figure(figsize=fig_size)
    # sns.swarmplot(x=sts[str_handle].loc[chosen_class],y=sts['L'].loc[chosen_class])
    # fig2.savefig('L.png')
    # fig3 = plt.figure(figsize=fig_size)
    # sns.swarmplot(x=sts[str_handle].loc[chosen_class],y=sts['S'].loc[chosen_class])
    # fig3.savefig('S.png')
    # fig4 = plt.figure(figsize=fig_size)
    # sns.swarmplot(x=sts[str_handle].loc[chosen_class],y=sts['delta'].loc[chosen_class])
    # fig4.savefig('delta.png')
    # plt.show()