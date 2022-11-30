import numpy as np
from PIL import Image

class mpegVideo():
    def __init__(self):
        self.fps = 23
        self.total_frame_num = 0
        self.current_frame_index = 0
        self.frame_list = list()
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

    def update_index(self, type):
        if type == "next":
            self.current_frame_index += 1
            if self.current_frame_index >= self.total_frame_num:
                self.current_frame_index = 0
        elif type == "prev":
            self.current_frame_index -= 1
            if self.current_frame_index < 0:
                self.current_frame_index = self.total_frame_num - 1

    def update_motion_vector_map(self, x, y, vector):
        if self.motion_vector_map is None:
            newShape = list(map(int, [self.width, self.height, 1]))
            self.motion_vector_map = np.zeros(newShape, dtype = np.uint8)