import pyrealsense2 as rs
import matplotlib.pyplot as plt
import numpy as np
import imageio
import time
import cv2
import glob
import os
import multiprocessing as mp
from itertools import repeat


def extract_tiff_from_bag(filename, destination):
    try:
        pipeline = rs.pipeline()
        config = rs.config()
        config.enable_device_from_file(filename, False)
        pipeline.start(config)
    except RuntimeError:
        return




    decimation = rs.decimation_filter()
    decimation.set_option(rs.option.filter_magnitude, 1)

    spatial = rs.spatial_filter()
    spatial.set_option(rs.option.filter_magnitude, 5)
    spatial.set_option(rs.option.filter_smooth_alpha, 1)
    spatial.set_option(rs.option.filter_smooth_delta, 50)
    spatial.set_option(rs.option.holes_fill, 2)

    i = 0
    stop = True
    while True:
        try:
            frames = pipeline.wait_for_frames(1000)
            depth_frame = frames.get_depth_frame()

            decimated_depth = decimation.process(depth_frame)
            filtered_depth = spatial.process(decimated_depth)
            depth_image = np.asanyarray(filtered_depth.get_data())
            imageio.imwrite(destination+f'{i}.tif', depth_image, 'TIFF')
            time.sleep(0.01)
            i+=1

        except RuntimeError:
            pipeline.stop()
            stop = False
            break

    if stop == True:
        pipeline.stop()
    return

def extract_all_tiff_from_folder(filenames, destinations):
    for i in range(0, len(filenames)):
        extract_tiff_from_bag(filenames[i], destinations[i])

#######################################################

def main():
    time1 = time.time()
    filename = 'From_pi'
    filenames = glob.glob(filename+'/*/*/*.bag')
    #print(len(filenames))
    # print(filenames)
    destinations = []

    dest_dir = filename+'_tif_multi'
    try:
        os.mkdir(dest_dir)
    except FileExistsError:
        pass

    for i in range(0, len(filenames)):
        os.chdir(dest_dir)
    #os.mkdir(os.path.basename(filenames[i])[0:-4])
        destinations.append('\\Users\\zacha\\Documents\\Precision Ranching Code\\'+dest_dir+'\\'+os.path.basename(filenames[i])[0:-4])
        os.chdir('..')


        # num_cpu = mp.cpu_count()



    # for w in range(num_cpu):
    #     p = mp.Process(target=extract_all_tiff_from_folder, args=(filenames, destinations))
    #     processes.append(p)
    #     p.start()
    #
    # for p in processes:
    #     p.join()
    pool = mp.Pool(16)
    m = mp.Manager()
    q = m.Queue()
    #zip(filenames, destinations)
    #pool_tuple = [(x, q) for x in range(1, no_pages)]
    #for i in range(0, len(filenames)):
    pool.starmap(extract_tiff_from_bag, zip(filenames, destinations))
    pool.close()

    time2 = time.time()
    print('Completed in ', time2-time1, ' seconds')
if __name__=='__main__':
    mp.freeze_support()
    main()
