from __future__ import print_function
import pyrealsense2.pyrealsense2 as rs
import numpy as np
import cv2
import time
from PIL import Image
import os
import mercury
import RPi.GPIO as GPIO
import multiprocessing as mp
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.IN)
from myFunctions import *

#initialize RFID reader
reader = mercury.Reader("tmr:///dev/ttyUSB0", baudrate=115200)
power = 2500

# store run time for file names
timeStamp = str(int(time.strftime("%Y"))%2000) + time.strftime("%m%d-%H%M%S")

# camera mode: video or image mode
mode = "image"
fps = 15

# create folder for output files
if(mode == "video"):
            # save frames as mp4. C is color D is depth
            try:
                os.chdir('/home/pi/Desktop/myCode/Working_ZW')
                os.mkdir(f'Camera/videos/{timeStamp}/')
            except FileExistsError:
                pass

            out1 = cv2.VideoWriter(f'Camera/videos/{timeStamp}/C.avi',cv2.VideoWriter_fourcc('X','V','I','D'), fps, (640,480))
            out2 = cv2.VideoWriter(f'Camera/videos/{timeStamp}/D.avi',cv2.VideoWriter_fourcc('X','V','I','D'), fps, (640,480))

elif(mode == "image"):
    try:
        os.chdir('/home/pi/Desktop/myCode/Working_ZW')
        #print(os.getcwd())

        os.mkdir(f'Camera/images/{timeStamp}')
    except FileExistsError:
        pass

# Configure depth and color streams

#queue = rs.frame_queue(10, keep_frames=True)

length, width = (640, 480)
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, length, width, rs.format.z16, fps)
config.enable_stream(rs.stream.color, length, width, rs.format.bgr8, fps)

# record .bag file
#config.enable_record_to_file('object_detection3.bag')



# Start streaming
pipe_profile = pipeline.start(config) #, queue)

decimation = rs.decimation_filter()
decimation.set_option(rs.option.filter_magnitude, 2)

spatial = rs.spatial_filter()
spatial.set_option(rs.option.filter_magnitude, 5)
spatial.set_option(rs.option.filter_smooth_alpha, 1)
spatial.set_option(rs.option.filter_smooth_delta, 50)
spatial.set_option(rs.option.holes_fill, 2)

thresh = rs.threshold_filter(min_dist = 0.1, max_dist = 3.0)
#thresh.set_option(min_dist = 0.1)
#thresh.set_option(max_dist = 3.0)

depth_sensor = pipe_profile.get_device().first_depth_sensor()

depth_sensor.set_option(rs.option.enable_auto_exposure, True)

n = 0
img_num = 0
time_flag = True

depth_train = np.zeros((length, width, 10))
color_train = np.zeros((length, width, 10))
depth_frame = pipeline.wait_for_frames().as_frameset().get_depth_frame()
depth_1 = depth_frame
depth_2 = depth_1
depth_3 = depth_2
depth_4 = depth_3
depth_5 = depth_4
depth_6 = depth_5
depth_7 = depth_6
depth_8 = depth_7
depth_9 = depth_8
try:
    while True:

        #checking to see if a new day has started
        currentTime = str(int(time.strftime("%Y"))%2000) + time.strftime("%m%d-%H%M%S")
        if (int(currentTime[7:]) < 100) and (int(currentTime[7:]) > 0) and (time_flag == True):
            timeStamp = str(int(time.strftime("%Y"))%2000) + time.strftime("%m%d-%H%M%S")
            time_flag = False

            try:
                os.mkdir(f'Camera/images/{timeStamp}')

            except FileExistsError:
                pass

            time.sleep(60)

        time_flag = True

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.as_frameset().get_depth_frame()
        depth_9 = depth_8
        depth_8 = depth_7
        depth_7 = depth_6
        depth_6 = depth_5
        depth_5 = depth_4
        depth_4 = depth_3
        depth_3 = depth_2
        depth_2 = depth_1
        depth_1 = depth_frame
        color_frame = frames.as_frameset().get_color_frame()



        #filtering
        #decimated_depth = decimation.process(depth_frame)
        thresh_frame = thresh.process(depth_frame)
        filtered_depth = spatial.process(thresh_frame)


        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        for i in range(9, 0, -1):
            depth_train[i] = depth_train[i-1]
            color_train[i] = color_train[i-1]
        
        depth_train[0] = np.asanyarray(filtered_depth.get_data())
        color_train[0] = np.asanyarray(color_frame.get_data())


        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_train[0], alpha=0.03), cv2.COLORMAP_JET)


        # Show images using cv2
        cv2.imshow('color', color_train[0])
        cv2.imshow('depth', depth_colormap)
        cv2.waitKey(1)
        #cv2.imshow("depth frame", depth_image)



        # Consider stopping the pipeline here to save power, but you will need to start it again when you want to take a picture




        #n = n+1

        #Check for proximity
        proximity = bool(GPIO.input(13))

        if(mode == "video") and (proximity == True):
            out1.write(color_train[0])
            out2.write(depth_colormap)

        elif(mode == "image") and (n%20 == 0) and (proximity == True):

            reader.set_region("NA2")
            reader.set_read_plan([1], "GEN2", bank=["user"], read_power=power)
            tag = reader.read(timeout=500)
            if len(tag)!=0:
                tag = str(bytes.fromhex(reader.read()[0].epc.decode('utf-8')))
                tag = tag[2:-1]
            if len(tag) == 0:
                tag = 'No_RFID'


            #color_rgb = color_image[:, :, [2, 1, 0]]
            #color = Image.fromarray(color_rgb)
            #color.save(f"Camera/images/{timeStamp}/{tag}_{img_num}_C.tif", "TIFF")

            #depth_rgb = depth_colormap[:, :, [2, 1, 0]]
            #depth = Image.fromarray(depth_image)
            #depth.save(f"Camera/images/{timeStamp}/{tag}_{img_num}_D.tif", "TIFF")

            for i in range(0, 9):
                cv2.imwrite(f"Camera/images/{timeStamp}/{tag}_{img_num}_{i}_C.tif", color_image)
                cv2.imwrite(f"Camera/images/{timeStamp}/{tag}_{img_num}_{i}_D.tif", depth_image)
            rs.save_single_frameset(f"Camera/images/{timeStamp}/{tag}_{img_num}_9_D").process(depth_9)
            rs.save_single_frameset(f"Camera/images/{timeStamp}/{tag}_{img_num}_8_D").process(depth_8)
            rs.save_single_frameset(f"Camera/images/{timeStamp}/{tag}_{img_num}_7_D").process(depth_7)
            rs.save_single_frameset(f"Camera/images/{timeStamp}/{tag}_{img_num}_6_D").process(depth_6)
            rs.save_single_frameset(f"Camera/images/{timeStamp}/{tag}_{img_num}_5_D").process(depth_5)
            rs.save_single_frameset(f"Camera/images/{timeStamp}/{tag}_{img_num}_4_D").process(depth_4)
            rs.save_single_frameset(f"Camera/images/{timeStamp}/{tag}_{img_num}_3_D").process(depth_3)
            rs.save_single_frameset(f"Camera/images/{timeStamp}/{tag}_{img_num}_2_D").process(depth_2)
            rs.save_single_frameset(f"Camera/images/{timeStamp}/{tag}_{img_num}_1_D").process(depth_1)
            rs.save_single_frameset(f"Camera/images/{timeStamp}/{tag}_{img_num}_0_D").process(depth_frame)
            img_num+=1



        n = n+1
        #if n>1000: # number of frames
            #print("Done!")
            #break

finally:


    # save recordings
    try:
        out1.release()
        out2.release()
    except:
        pass

    # Stop streaming
    pipeline.stop()
    cv2.destroyAllWindows()

    # display video druation
    if(mode == "video"):
        cap = cv2.VideoCapture(f'./videos/{timeStamp}/C.mp4')
        t = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))/fps
        cap.release()
        print(f"recorded duration: {t:.3} s")
