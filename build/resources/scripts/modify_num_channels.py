from PIL import Image
import numpy as np
import sys
import os

def modify_num_channels(img_path, x_res_new, y_res_new, num_channel=3):
    with Image.open(img_path) as img_source:
        img_source = Image.open(img_path)
        data_source = np.array(img_source)
        data_destination = data_source.reshape(y_res_new, x_res_new, num_channel)
        img_destination = Image.fromarray(data_destination, 'RGB')
        img_destination.save(img_path)


if __name__ == "__main__":

    source_dir = sys.argv[1]
    x_res_new = int(sys.argv[2])
    y_res_new = int(sys.argv[3])

    if not os.path.exists(source_dir):
        print("[DEBUG]", "Directory is invalid.")

    source_png_name_list = os.listdir(source_dir)
    source_png_name_list = [os.path.join(
        source_dir, i) for i in source_png_name_list if i.endswith(".png")]
    source_png_name_list.sort()

    for img_path in source_png_name_list:
        modify_num_channels(img_path, x_res_new, y_res_new, num_channel=3)
