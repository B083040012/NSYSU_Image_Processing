import math
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
        if self.mod_image is None:
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
        elif type == "reverse":
            # matrix_1 = np.array([[1, 0, 0], [0, -1, 0], [-(self.rotate_width / 2), self.rotate_height / 2, 1]])
            matrix_1 = np.array([[1, 0, int(self.rotate_width / 2)], [0, 1, int(self.rotate_height / 2)], [0, 0, 1]])
        matrix_2 = np.array([[math.cos(degree), -(math.sin(degree)), 0], [math.sin(degree), math.cos(degree), 0], [0, 0, 1]])
        if type == "normal":
            # matrix_3 = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])
            matrix_3 = np.array([[1, 0, -int(self.mod_width / 2)], [0, 1, -int(self.mod_height / 2)], [0, 0, 1]])
        elif type == "reverse":
            # matrix_3 = np.array([[1, 0, 0], [0, -1, 0], [-int((self.rotate_width - self.mod_width) / 2), -int((self.rotate_height - self.mod_height) / 2), 1]])
            matrix_3 = np.array([[1, 0, -int(self.rotate_width / 2)], [0, 1, -int(self.rotate_height / 2)], [0, 0, 1]])
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
            # find the negative corrdinate that outsude the frame (used to adjust the rotated image)
            edge_list = [np.array([0, 0, 1]), np.array([self.rotate_width, 0, 1]), np.array([0, self.rotate_height, 1]), np.array([self.rotate_width, self.rotate_height, 1])]
            x_fix = int((self.rotate_width - self.mod_width) / 2)
            y_fix = int((self.rotate_height - self.mod_height) / 2)

            for x in range(self.rotate_image.shape[0]):
                for y in range(self.rotate_image.shape[1]):
                    cor = np.array([x, y, 1])
                    ori_cor = np.matmul(rotate_matrix, cor)
                    ori_x = int(ori_cor[0] + abs(x_fix) - abs(x_fix)); ori_y = int(ori_cor[1] + abs(y_fix) - abs(y_fix))
                    if ori_x < 0 or ori_x >=self.mod_width or ori_y < 0 or ori_y >=  self.mod_height:
                        continue
                    self.rotate_image[x, y] = self.mod_image[ori_x, ori_y]
        # self.mod_image = np.copy(self.rotate_image)
        # self.mod_width = self.rotate_width
        # self.mod_height = self.rotate_height
        return self.rotate_image, self.rotate_width, self.rotate_height

    def shear(self, slope):

        """
        Shear the image
        """
        self.initial_mod_image("general")
        height = self.mod_height + slope*self.mod_width + 0.5
        width = self.mod_width
        newShape = list(map(int, [abs(height), abs(width), 3]))
        shear_image = np.full(newShape, 255)
        for x in range(self.mod_height):
            for y in range(self.mod_width):
                new_x, new_y = (x + slope*y + 0.5), y
                shear_image[int(abs(new_x)), int(abs(new_y)), :] = self.ori_image[x, y, :]
        return shear_image, width, height

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
        thick = 10
        x_fix = current.x() - end.x(); y_fix = current.y() - end.y()
        accord_corx, accord_cory = begin.x() + x_fix, begin.y() + y_fix
        for t in range(-thick, thick):
            tmpx, tmpy = accord_corx + t, accord_cory + t
            orix, oriy = current.x() + t, current.y() + t
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
        result_image = np.zeros(newShape, dtype = np.uint8)
        for x in range(result_image.shape[0]):
            for y in range(result_image.shape[1]):
                if x >= self.mod_width or y >= self.mod_height:
                    result_image[x][y] = alpha_img[x][y]
                elif x >= alpha_width or y >= alpha_height:
                    result_image[x][y] = self.mod_image[x][y]
                else:
                    result_image[x][y] = alpha_img[x][y] * (1 - alpha_value) + self.mod_image[x][y] * alpha_value
        return result_image, width, height

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
            for x in range(int(center[0] - radius), int(center[0] + radius)):
                for y in range(int(center[1] - radius), int(center[1] + radius)):
                    if np.linalg.norm(np.array([x, y])-center) < radius:
                        if x < 0:
                            n_vec = np.array([1, 0])
                        elif y < 0:
                            n_vec = np.array([0, 1])
                        elif x >= width:
                            n_vec = np.array([-1, 0])
                        elif y >= height:
                            n_vec = np.array([0, -1])
                        else:
                            n_vec = np.array([0, 0])
                        new_vector = vector - 2 * np.dot(n_vec, vector) * n_vec
                        vector = new_vector
                        if n_vec[0] == 0 and n_vec[1] == 0:
                            ball_image[y, x, :] = [255, 255, 255]
        return ball_image, width, height, center, vector