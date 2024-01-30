import os
import zipfile
import shutil
import sys

def main():
    file_dir = sys.argv[1]
    extract_dir = sys.argv[2]
    thumb_dir = 'thumbnail/thumbnail400x400.png'
    # file_dir = "/home/roebin/Desktop/sample_usb_list/"
    # extract_dir = '/home/roebin/Desktop/G3D-Printer/build/resources/thumbnail/image/'

    #deleting the thumbnail folder 
    try:
        shutil.rmtree(extract_dir)
        print('Directory thumbnail is deleted')
    except FileNotFoundError:
        print('File is not found')


    try:
        os.makedirs(extract_dir)
        print('Directory ', extract_dir, 'Created')
    except FileExistsError:
        print('Directory ', extract_dir, 'already existed')


    g3d_file = os.listdir(file_dir)
    g3d_file = [ i for i in g3d_file if i.endswith(".nex")]

    print("Received path new: ", file_dir)
    print(g3d_file)
    
    for filename in g3d_file:
            print(file_dir + filename)
            with zipfile.ZipFile(file_dir + filename, 'r') as my_zip:
                try:
                    my_zip.extract(thumb_dir, file_dir)
                    shutil.copy(file_dir + thumb_dir, extract_dir + filename.replace('.nex','.png'))
                    print("DEBUG: ", file_dir + thumb_dir, extract_dir + filename.replace('.nex','.png'))
                except:
                    print("error in extracting a given file")

    try:
        thumb_usb_dir = file_dir + 'thumbnail/'
        shutil.rmtree(thumb_usb_dir)
        print('Deleting thumbnail folder')
    except FileNotFoundError:
        print("File not found")

 

try:
    main()
    print("DONE")
except OSError as e:
    print(e)
