#----------아래의 과정은 객체 생성을 시작으로 한번에 이루어짐

#----------인스턴스 생성시 주어진 파일명을 가지고 파일 읽기를 시도
#----------PredictionExtract함수 에서 사진의 특징점을 numpy array로 추출
#----------Prettify 함수에서 특징점 좌표들을 조정한다.

#----------모든 특징점 좌표는 객체의 shape_2d에 배열로 저장된다.
import cv2, dlib, sys
import numpy as np

class CVloader:

    shape_2d = 0
    img = None


    def __init__(self,file_name):
        try:
            file_path = 'media/image/face.jpg'
            self.img = cv2.imread(file_path, 1)
            print("file read success")

        except:
            print("cannot read file :: name=", file_name)
            
        


        

    def PredictionExtract(self):
        try:
            scaler = 0.3
            detector = dlib.get_frontal_face_detector()
            predictor = dlib.shape_predictor('static/shape_predictor_194_face_landmarks.dat')
        except:
            print("no .dat file")
            return None
        
        faces = detector(self.img)
        face = faces[0]

        dlib_shape = predictor(self.img,face)
        self.shape_2d = np.array([[p.x,p.y] for p in dlib_shape.parts()])

        




    #Adjust coordination for OpenGL
    def Prettify(self):
        #symetrical points for Adjusting
        
        #prettyLine = ((0,16),(1,15),(2,14),(3,13),(4,12),(5,11),(6,10),(7,9))
        prettyEye = ((26,48),(27,49),(28,50),(29,51),(30,52),(31,53),(33,55),
                     (34,56),(35,57),(36,58),(37,59),(38,60),(39,61),(40,62),
                     (41,63),(42,64),(44,66),(45,67),(46,68),(47,69))
                     
        #prettyBrow = ((21,22),(20,23),(19,24),(18,25),(17,26))
        prettyNose = ((135,151),(136,150),(137,149),(138,148),(139,147),(140,146),(141,145),(142,144))
       # prettyLib = ((48,54),(49,53),(50,52),(60,64),(61,63),(67,65),(59,55),(58,56))

        prettyTuple = ( prettyEye,prettyNose)
        prettyAxis =(143)


        for i in range(0,194):
            self.shape_2d[i][1] = self.shape_2d[i][1] * (-1)
            self.shape_2d[i][0] = self.shape_2d[i][0] * (-1)



        # Y좌표 조정
        print(self.shape_2d[26])
        print(self.shape_2d[37])
        print(self.shape_2d[59])
        print(self.shape_2d[48])
        rd = self.shape_2d[37] - self.shape_2d[26]
        ld = self.shape_2d[48] - self.shape_2d[59]
        
        rval = rd[0] - rd[1]
        lval = ld[0] - ld[1]
        print(ld, rd)
        print(lval, rval)

        
        if lval > rval:
            for p in prettyTuple:
                for y in p:
                    self.shape_2d[y[1]][1] = self.shape_2d[y[0]][1]
        else: #rval >= lval
            for p in prettyTuple:
                for y in p:
                    self.shape_2d[y[0]][1] = self.shape_2d[y[1]][1]


                    
        
        # X좌표 조정
        axis = self.shape_2d[143][0]
        for p in prettyTuple:
            for x in p:
                avg = ((axis - self.shape_2d[x[0]][0]) + (self.shape_2d[x[1]][0] - axis)) / 2
                self.shape_2d[x[0]][0] = axis - avg
                self.shape_2d[x[1]][0] = axis + avg          
        #for p in prettyAxis:
            #self.shape_2d[p][0] = axis
        


        
