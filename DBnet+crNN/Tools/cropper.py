

import numpy as np
import cv2
import os

class Imgmaster():
    def __init__(self,img_dir,pos_dir,mid_dir):
        self.img_dir = img_dir
        self.pos_dir = pos_dir
        self.mid_dir = mid_dir

    def cropper(self,path,array,mkpos):
        # img = cv2.imread("../img_10.png")
        img = cv2.imread(path)
        # pts = np.array([[34,81],[152,72],[155,106],[37,115]])
        pts = np.array(array)
        pts = np.array([pts])
        mask = np.zeros(img.shape[:2], np.uint8)
        cv2.polylines(mask, pts, 1, 255)
        cv2.fillPoly(mask, pts, 255)
        dst = cv2.bitwise_and(img, img, mask=mask)
        bg = np.ones_like(img, np.uint8) * 255
        cv2.bitwise_not(bg, bg, mask=mask)
        dst_white = bg + dst
        cropped = dst_white[mkpos[0]:mkpos[1], mkpos[2]:mkpos[3]]
        # cv2.imwrite("res.jpg", cropped)
        return cropped


    def rgb_equalHist(self,img,add):
        (b, g, r) = cv2.split(img)
        bH = cv2.equalizeHist(b)
        gH = cv2.equalizeHist(g)
        rH = cv2.equalizeHist(r)
        res = cv2.merge((bH, gH, rH))
        cv2.imwrite(add, res)
        return res

    def pos_convert(self,array):
        res = []
        res.append([int(array[0]),int(array[1])])
        res.append([int(array[2]), int(array[3])])
        res.append([int(array[4]), int(array[5])])
        res.append([int(array[6]), int(array[7])])
        return res

    def mkconvert(self,array):
        # print(array)
        ylist = []
        xlist = []
        reslist = []
        for i in array:
            ylist.append(i[1])
            xlist.append(i[0])
        sty = sorted(ylist)
        stx = sorted(xlist)
        # print(sty,stx)
        reslist.append(sty[0])
        reslist.append(sty[3])
        reslist.append(stx[0])
        reslist.append(stx[3])
        return reslist

    def worker(self):
        pic = './DBNet/datasets/icdar/pred_img/test.jpg'
        posadd = './DBNet/outputs_pred/img_text/res_test.txt'
        f = open(posadd)
        poss = []
        for line in f:
            if line:
                raw_pos = line.strip().split(',')
                pos_res = self.pos_convert(raw_pos)
                poss.append(pos_res)
        for i in range(len(poss)):
            res_add = './midfiles/'+str(i)+'.jpg'
            # print(res_add)
            mkpos = self.mkconvert(poss[i])
            res = self.cropper(pic,poss[i],mkpos)
            self.rgb_equalHist(res,res_add)
        return 1

def run():
    print(os.getcwd())
    os.chdir('../DBnet+crNN/')
    img_dir = r'./DBNet/datasets/icdar/pred_img/'
    print(os.listdir(img_dir))
    pos_dir = r'./DBNet/output_pred/img_text/'
    mid_dir = r'./midfiles/'
    p = Imgmaster(img_dir,pos_dir,mid_dir)
    res = p.worker()
    # print(res)

if __name__ == '__main__':
    run()
