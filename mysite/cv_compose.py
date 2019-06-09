import numpy as np
import cv2

#################### 버전 1 #############################################


class Composer:
    def __init__(self):
        pass
    
    def hair_clothes(self):
        input_img = cv2.imread('static/ForComposing.png')     
        output_img = cv2.imread('static/First_output/FirstResult.jpg')


        top_hair = input_img[0:350, 60:660]
        shirt = input_img[750:991, 0:710]

        mt = output_img[20:370, 100:700]

        #블렌딩
        mix = 5
        blended_top = cv2.addWeighted(top_hair, float(100-mix)/100, mt, float(mix)/100, 0)

        #삽입
        output_img[10:360, 100:700] = blended_top
        output_img[755:996, 38:748] = shirt


        filename = 'FinalResult.jpg'
        cv2.imwrite('static/Final_output/'+filename, output_img)