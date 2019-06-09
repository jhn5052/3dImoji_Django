import glfw, pyrr, numpy
from OpenGL.GL import *
from PIL import Image
import pyscreenshot as ImageGrab

from .gl_ObjLoader import *
from .cv_ReadUserImage import *
from .cv_ConvertCoords3 import *
from .gl_ShaderLoader import *
from .cv_compose import *




def window_resize(window, width, height):
    glViewport(0, 0, width, height)

def main():
    
    # Set window
    if not glfw.init():
        return
    w_width, w_height = 800, 1000
    window = glfw.create_window(w_width, w_height, "My OpenGL window", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, window_resize)

    
    
    # Load Predictation(특징점) from User Image
    cv = CVloader("face.jpg")
    cv.PredictionExtract()
    cv.Prettify()
    
    # Load Sample Model(.obj) first_nice.obj  hoxi.obj
    obj = ObjLoader()
    obj.parse_model("static/realeye.obj") # Coords -> { Y Z X }

        #adjust coordinations
    converter = Converter(cv.shape_2d, obj.vert_coords)
    obj.vert_coords = converter.adjustEye()
    obj.vert_coords = converter.adjust_zx()
    obj.load_model()



    # To Buffer
    texture_offset = len(obj.vertex_index)*12
    normal_offset = (texture_offset + len(obj.texture_index)*8)
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, obj.model.itemsize * len(obj.model), obj.model, GL_STATIC_DRAW)
        # positions
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, obj.model.itemsize * 3, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
        # textures
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, obj.model.itemsize * 2, ctypes.c_void_p(texture_offset))
    glEnableVertexAttribArray(1)
        # normals
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, obj.model.itemsize * 3, ctypes.c_void_p(normal_offset))
    glEnableVertexAttribArray(2)


    
    # Texture Mapping
    texture = glGenTextures(1)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # Set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    # Load textureimage
    image = Image.open("static/modified2.jpg")#MJ_FINAL
    flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = image.convert("RGBA").tobytes()
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

      

    # Compile Shader
    shader = compile_shader("vertex.vs", "fragment.fs")
    glUseProgram(shader)
    glClearColor(1, 1, 1, 1.0)
    glEnable(GL_DEPTH_TEST)

    view = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, -3.0]))
    projection = pyrr.matrix44.create_perspective_projection_matrix(8.0, w_width / w_height, 0.1, 100.0)
    model = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, 0.0]))

    view_loc = glGetUniformLocation(shader, "view")
    proj_loc = glGetUniformLocation(shader, "projection")
    model_loc = glGetUniformLocation(shader, "model")
    transform_loc = glGetUniformLocation(shader, "transform")
    light_loc = glGetUniformLocation(shader, "light")

    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

    
    # Rendering Here

    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
           
    #0.8 * glfw.get_time() #4.75
    rot_x = pyrr.Matrix44.from_x_rotation(2.8 )#2.5
    rot_y = pyrr.Matrix44.from_y_rotation(4.75 )
    glUniformMatrix4fv(transform_loc, 1, GL_FALSE, rot_y)
    glUniformMatrix4fv(light_loc, 1, GL_FALSE, rot_x)

    glDrawArrays(GL_TRIANGLES, 0, len(obj.vertex_index))
    glfw.swap_buffers(window)
    
    glReadBuffer(GL_FRONT)
    pixels= glReadPixels(0,0,w_width,w_height,GL_RGB,GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGB",(w_width,w_height),pixels)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)

    filename ='FirstResult'
    image.save('static/First_output/'+filename+'.jpg')
    glfw.terminate()

    composer = Composer()
    composer.hair_clothes()
 
    
if __name__ == "__main__":
    main()
