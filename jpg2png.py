import cv2
import os


def charge(input_path,ouput_path):
    flies = os.listdir(input_path)      #获取所有图片的名称，保存为列表
#    print(flies)

    for ii in range(len(flies)):
#        print(flies)
#        im = Image.open(input_path+'/'+flies[ii])
 
        im = cv2.imread(input_path+'/'+flies[ii])       #读取图片

            #im = Image.open("./tmp.jpg")
        cv2.imwrite(ouput_path +'/'+ flies[ii][:-4] + ".png",im,)  #保存为png

 
if __name__ == '__main__':

    input_path = './1' #读取图片输入路径
    ouput_path = './2'  #图片输出路径
    
    charge(input_path,ouput_path)