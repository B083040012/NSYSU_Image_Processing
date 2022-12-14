import math, random
# from random import random
import numpy as np

def get_bilinear(img, posx, posy):
    level = list()
    p1=min(int(posx),img.shape[0]-1)
    q1=min(int(posy),img.shape[1]-1)
    mu = posx - p1
    lamb = posy - q1
    p2=min(p1+1,img.shape[0]-1)
    q2=min(q1+1,img.shape[1]-1)

    for z in range(img.shape[2]):
        leftUp=img[p1, q1, z]
        leftDown=img[p2, q1, z]
        rightUp=img[p1, q2, z]
        rightDown=img[p2, q2, z]

        value1=mu*rightDown+(1-mu)*leftUp
        value2=mu*rightUp+(1-mu)*leftDown

        level.append(lamb*value1+(1-lamb)*value2)
    level = np.array(level)

    return level

class PcxImage():
    def __init__(self):
        self.mod_image = None
        self.mod_width = None
        self.mod_height = None

        # self.enlarged_image = None
        self.enlarged_time = None
        # self.rotate_image = None
        self.rotate_angle = None

    def initial_mod_image(self, type):
        if type == "gray":
            self.mod_image = np.copy(self.gray_image)
            self.mod_width = self.gray_image.shape[0]
            self.mod_height = self.gray_image.shape[1]
        elif type == "general" or self.mod_image is None:
            self.mod_image = np.copy(self.ori_image)
            self.mod_width = self.width
            self.mod_height = self.height
        # if self.mod_image is None:
        #     if type == "general":
        #         self.mod_image = np.copy(self.ori_image)
        #         self.mod_width = self.width
        #         self.mod_height  =self.height
        #     elif type == "rotate":
        #         self.mod_image = np.copy(self.ori_image) if self.enlarged_image is None else np.copy(self.enlarged_image)
        #         self.mod_width = self.enlarged_width if self.enlarged_image is None else self.width
        #         self.mod_height = self.enlarged_height if self.enlarged_image is None else self.height
        #     elif type == "enlarge":
        #         self.mod_image = np.copy(self.ori_image) if self.rotate_image is None else np.copy(self.rotate_image)
        #         self.mod_width = self.rotate_width if self.rotate_image is None else self.width
        #         self.mod_height = self.rotate_height if self.rotate_image is None else self.height

    def read_from_filename(self, filename):
        try:
            with open(filename, mode = 'rb') as pcx_file:
                content = pcx_file.read()
        except:
            return -1

        self.header = {"manufacturer": content[0], "version": content[1], "encoding": content[2], "bits per pixel": content[3], 
                       "window": content[4:12], "hdpi":  int.from_bytes(content[12:14], byteorder="little"),
                       "vdpi": int.from_bytes(content[14:16], byteorder="little"), "colormap": content[16:64], "reversed": content[64], 
                       "nplanes": content[65], "bytes per line": int.from_bytes(content[66:68], byteorder="little"),
                       "palette info": int.from_bytes(content[68:70], byteorder="little"), "hscreen size": int.from_bytes(content[70:72], byteorder="little"),
                       "vscreen size": int.from_bytes(content[72:74], byteorder="little"), "filter": content[75:128]}

        # extract the color palette
        self.color_pal = None
        if self.header["version"] == 5:
            # 256-color palettes, seek to the end of file and  count back 796 bytes
            self.color_pal = list()
            pal_content = content[-768:]
            for i in range(256):
                # append the rgb value into color_pal
                rgb_list = list()
                rgb_list.append(pal_content[i * 3])
                rgb_list.append(pal_content[i * 3 + 1])
                rgb_list.append(pal_content[i * 3 + 2])
                self.color_pal.append(rgb_list)
        
        # extract the pixel content
        self.pixel_content = None
        if self.header["nplanes"] == 1:
            self.pixel_content = content[128:-769]
        elif self.header["nplanes"] == 3:
            # still not sure about this
            # try the sample.pcx for correctness
            self.pixel_content = content[128:]
    
    def decode_image(self):
        xmin, ymin, xmax, ymax = (int.from_bytes(self.header["window"][0:2], byteorder="little"), 
                                  int.from_bytes(self.header["window"][2:4], byteorder="little"),
                                  int.from_bytes(self.header["window"][4:6], byteorder="little"), 
                                  int.from_bytes(self.header["window"][6:8], byteorder="little"))
        self.width = xmax - xmin + 1
        self.height = ymax - ymin + 1
        self.r_map, self.g_map, self.b_map = (list() for i in range(3))
        index = 0

        if self.header["nplanes"] == 1:
            while index < len(self.pixel_content):
                byte_tmp = self.pixel_content[index]
                dup_time = 1
                if byte_tmp > 192:
                    # 2 high bits are set
                    dup_time = int(byte_tmp) - 192
                    index += 1
                color_index = self.pixel_content[index]
                index += 1
                
                # insert the gray scale value into map
                for times in range(dup_time):
                    self.r_map.append(self.color_pal[color_index][0])
                    self.g_map.append(self.color_pal[color_index][1])
                    self.b_map.append(self.color_pal[color_index][2])
        elif self.header["nplanes"] == 3:
            rgb = 0
            add_byte = 0
            while index < len(self.pixel_content):
                byte_tmp = self.pixel_content[index]
                dup_time = 1
                if byte_tmp > 192:
                    # 2 high bits are set
                    dup_time = int(byte_tmp) - 192
                    index += 1
                color = self.pixel_content[index]
                index += 1
                
                # insert the gray scale value into map
                for times in range(dup_time):
                    if rgb == 0:
                        self.r_map.append(color)
                    elif rgb == 1:
                        self.g_map.append(color)
                    elif rgb == 2:
                        self.b_map.append(color)
                    add_byte += 1
                    if add_byte >= self.width:
                        add_byte = 0
                        rgb = (rgb + 1)%3
        self.r_map = np.array(self.r_map)
        self.g_map = np.array(self.g_map)
        self.b_map = np.array(self.b_map)

        # build the original image from rgb map
        self.ori_image = list()
        for x in range(self.width):
            for y in range(self.height):
                rgb_value = list()
                index = x * self.width + y
                rgb_value.append(self.r_map[index])
                rgb_value.append(self.g_map[index])
                rgb_value.append(self.b_map[index])
                self.ori_image.append(rgb_value)
        self.ori_image = np.resize(self.ori_image, (self.width, self.height, 3))
        self.gray_image = self.color_gray_convert(self.ori_image)

    def color_gray_convert(self, color_img):
        newShape=list(map(int,[color_img.shape[0], color_img.shape[1], 1]))
        gray_image = np.zeros(newShape,dtype=np.uint8)
        for x in range(0, gray_image.shape[0]):
            for y in range(0, gray_image.shape[1]):
                gray_scale = (color_img[x, y, 0] + color_img[x, y, 1] + color_img[x, y, 2]) / 3
                gray_image[x, y] = (gray_scale)
        return gray_image

    def color_pal_image(self):
        # color palette content
        # pixel_size: the pixel of one color = pixel_size * pixel_size
        # color_num: the total num of pcx color from palette
        pixel_size = 6
        color_num = 16
        newShape=list(map(int,[pixel_size * color_num, pixel_size * color_num, 3]))
        pal_image = np.zeros(newShape,dtype=np.uint8)
        xindex = 0; yindex = 0
        for item in self.color_pal:
            for x in range(pixel_size):
                for y in range(pixel_size):
                    pal_image[xindex + x][yindex + y] = item
            yindex+=pixel_size
            if(yindex > (pixel_size * color_num - pixel_size)):
                yindex = yindex%(pixel_size * color_num)
                xindex = (xindex + pixel_size)%(pixel_size * color_num)
        return pal_image, pixel_size * color_num, pixel_size * color_num

    def rgb_value_pos(self, posx, posy):
        try:
            r = self.ori_image[posx][posy][0]
            g = self.ori_image[posx][posy][1]
            b = self.ori_image[posx][posy][2]
            return r, g, b
        except:
            return -1, -1, -1

    def mod_pixel(self, posx, posy, r, g, b):
        self.initial_mod_image("general")
        if r > 255 or g > 255 or b > 255 or r < 0 or g < 0 or b < 0:
            print("invalid rgb value")
            return self.ori_image, self.width, self.height
        # print("valid rgb: {0}, {1}, {2}".format(r, g, b))
        self.mod_image[posy][posx][0] = r
        self.mod_image[posy][posx][1] = g
        self.mod_image[posy][posx][2] = b

        return self.mod_image, self.mod_width, self.mod_height

    def rgb_channel(self, type):
        width, height = self.width, self.height
        newShape = list(map(int, [width, height, 3]))
        channel_img = np.zeros(newShape, dtype = np.uint8) 
        if type == "red":
            channel_img[:, :, 0] = self.ori_image[:, :, 0]
        elif type == "green":
            channel_img[:, :, 1] = self.ori_image[:, :, 1]
        elif type == "blue":
            channel_img[:, :, 2] = self.ori_image[:, :, 2]
        
        return channel_img, width, height

    def enlarge(self, type, times):
        
        """
        Two enlarge method: 
            1. simple_dup
            2. bi_linear
        """
        self.initial_mod_image("enlarge")
        times = 2**times
        # adjust the enlarged times if repeated enlarged and rotate
        # tmp = times
        # times = times if self.enlarged_time is None else times/self.enlarged_time
        # self.enlarged_time = tmp

        self.enlarged_width = int(self.mod_width * times)
        self.enlarged_height = int(self.mod_height * times)
        newShape = list(map(int,[self.enlarged_width, self.enlarged_height, 3]))
        self.enlarged_image = np.zeros(newShape,dtype=np.uint8)
            
        if type == "simple_dup":
            if times >= 1:
                for xindex in range(0, self.mod_width - times + 1):
                    large_x = xindex * times
                    for yindex in range(0, self.mod_height - times + 1):
                        large_y = yindex * times
                        self.enlarged_image[large_x : (large_x + times), large_y : (large_y + times)] = self.mod_image[xindex][yindex]
            elif times < 1:
                ratio = int(1/times)
                for xindex in range(0, self.enlarged_width):
                    large_x = int(xindex * ratio)
                    for yindex in range(0, self.enlarged_height):
                        large_y = int(yindex * ratio)
                        self.enlarged_image[xindex, yindex] = self.mod_image[large_x, large_y]
        elif type == "bi_linear":
            ratio = 1/times
            for x in range(self.enlarged_width):
                for y in range(self.enlarged_height):
                    orix = x * ratio
                    oriy = y * ratio
                    self.enlarged_image[x, y, :] = get_bilinear(self.mod_image, orix, oriy)
        
        return self.enlarged_image, self.enlarged_width, self.enlarged_height

    def rotate(self, type, theta):
        
        """
        Two rotate method
            1. nromal rotation: ori_img corrdinate--> new_img coordinate
            2. reverse rotation: new_img coordinate--> ori_img coordinate
        """
        self.initial_mod_image("rotate")
        # adjust theta if repeated enlarged and rotate
        # tmp = theta
        # theta = theta if self.rotate_angle is None else theta - self.rotate_angle
        # self.rotate_angle = tmp

        degree = math.radians(theta)
        degree = -(degree) if type == "reverse" else degree
        self.rotate_width, self.rotate_height = abs(self.mod_width*math.cos(degree)) + abs(self.mod_height*math.sin(degree)), \
                                                abs(self.mod_height*math.sin(degree)) + abs(self.mod_width*math.cos(degree))
        newShape=list(map(int,[self.rotate_width + 1, self.rotate_height + 1, 3]))
        self.rotate_image = np.full(newShape, 255)

        # rotate according to the center: matrix1 * matrix_2 * matrix_3
        if type == "normal":
            # matrix_1 = np.array([[1, 0, 0], [0, -1, 0], [-(self.mod_width / 2), self.mod_height / 2, 1]])
            matrix_1 = np.array([[1, 0, int(self.mod_width / 2)], [0, 1, int(self.mod_height / 2)], [0, 0, 1]])
            # matrix_3 = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])
            matrix_3 = np.array([[1, 0, -int(self.mod_width / 2)], [0, 1, -int(self.mod_height / 2)], [0, 0, 1]])
        elif type == "reverse":
            # matrix_1 = np.array([[1, 0, 0], [0, -1, 0], [-(self.rotate_width / 2), self.rotate_height / 2, 1]])
            matrix_1 = np.array([[1, 0, int(self.rotate_width / 2)], [0, 1, int(self.rotate_height / 2)], [0, 0, 1]])
            # matrix_3 = np.array([[1, 0, 0], [0, -1, 0], [-int((self.rotate_width - self.mod_width) / 2), -int((self.rotate_height - self.mod_height) / 2), 1]])
            matrix_3 = np.array([[1, 0, -int(self.rotate_width / 2)], [0, 1, -int(self.rotate_height / 2)], [0, 0, 1]])
        matrix_2 = np.array([[math.cos(degree), -(math.sin(degree)), 0], [math.sin(degree), math.cos(degree), 0], [0, 0, 1]])
        rotate_matrix = np.matmul(matrix_1, matrix_2)
        rotate_matrix = np.matmul(rotate_matrix, matrix_3)

        # rotate by different method
        if type == "normal":
            # find the negative corrdinate that outsude the frame (used to adjust the rotated image)
            edge_list = [np.array([0, 0, 1]), np.array([self.mod_width, 0, 1]), np.array([0, self.mod_height, 1]), np.array([self.mod_width, self.mod_height, 1])]
            x_fix = 0; y_fix = 0
            for edge_tmp in edge_list:
                tmp_cor = np.matmul(rotate_matrix, edge_tmp)
                x_fix = tmp_cor[0] if x_fix > tmp_cor[0] else x_fix
                y_fix = tmp_cor[1] if y_fix > tmp_cor[1] else y_fix

            for x in range(self.mod_image.shape[0]):
                for y in range(self.mod_image.shape[1]):
                    cor = np.array([x, y, 1])
                    new_cor = np.matmul(rotate_matrix, cor)
                    self.rotate_image[int(new_cor[0] + abs(x_fix)), int(new_cor[1] + abs(y_fix))] = self.mod_image[x, y]
        elif type == "reverse":
            x_fix = int((self.rotate_width - self.mod_width) / 2)
            y_fix = int((self.rotate_height - self.mod_height) / 2)

            for x in range(self.rotate_image.shape[0]):
                for y in range(self.rotate_image.shape[1]):
                    cor = np.array([x, y, 1])
                    ori_cor = np.matmul(rotate_matrix, cor)
                    ori_x = int(ori_cor[0] - abs(x_fix)); ori_y = int(ori_cor[1] - abs(y_fix))
                    if ori_x < 0 or ori_x >=self.mod_width or ori_y < 0 or ori_y >=  self.mod_height:
                        continue
                    self.rotate_image[x, y] = self.mod_image[ori_x, ori_y]
        # self.mod_image = np.copy(self.rotate_image)
        # self.mod_width = self.rotate_width
        # self.mod_height = self.rotate_height
        return self.rotate_image, self.rotate_width, self.rotate_height

    def shear_cal(self, angle, x, y):

        tangent=math.tan(angle/2)
        new_x=round(x-y*tangent)
        new_y=y
        
        return new_y,new_x

    def shear(self, angle):
        self.initial_mod_image("general")
        angle=math.radians(angle)                           
        cosine=math.cos(angle)
        sine=math.sin(angle)

        height=self.mod_image.shape[0]
        width=self.mod_image.shape[1]

        new_height  = round(abs(height*cosine)+abs(width*sine))+1
        new_width  = round(abs(width*cosine)+abs(height*sine))+1

        output=np.zeros((new_height,new_width,3))

        original_centre_height   = round(((height+1)/2)-1)
        original_centre_width    = round(((width+1)/2)-1)

        new_centre_height= round(((new_height+1)/2)-1)
        new_centre_width= round(((new_width+1)/2)-1)


        for i in range(height):
            for j in range(width):
                y=height-1-i-original_centre_height                   
                x=width-1-j-original_centre_width 

                new_y,new_x=self.shear_cal(angle,x,y)

                new_y=new_centre_height-new_y
                new_x=new_centre_width-new_x
                
                output[new_y,new_x,:]=self.ori_image[i,j,:]

        return output, width, height

    # def shear(self, slope):

    #     """
    #     Shear the image
    #     """
    #     self.initial_mod_image("general")
    #     height = self.mod_height + slope*self.mod_width + 0.5
    #     width = self.mod_width
    #     newShape = list(map(int, [abs(height), abs(width), 3]))
    #     shear_image = np.full(newShape, 255)
    #     for x in range(self.mod_height):
    #         for y in range(self.mod_width):
    #             new_x, new_y = (x + slope*y + 0.5), y
    #             shear_image[int(abs(new_x)), int(abs(new_y)), :] = self.ori_image[x, y, :]
    #     return shear_image, width, height

    def cut(self, type, cor1, cor2):

        """
        2 method to cut the image
            1. cut by selecting a rect
                cor1: leftup cor, cor2: rightdown cor
            2. cut by selecting a circle
                cor1: centroid cor, cor2: radius
        """
        self.initial_mod_image("general")
        width = self.mod_width
        height = self.mod_height
        newShape = list(map(int, [width, height, 3]))
        cut_image = np.full(newShape, 255)

        # starting cut process
        if type == "rect":
            sx = min(cor1.x(), cor2.x()); ex = max(cor1.x(), cor2.x()); 
            sy = min(cor1.y(), cor2.y()); ey = max(cor1.y(), cor2.y())
            for x in range(sx, ex):
                for y in range(sy, ey):
                    cut_image[y][x] = self.mod_image[y][x]
        elif type == "circle":
            for x in range(int(cor1.x() - cor2), int(cor1.x() + cor2)):
                for y in range(int(cor1.y() - cor2), int(cor1.y() + cor2)):
                    if x < 0 or y < 0 or x > width or y > height: continue
                    if np.linalg.norm(np.array([x, y])-np.array([cor1.x(), cor1.y()])) < cor2:
                        cut_image[y][x] = self.mod_image[y][x]
        return cut_image, width, height

    def magic_wand(self, magic_wand_img, begin, end, current):

        """
        Magic Wand Function From PhotoShop
            * copy the [original content of coordinate] to 
              [the magic wand image coordinate <--> begin with same distance as current <--> end]
            * the original content must from self.ori_img
        """
        thick = 5
        x_fix = current.x() - end.x(); y_fix = current.y() - end.y()
        accord_corx, accord_cory = begin.x() + x_fix, begin.y() + y_fix

        for tx in range(-thick, thick):
            for ty in range(-thick, thick):
                tmpx, tmpy = accord_corx + tx, accord_cory + ty
                orix, oriy = current.x() + tx, current.y() + ty
                if tmpx < 0 or tmpx >= self.width or tmpy < 0 or tmpy >= self.height or\
                    orix < 0 or orix >= self.width or oriy < 0 or oriy >= self.height:
                    pass
                else:
                    magic_wand_img[tmpy][tmpx] = self.ori_image[oriy][orix]
        return magic_wand_img

    def alpha(self, alpha_img, alpha_width, alpha_height, alpha_value):

        """
        Cover mod_image and alpha_img according to the alpha value
        """
        self.initial_mod_image("general")
        width = max(alpha_width, self.mod_width)
        height = max(alpha_height, self.mod_height)
        newShape = list(map(int, [width, height, 3]))
        alpha_image = np.zeros(newShape, dtype = np.uint8)
        for x in range(alpha_image.shape[0]):
            for y in range(alpha_image.shape[1]):
                if x >= self.mod_width or y >= self.mod_height:
                    alpha_image[x][y] = alpha_img[x][y]
                elif x >= alpha_width or y >= alpha_height:
                    alpha_image[x][y] = self.mod_image[x][y]
                else:
                    alpha_image[x][y] = alpha_img[x][y] * (1 - alpha_value) + self.mod_image[x][y] * alpha_value
        return alpha_image, width, height

    def ball(self, type, center = None, vector = None, speed = None):

        """
        2 types of ball function
            1. create: produce the ball image: 256 * 256 with ball at center (radius = 10)
            2. bouncing: produce the next ball image according to the physics factor
        """
        radius = 10
        width = 256; height = 256
        newShape = list(map(int, [width, height, 3]))
        if type == "create":
            center = np.array([int(width / 2), int(height / 2)])
            vector = np.array([1, 0.5])
            ball_image = np.zeros(newShape, dtype = np.uint8)
            for x in range(int(center[0] - radius), int(center[0] + radius)):
                for y in range(int(center[1] - radius), int(center[1] + radius)):
                    if x < 0 or y < 0 or x >= width or y >= height:
                        continue
                    if np.linalg.norm(np.array([x, y])-center) < radius:
                            ball_image[y, x, :] = [255, 255, 255]
        elif type == "bouncing":
            ball_image = np.zeros(newShape, dtype = np.uint8)
            center = np.array([int(center[0] + vector[0] * speed), int(center[1] + vector[1] * speed)])
            if center[0] - radius < 0:
                n_vec = np.array([1, 0])
            elif center[0] + radius >= width:
                n_vec = np.array([-1, 0])
            elif center[1] - radius < 0:
                n_vec = np.array([0, 1])
            elif center[1] + radius >= width:
                n_vec = np.array([0, -1])
            else: 
                n_vec = np.array([0, 0])
                for x in range(int(center[0] - radius), int(center[0] + radius)):
                    for y in range(int(center[1] - radius), int(center[1] + radius)):
                        if np.linalg.norm(np.array([x, y])-center) < radius:
                            ball_image[y, x, :] = [255, 255, 255]
            new_vector = vector - 2 * np.dot(n_vec, vector) * n_vec
            vector = new_vector
        return ball_image, width, height, center, vector

    def misaligned(self, offset):
        
        """
        Move the green plane and blue plane vertically depending on the offset
        """
        self.initial_mod_image("general")
        width = self.mod_width
        height = self.mod_height
        newShape = list(map(int, [width, height, 3]))
        misaligned_image = np.zeros(newShape, dtype = np.uint8)
        for x in range(0, misaligned_image.shape[0]):
            misaligned_image[x, :, 0] = self.mod_image[x, :, 0]
            if (x + offset) < self.mod_image.shape[0]:
                misaligned_image[x, :, 1] = self.mod_image[(x + offset), :, 1]
            if (x + 2 * offset) < self.mod_image.shape[0]:
                misaligned_image[x, :, 2] = self.mod_image[(x + 2 * offset), :, 2]

        return misaligned_image, width, height

    def dithering(self, depth):

        """
        Presenting gray level by dithering
            * enhance depth by reducing resolution (1 pixel --> 4 pixel)
        """
        times = 2
        width = self.gray_image.shape[0] * 2
        height = self.gray_image.shape[1] * 2
        newShape = list(map(int, [width, height, 1]))
        dithering_image = np.zeros(newShape, dtype = np.uint8)
        for x in range(self.gray_image.shape[0]):
            for y in range(self.gray_image.shape[1]):
                level = int((self.gray_image[x, y, 0] / 255) * (depth - 1))
                # print("level = {0}".format(level))
                # choice_list = [[times * x, times * y], [times * x + 1, times * y], \
                #                [times * x, times * y + 1], [times * x + 1, times * y + 1]]
                choice_list = [i for i in range(times * times)]
                mod_index = np.random.choice(choice_list, level + 1)
                for i in range(level):
                    if mod_index[i] == 0: dithering_image[times * x, times * y] = 255
                    elif mod_index[i] == 1: dithering_image[times * x + 1, times * y] = 255
                    elif mod_index[i] == 2: dithering_image[times * x, times * y + 1] = 255
                    elif mod_index[i] == 3: dithering_image[times * x + 1, times * y + 1] = 255
        return dithering_image, width, height

    def negative(self):
        
        """
        Negative the gray scale of input image
        """
        self.initial_mod_image("general")
        width = self.mod_image.shape[0]
        height = self.mod_image.shape[1]
        newShape = list(map(int, [width, height, 3]))
        negative_image = np.zeros(newShape, dtype = np.uint8)
        for x in range(negative_image.shape[0]):
            for y in range(negative_image.shape[1]):
                negative_image[x, y, :] = 255 - self.mod_image[x, y, :]
        return negative_image, width, height

    def mirror(self, type):

        """
        4 types of mirror image (depending on different symmetry axis)
            1. vertical
            2. horizontal
            3. 45 degree
            4. 135 degree
        """
        self.initial_mod_image("general")
        width = self.mod_width
        height = self.mod_height
        newShape = list(map(int, [width, height, 3]))
        mirror_image = np.zeros(newShape, dtype = np.int8)
        if type == "vertical":
            axis_value = int(width / 2)
            for x in range(width):
                dist = axis_value - x
                mirror_image[:,(dist + axis_value) - 1] = self.mod_image[:,x]
        elif type == "horizontal":
            axis_value = int(height / 2)
            for y in range(height):
                dist = axis_value - y
                mirror_image[(dist+ axis_value) - 1] = self.mod_image[y]
        elif type == "45":
            for x in range(width):
                for y in range(height):
                    mirror_image[x, y] = self.mod_image[abs(width - 1 - y), abs(height - 1 - x)]
        elif type == "135":
            for x in range(width):
                for y in range(height):
                    mirror_image[x, y] = self.mod_image[y, x]
        return mirror_image, width, height

    def custom_threshold(self, threshold_value):
        
        """
        Generate the corresponding image from the given threshold_value
        """
        self.initial_mod_image("gray")
        width = self.mod_width
        height = self.mod_height
        newShape = list(map(int, [width, height, 1]))
        th_image = np.zeros(newShape, dtype = np.int8)

        for x in range(width):
            for y in range(height):
                th_image[x, y] = 255 if self.mod_image[x, y] > threshold_value else 0
        return th_image, width, height

    def local_threshold(self, type, kernel_size, C):

        """
        3 types of local threshold
            1. mean of neighborhood
            2. median of neighborhood
            3. mean of the minimum and maximum of neighborhood
        * kernel_size: the size of neighbor pixels that have to examine
        * C: the offset of threshold value and center pixel value
        * details:
            for each pixel, the algorithm will calculate (with different types) the threshold 
            with its neighbors in the kernel, if the gray scale level exceed the threshold with C, 
            turn the pixel into black level (0), otherwise preserve its gray level
        """
        self.initial_mod_image("gray")
        width = self.mod_width
        height = self.mod_height
        newShape = list(map(int, [width, height, 1]))
        lt_image = np.zeros(newShape, dtype = np.int8)
        for x in range(width):
            for y in range(height):
                tmp_list = list()
                for kx in range(-int((kernel_size - 1) / 2), int((kernel_size - 1) / 2) + 1):
                    for ky in range(-int((kernel_size - 1) / 2), int((kernel_size - 1) / 2) + 1):
                        if x + kx < 0 or x + kx >= width: continue
                        if y + ky < 0 or y + ky >= height: continue
                        if kx == 0 and ky == 0: continue
                        tmp_list.append(self.mod_image[(x + kx), (y + ky)])
                tmp_list = np.array(tmp_list)
                if type == "mean":
                    t_value = np.mean(tmp_list)
                elif type == "median":
                    t_value = np.median(tmp_list)
                elif type == "min_max_mean":
                    t_value = (tmp_list.max() + tmp_list.min()) / 2
                else:print("undefined type")
                if (self.mod_image[x, y] - t_value) > C:
                    lt_image[x, y] = 255
                else:
                    lt_image[x, y] = 0
        return lt_image, width, height

    def otsu_threshold(self):

        """
        Steps of otsu thresholding:
            1. summarize the times of each gray level occur in the image
            2. calculate the probability of each gray level occur in the whole image (/sum)
            3. search all the threshold candidates from 0 to 255, find the threshold with the largeset variances
            * equation from wiki: b(t) = q1(t) * q2(t) * [u1(t) - u2(t)]^2
        """
        self.initial_mod_image("gray")
        width = self.mod_width
        height = self.mod_height
        scale_sum = np.zeros((256, ), dtype = np.uint)
        scale_prob = np.zeros((256, ), dtype = float)
        for x in range(width):
            for y in range(height):
                scale_sum[self.mod_image[x, y]] += 1
        for i in range(len(scale_sum)):
            scale_prob[i] = scale_sum[i] / (width * height)
        weight_sum  = 0
        for i in range(0, 256):
            weight_sum += i * scale_prob[i]
        
        # initialize q1, q2, u1, u2
        q1 = scale_prob[0]
        sum1 = 0; sum2 = 0
        max_t = 0; target_t = 0
        # search all threshold t
        for t in range(1, 256):
            q1 += scale_prob[t]; q2 = 1 - q1
            sum1 += t * scale_prob[t]
            u1 = sum1 / q1
            u2 = (weight_sum - sum1) / q2
            # equation from the wiki
            b = q1 * q2 * pow((u1 - u2), 2)
            if b >= max_t:
                target_t = t
                max_t = b
        return target_t

    def binary_to_gray_code(self, bit_string):
        # MSB of binary = MSB of gray code
        gray_code_string = bit_string[0]
        for i in range(1, 8):
            # gray_code[i] = binary[i] xor binary[i + 1]
            gray_code_string += str(int(bit_string[i] != bit_string[i - 1]))
        return gray_code_string

    def gray_to_decimal(self, gray_code_string):
        binary_code_string = gray_code_string[0]
        ans = int(binary_code_string) * pow(2, 7)
        for i in range(1, 8):
            binary_code_string += str(int(binary_code_string[i - 1] != gray_code_string[i]))
            ans += int( binary_code_string[i]) * pow(2, (7 - i))
        return ans

    def bit_plane(self, type):

        """
        2 types of bit plane slicing
            1. 8-bit slicing
            2. gray code slicing
        """
        self.initial_mod_image("gray")
        width = self.mod_width
        height = self.mod_height
        result_img_list = list()
        if type == "binary":
            slicing_list = list()
            for x in range(width):
                for y in range(height):
                    # print("mod_image: {0}".format(int(self.mod_image[x, y])))
                    bit_string = np.binary_repr(int(self.mod_image[x, y]), width = 8)
                    # print("bit_string: {0}".format(bit_string))
                    slicing_list.append(bit_string)
        elif type == "gray_code":
            slicing_list = list()
            for x in range(width):
                for y in range(height):
                    bit_string = np.binary_repr(int(self.mod_image[x, y]), width = 8)
                    bit_string = self.binary_to_gray_code(bit_string)
                    slicing_list.append(bit_string)
        for i in range(0, 8):
            tmp_img = np.array([int(pixel[(7 - i)]) for pixel in slicing_list], dtype = np.uint8)
            tmp_img = tmp_img.reshape(width, height, 1)
            result_img_list.append(tmp_img)

        return result_img_list

    def merge_bit_plane(self, type, img_list):
        
        """
        2 types of bit plane
            1. 8-bit bit plane
            2. gray code bit plane
        num: the bit plane index that have to be changed
        img_list: image of every bit plane
        """
        width = len(img_list[0])
        height = len(img_list[0][0])
        newShape = list(map(int, [width, height, 1]))
        merged_image = np.zeros(newShape, dtype = np.uint8)
        if type == "binary":
            for p in range(8):
                merged_image += pow(2, p) * img_list[p]
        elif type == "gray_code":
            for x in range(width):
                for y in range(height):
                    gray_code = ""
                    for p in range(0, 8):
                        gray_code += str(int(img_list[(7 - p)][x][y]))
                        # print(gray_code)
                    merged_image[x, y] = self.gray_to_decimal(gray_code)
        return merged_image, width, height

    def cal_snr(self, merge_image):

        """
        Comparing the differenc of gray_image and mod_image
            by calculating SNR value
        """
        snr_value = 0
        width = self.gray_image.shape[0]
        height = self.gray_image.shape[1]
        ori_squre_sum = 0
        diff_square_sum = 0
        for x in range(width):
            for y in range(height):
                ori_squre_sum += pow(self.gray_image[x, y, 0], 2)
                diff_square_sum += pow((int(self.gray_image[x, y, 0]) - int(merge_image[x, y, 0])), 2)
        snr_value = 10 * math.log((ori_squre_sum / diff_square_sum), 10)
        return snr_value

    def contrast_stretching(self, type, r1 = None, s1 = None, r2 = None, s2 = None):
        
        """
        2 types of contrast stretching
            1. simple linear: stretch gray scale to 0-255
            2. piecewise linear: stretch gray scale depend on (r1, s1), (r2, s2)
        """
        self.initial_mod_image("gray")
        width = self.mod_width
        height = self.mod_height
        newShape = list(map(int, [width, height, 1]))
        cs_image = np.zeros(newShape, dtype = np.uint8)
        if type == "simple_linear":
            ori_min = self.mod_image.min()
            ori_max = self.mod_image.max()
            min = 0; max = 255
            cs_image = ((self.mod_image - ori_min) / (ori_max - ori_min)) * max + \
                (1 - ((self.mod_image - ori_min) / (ori_max - ori_min))) * min
        elif type == "piecewise_linear":
            mask = [(self.mod_image <= r1), np.logical_and((r1 < self.mod_image), (self.mod_image <= r2)), (r2 < self.mod_image)]
            ori_min_max_list = [[0, r1], [r1, r2], [r2, 255]]
            new_min_max_list = [[0, s1], [s1, s2], [s2, 255]]
            for i in range(0, 3):
                ori_min, ori_max = ori_min_max_list[i][0], ori_min_max_list[i][1]
                min, max = new_min_max_list[i][0], new_min_max_list[i][1]
                cs_image[mask[i]] = ((self.mod_image[mask[i]] - ori_min) / (ori_max - ori_min)) * max + \
                    (1 - ((self.mod_image[mask[i]] - ori_min) / (ori_max - ori_min))) * min
        return cs_image, width, height

    def gray_level_slicing(self, type, r1, r2, mod_level):

        """
        2 types of gray level slicing
            1. diminish: modify the gray level b/w r1 and r2 to mod_level, set the rest to 0
            2. preserve: modify the gray level b/w r1 and r2 to mod_level, set the rest unchanged
        """
        self.initial_mod_image("gray")
        width = self.mod_width
        height = self.mod_height
        if type == "diminish_gls":
            newShape = list(map(int, [width, height, 1]))
            gls_image = np.zeros(newShape, dtype = np.uint8)
        elif type == "preserve_gls":
            gls_image = np.copy(self.mod_image)
        mask = (self.mod_image > r1) & (self.mod_image < r2)
        gls_image[mask] = mod_level

        return gls_image, width, height

    def noise(self, input_image):

        """
        Create noise image with pepper and salt method based on input_image
        """
        width, height = input_image.shape[0], input_image.shape[1]
        noise_ratio = 0.05
        choose_num = int(width * height * noise_ratio)
        noise_list = [0, 255]

        x_index_list = np.random.choice(255, choose_num)
        y_index_list = np.random.choice(255, choose_num)

        for ch in range(0, choose_num):
            x, y = x_index_list[ch], y_index_list[ch]
            input_image[x][y] = random.sample(noise_list, 1)

        return input_image, width, height

    def outlier(self, input_image, filter_size, threshold):

        """
        Compared to the average of its neighbors, 
        the number of neighbors depends on the filter_size
            * circle padding is adopted
        """
        mod_img = np.copy(input_image)
        width = mod_img.shape[0]
        height = mod_img.shape[1]
        fix = int((filter_size - 1) / 2)
        for x in range(width):
            for y in range(height):
                xmin = (x - fix) if (x - fix) >= 0 else 0
                ymin = (y - fix) if (y - fix) >= 0 else 0
                xmax = (x + fix + 1) if (x + fix + 1) <= width else width
                ymax = (y + fix + 1) if (y + fix + 1) <= height else height
                sum = mod_img[xmin : xmax, ymin : ymax].sum()
                mean = sum / (filter_size * filter_size)
                # print("mean: {0}".format(mean))
                if mod_img[x][y] -  mean > threshold: mod_img[x][y] = int(mean)

        return mod_img, width, height

    def median(self, input_image, filter_size, filter_shape):

        """
        filter_shape: 1 for square, 2 for cross
        """
        
        width = input_image.shape[0]
        height = input_image.shape[1]
        newShape = list(map(int, [width, height, 1]))
        mod_img = np.zeros(newShape, dtype = np.uint8)
        fix = int((filter_size - 1) / 2)
        for x in range(width):
            for y in range(height):
                xmin = (x - fix) if(x - fix) >= 0 else 0
                ymin = (y - fix) if (y - fix) >= 0 else 0
                xmax = (x + fix + 1) if (x + fix + 1) <= width else width
                ymax = (y + fix + 1) if (y + fix + 1) <= height else height
                if filter_shape == 1:
                    tmp_list = input_image[xmin : xmax, ymin : ymax].flatten()
                    while len(tmp_list) < filter_size * filter_size:
                        tmp_list = np.append(tmp_list, 0)
                    median = np.median(tmp_list)
                elif filter_shape == 2:
                    tmp_list = input_image[xmin : xmax, y].flatten()
                    tmp_list = np.delete(tmp_list, np.where(input_image[x][y]))
                    tmp_list2 = input_image[x, ymin : ymax].flatten()
                    for ele in tmp_list2:
                        tmp_list = np.append(tmp_list, ele)
                    while len(tmp_list) < filter_size * 2 - 1:
                        tmp_list = np.append(tmp_list, 0)
                    median = np.median(tmp_list)
                mod_img[x][y] = median

        return mod_img, width, height

    def maxmin(self, input):
        flat = input.flatten()
        l = len(flat)
        m = int((l + 1) / 2)
        min_list = list()
        for i in range(1, (l - m + 2)):
            tmp = flat[i:(i + m - 1)].min()
            min_list.append(tmp)
        min_list = np.array(min_list)

        return min_list.max()

    def minmax(self, input):
        flat = input.flatten()
        l = len(flat)
        m = int((l + 1) / 2)
        max_list = list()
        for i in range(1, (l - m + 2)):
            tmp = flat[i:(i + m - 1)].max()
            max_list.append(tmp)
        max_list = np.array(max_list)

        return max_list.min()

    def pmed(self, input_image, filter_size):

        width = input_image.shape[0]
        height = input_image.shape[1]
        newShape = list(map(int, [width, height, 1]))
        mod_img = np.zeros(newShape, dtype = np.uint8)
        fix = int((filter_size - 1) / 2)
        for x in range(width):
            for y in range(height):
                xmin = (x - fix) if(x - fix) >= 0 else 0
                ymin = (y - fix) if (y - fix) >= 0 else 0
                xmax = (x + fix + 1) if (x + fix + 1) <= width else width
                ymax = (y + fix + 1) if (y + fix + 1) <= height else height
                maxmin = self.maxmin(input_image[xmin : xmax, ymin : ymax])
                minmax = self.minmax(input_image[xmin : xmax, ymin : ymax])
                mod_img[x][y] = (maxmin / 2) + (minmax / 2)

        return mod_img, width, height

    def low_pass(self, input_image, filter_size):

        width = input_image.shape[0]
        height = input_image.shape[1]
        newShape = list(map(int, [width, height, 1]))
        mod_img = np.zeros(newShape, dtype = np.uint8)
        fix = int((filter_size - 1) / 2)
        for x in range(width):
            for y in range(height):
                xmin = (x - fix) if(x - fix) >= 0 else 0
                ymin = (y - fix) if (y - fix) >= 0 else 0
                xmax = (x + fix + 1) if (x + fix + 1) <= width else width
                ymax = (y + fix + 1) if (y + fix + 1) <= height else height
                tmp_list = input_image[xmin : xmax, ymin : ymax].flatten()
                while len(tmp_list) > filter_size * filter_size:
                    tmp_list = np.append(tmp_list, 0)
                mean = tmp_list.sum() / (filter_size * filter_size)
                mod_img[x][y] = int(mean)
        return mod_img, width, height

    def high_pass(self, input_image, filter_size):

        # width = input_image.shape[0]
        # height = input_image.shape[1]
        # mod_img = np.copy(input_image)
        # low_image, w, h = self.low_pass(input_image, filter_size)
        # mod_img = mod_img - low_image

        width = input_image.shape[0]
        height = input_image.shape[1]
        newShape = list(map(int, [width, height, 1]))
        mod_img = np.zeros(newShape, dtype = np.uint8)
        fix = int((filter_size - 1) / 2)
        if filter_size == 3:
            kernel = np.array([[-1, -1, -1],
                               [-1,  8, -1],
                               [-1, -1, -1]])
        elif filter_size == 5:
            kernel = np.array([[-1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, -1],
                               [-1, -1, 24, -1, -1],
                               [-1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, -1]])
        elif filter_size == 7:
            kernel = np.array([[-1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, 48, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1]])
        for x in range((fix), (width - fix)):
            for y in range((fix), (height - fix)):
                xmin = (x - fix)
                ymin = (y - fix)
                xmax = (x + fix + 1)
                ymax = (y + fix + 1)
                data = input_image[xmin : xmax, ymin : ymax]
                # print("\n\ndata: {0}".format(data))
                data = np.resize(data, (filter_size, filter_size))
                result = np.multiply(data, kernel)
                mean = result.sum()
                if mean < 0: mean = 0
                if mean > 255: mean = 255
                mod_img[x][y] = int(mean)
        # mod_img = input_image - mod_img
        return mod_img, width, height

    def edge_cris(self, input_image):

        width = input_image.shape[0]
        height = input_image.shape[1]
        newShape = list(map(int, [width, height, 1]))
        mod_img = np.zeros(newShape, dtype = np.uint8)
        mod_img = np.copy(input_image)
        filter_size = 3
        fix = int((filter_size - 1) / 2)

        # kernel = np.array([[-1, -1, -1],
        #                    [-1,  9, -1],
        #                    [-1, -1, -1]])
        kernel = np.array([[ 0, -1,  0],
                           [-1,  5, -1],
                           [ 0, -1,  0]])
        # kernel = np.array([[ 1, -2,  1],
        #                    [-2,  5, -2],
        #                    [ 1, -2,  1]])

        for x in range((fix), (width - fix)):
            for y in range((fix), (height - fix)):
                xmin = (x - fix)
                ymin = (y - fix)
                xmax = (x + fix + 1)
                ymax = (y + fix + 1)
                data = input_image[xmin : xmax, ymin : ymax]
                data = np.resize(data, (filter_size, filter_size))
                result = np.multiply(data, kernel)
                # print("result: {0}\n\n".format(result))
                mean = result.sum()
                if mean < 0: mean = 0
                if mean > 255: mean = 255
                # mean /=  (filter_size * filter_size)
                mod_img[x][y] = int(mean)
        # mod_img = input_image - mod_img
        return mod_img, width, height

    def high_boost(self, input_image, filter_size, a):

        width = input_image.shape[0]
        height = input_image.shape[1]
        newShape = list(map(int, [width, height, 1]))
        mod_img = np.zeros(newShape, dtype = np.uint8)
        mod_img = np.copy(input_image)
        fix = int((filter_size - 1) / 2)
        if filter_size == 3:
            kernel = np.array([[-1, -1, -1],
                               [-1,  (9*a)-1, -1],
                               [-1, -1, -1]])
        elif filter_size == 5:
            kernel = np.array([[-1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, -1],
                               [-1, -1, (25*a)-1, -1, -1],
                               [-1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, -1]])
        elif filter_size == 7:
            kernel = np.array([[-1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, (49*a)-1, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1]])
        for x in range((fix), (width - fix)):
            for y in range((fix), (height - fix)):
                xmin = (x - fix)
                ymin = (y - fix)
                xmax = (x + fix + 1)
                ymax = (y + fix + 1)
                data = input_image[xmin : xmax, ymin : ymax]
                # print("\n\ndata: {0}".format(data))
                data = np.resize(data, (filter_size, filter_size))
                result = np.multiply(data, kernel)
                mean = result.sum()
                if mean < 0: mean = 0
                if mean > 255: mean = 255
                mod_img[x][y] = int(mean)
        return mod_img, width, height

    def gradient(self, input_image, type):
        width = input_image.shape[0]
        height = input_image.shape[1]
        newShape = list(map(int, [width, height, 1]))
        mod_img = np.zeros(newShape, dtype = np.uint8)

        if type == "robert":
            kernelx = np.array([[1, 0],
                                [0, -1]])
            kernely = np.array([[0, -1],
                                [1,  0]])
            filter_size = 2
            fix = 1
            for x in range(0, (width - 1)):
                for y in range(0, (height - 1)):
                    xmin = (x)
                    ymin = (y)
                    xmax = (x + fix + 1)
                    ymax = (y + fix + 1)
                    data = input_image[xmin : xmax, ymin : ymax]
                    # print("\n\ndata: {0}".format(data))
                    data = np.resize(data, (filter_size, filter_size))
                    resultx = np.multiply(data, kernelx)
                    resulty = np.multiply(data, kernely)
                    meanx = resultx.sum()
                    meany = resulty.sum()
                    # if meanx < 0: meanx = 0
                    # if meanx > 255: meanx = 255
                    # if meany < 0: meany = 0
                    # if meany > 255: meany = 255
                    final = math.sqrt((meanx * meanx) + (meany * meany))
                    if final < 0: final = 0
                    if final > 255: final = 255
                    mod_img[x][y] = int(final)

        elif type == "sobel":
            kernelx = np.array([[-1, 0, 1],
                                [-2, 0, 2],
                                [-1, 0, 1]])
            kernely = np.array([[ 1, 2, 1],
                                [ 0, 0, 0],
                                [-1,-2,-1]])
            filter_size = 3
            fix = 1
            for x in range(0, (width - 1)):
                for y in range(0, (height - 1)):
                    xmin = (x - fix)
                    ymin = (y - fix)
                    xmax = (x + fix + 1)
                    ymax = (y + fix + 1)
                    data = input_image[xmin : xmax, ymin : ymax]
                    data = np.resize(data, (filter_size, filter_size))
                    resultx = np.multiply(data, kernelx)
                    resulty = np.multiply(data, kernely)
                    meanx = resultx.sum()
                    meany = resulty.sum()
                    final = math.sqrt((meanx * meanx) + (meany * meany))
                    if final < 0: final = 0
                    if final > 255: final = 255
                    mod_img[x][y] = int(final)

        elif type == "prewitt":
            kernelx = np.array([[-1, 0, 1],
                                [-1, 0, 1],
                                [-1, 0, 1]])
            kernely = np.array([[ 1, 1, 1],
                                [ 0, 0, 0],
                                [-1,-1,-1]])
            filter_size = 3
            fix = 1
            for x in range(0, (width - 1)):
                for y in range(0, (height - 1)):
                    xmin = (x - fix)
                    ymin = (y - fix)
                    xmax = (x + fix + 1)
                    ymax = (y + fix + 1)
                    data = input_image[xmin : xmax, ymin : ymax]
                    data = np.resize(data, (filter_size, filter_size))
                    resultx = np.multiply(data, kernelx)
                    resulty = np.multiply(data, kernely)
                    meanx = resultx.sum()
                    meany = resulty.sum()
                    final = math.sqrt((meanx * meanx) + (meany * meany))
                    if final < 0: final = 0
                    if final > 255: final = 255
                    mod_img[x][y] = int(final)
        return mod_img, width, height
            