# coding:utf-8
import os


if __name__ == "__main__":
    folder1_path = 'D:/DL/result/CAM/success/'
    folder2_path = 'D:/DL/result/CAM/failure/'
    filenames1 = os.listdir(folder1_path)
    filenames2 = os.listdir(folder2_path)
    filenames1.sort()
    filenames2.sort()

    len1 = len(filenames1)//3
    len2 = len(filenames2)
    print(f'图片总数：{len1+len2:5d}\n'
          f'总成功数：{len1:5d}\n'
          f'总失败数：{len2:5d}\n'
          f'成功率：{len1/(len1+len2)*100:6.2f}%\n'
        )

    defence_rank = dict()
    for i in range(0,len1,3):
        filename = filenames1[i][7:-4].split('+')[0]
        if filename in defence_rank:
            defence_rank[filename][0] += 1
            defence_rank[filename][1] += 1
        else:
            defence_rank[filename] = [1,1,0]
    for filename in filenames2:
        filename = filename[7:-4].split('+')[0]
        if filename in defence_rank:
            defence_rank[filename][0] += 1
            defence_rank[filename][2] += 1
        else:
            defence_rank[filename] = [1,0,1]
    defence_rank = list(defence_rank.items())
    for x in defence_rank:
        x[1].append(100*x[1][1]/x[1][0])
    defence_rank.sort(key=lambda x: x[1][3]*x[1][1],reverse=True)
    # print('成功率排序：基数大于十')
    text1, text2, text3, text4, text5 = '类别', '总数', '成功', '失败', '成功率'
    print(f'{text1:^23}{text2:^4}{text3:^4}{text4:^4}{text5:>5}'
          f'      {text1:^25}{text2:^4}')
    for i in range(15):
        x = defence_rank[i]
        most = dict()
        for j in range(0,len1,3):
            if filenames1[j].find(x[0])!=-1:
                filename = filenames1[j+1][7:-4].split('+')[0]
                if filename in most:
                    most[filename] += 1
                else:
                    most[filename] = 1
        most_sorted = sorted(most,key=lambda x: most[x],reverse=True)
        print(f'{x[0]:^25}{x[1][0]:^6d}{x[1][1]:^6d}{x[1][2]:^6d}{x[1][3]:6.1f}%'
              f'     --->{most_sorted[0]:^25}{most[most_sorted[0]]:^6d}')
    print('\n最容易被攻击的类：')
    attack_rank = dict()
    for i in range(1,len1,3):
        filename = filenames1[i][7:-4].split('+')[0]
        if filename in attack_rank:
            attack_rank[filename] += 1
        else:
            attack_rank[filename] = 1
    attack_rank_list = sorted(attack_rank,key=lambda x: attack_rank[x],reverse=True)
    for i in range(10):
        print(f'{attack_rank_list[i]:^25}{attack_rank[attack_rank_list[i]]:^6d}')


