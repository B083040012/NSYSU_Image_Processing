import math
import numpy as np
from PIL import Image

class mpegVideo():
    def __init__(self):
        self.fps = 23
        self.total_frame_num = 0
        self.current_frame_index = 0
        self.frame_list = list()
        self.compress_frame_list = list()
        self.motion_vector_map = None

    def read_from_filename(self, filenames):
        try:
            for file in filenames:
                tiff_im = Image.open(file)
                tiff_imarray = np.array(tiff_im)
                self.frame_list.append(tiff_imarray)
        except:
            return -1
        self.total_frame_num = len(self.frame_list)
        self.width, self.height = self.frame_list[0].shape[0], self.frame_list[0].shape[1]
        first_frame = np.copy(self.frame_list[0])
        self.compress_frame_list.append(first_frame)

    def update_index(self, type):
        if type == "next":
            self.current_frame_index += 1
            if self.current_frame_index >= self.total_frame_num:
                self.current_frame_index = 0
        elif type == "prev":
            self.current_frame_index -= 1
            if self.current_frame_index < 0:
                self.current_frame_index = self.total_frame_num - 1

    def rotate(self, pivot_point, rotate_point, angle):
        s = math.sin(angle)
        c = math.cos(angle)

        rotate_point[0] -= pivot_point[0]
        rotate_point[1] -= pivot_point[1]

        newx = rotate_point[0] * c - rotate_point[1] * s
        newy = rotate_point[0] * s + rotate_point[1] * c

        rotate_point[0] = newx + pivot_point[0]
        rotate_point[1] = newy + pivot_point[1]

        return rotate_point[0], rotate_point[1]


    def update_motion_vector_map(self, x, y, vector):
        if self.motion_vector_map is None:
            newShape = list(map(int, [self.width, self.height]))
            self.motion_vector_map = np.zeros(newShape, dtype = np.uint8)
        sub_map = np.zeros((8, 8), dtype = np.uint8)
        # full_map = np.zeros((64, 64), dtype = np.uint8)
        origin = [4, 4]
        norm = np.linalg.norm(vector)
        if norm == 0:
            sub_map[3:5, 3:5] = 255
        else:
            mydegrees = math.degrees(math.atan2(vector[0], vector[1]))
            # print("unit_vector: {0}".format(vector))
            # print("degeee: {0}".format(mydegrees))
            if mydegrees >= 0 and mydegrees < 90:
                index = [[4, 4], [5, 5], [6, 6], [7, 7], [7, 6], [7, 5], [6, 7], [5, 7]]
            elif mydegrees >= 90 and mydegrees <= 180:
                index = [[4, 4], [3, 5], [2, 6], [1, 7], [1, 6], [1, 5], [2, 7], [3, 7]]
            elif mydegrees < 0 and mydegrees > -90:
                index = [[4, 4], [5, 3], [6, 2], [7, 1], [6, 1], [5, 1], [7, 2], [7, 3]]
            elif mydegrees <= -90 and mydegrees >= -180:
                index = [[4, 4], [3, 3], [2, 2], [1, 1], [1, 2], [1, 3], [2, 1], [3, 1]]
            for i in index: sub_map[i[0], i[1]] = 255
            unit_vector = vector / norm
            # for i in range(-3, 3):
            #     sub_map[int(origin[0] + i * unit_vector[0]), int(origin[1] + i * unit_vector[1])] = 255
            # pivot_point = [int(origin[0] + 3 * unit_vector[0]), int(origin[1] + 3 * unit_vector[1])]
            # for i in range(1, 3):
            #     rotate_point = [int(origin[0] + i * unit_vector[0]), int(origin[1] + i * unit_vector[1])]
            #     newx, newy = self.rotate(pivot_point, rotate_point, 45)
            #     sub_map[int(newx), int(newy)] = 255
        self.motion_vector_map[y:(y + 8), x:(x + 8)] = sub_map

        return sub_map