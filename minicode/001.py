#coding:utf-8
import os
import shutil

# 分类成功与失败图片，放入两个文件夹
# 特点：图片前六位为数字序号，第七位-代表成功图片，需要将其同一序号所有图片移至成功文件夹

if __name__ == "__main__":
    raw_file_path = 'D:/DL/result/CAM/'
    success_file_folder_name = 'success'
    failure_file_folder_name = 'failure'

    os.chdir(raw_file_path)
    os.mkdir(success_file_folder_name)
    os.mkdir(failure_file_folder_name)
    file_names = os.listdir(raw_file_path)

    target_file_num = set()
    for file_name in file_names:
        if file_name.find('-') == 6:
            target_file_num.add(file_name[:6])
    # print(target_file_num)
    for file_name in file_names:
        if file_name[:6] in target_file_num:
            shutil.copy(file_name,success_file_folder_name+'/'+file_name)
        else:
            shutil.copy(file_name,failure_file_folder_name+'/'+file_name)
        os.remove(file_name)
    

            
