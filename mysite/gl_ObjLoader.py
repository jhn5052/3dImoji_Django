import numpy as np



class ObjLoader:
    def __init__(self):
        self.vert_coords = []
        self.text_coords = []
        self.norm_coords = []

        self.vertex_index = []
        self.texture_index = []
        self.normal_index = []

        self.model = []

        self.flag = -1

    #Read Obj file and parsing
    def parse_model(self, file):
        for line in open(file, 'r',encoding='UTF8'):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue

            if values[0] == 'v':

                values[1] = float(values[1])
                values[2] = float(values[2])          
                values[3] = float(values[3])
                
                self.vert_coords.append(values[1:4])
                '''
                if float(values[1]) < -0.119 and float(values[1]) >-0.126:
                    if float(values[2]) >0.18 and float(values[2]) < 0.21:
                        if float(values[3]) >= -0.071404 and float(values[3]) <= -0.064529:
                            print(values)
                '''       
            if values[0] == 'vt':
                self.text_coords.append(values[1:3])
            if values[0] == 'vn':
                self.norm_coords.append(values[1:4])
            if values[0] == 'f':
                face_i = []
                text_i = []
                norm_i = []
                for v in values[1:4]:
                    w = v.split('/')

                    if '' in w:
                        w[1] = 1
                        
                    face_i.append(int(w[0])-1)
                    text_i.append(int(w[1])-1)
                    norm_i.append(int(w[2])-1)               
                self.vertex_index.append(face_i)
                self.texture_index.append(text_i)
                self.normal_index.append(norm_i)
                
        if len(self.text_coords)  > 0 :
            self.flag = 1


    #ready to draw model
    def load_model(self):
        self.vertex_index = [y for x in self.vertex_index for y in x]
        self.texture_index = [y for x in self.texture_index for y in x]
        self.normal_index = [y for x in self.normal_index for y in x]

        for i in self.vertex_index:
            self.model.extend(self.vert_coords[i])


        if self.flag == 1:
            for i in self.texture_index:
                self.model.extend(self.text_coords[i])

        for i in self.normal_index:
            self.model.extend(self.norm_coords[i])

        self.model = np.array(self.model, dtype='float32')
