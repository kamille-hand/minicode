# coding:utf-8
from PIL import Image
import os

if __name__ == "__main__":
    os.chdir("G:/组会/202012_CAM")
    imgs = os.listdir()
    print(imgs)
    imglist = []
    for img in imgs:
        if img[-3:] == "jpg":
            imglist.append(Image.open(img))
    ori = imglist[-1]
    best = imglist[-2]
    imglist = imglist[:-2]
    for _ in range(5):
        imglist.insert(0, ori)
        imglist.append(best)
    ori.save("009781.gif", save_all=True, append_images=imglist, loop=0, duration=200)
