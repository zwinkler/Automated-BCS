import cv2

def video(timeStamp, seconds):
    os.mkdir(f'./videos/{timeStamp}/')
    out1 = cv2.VideoWriter(f'./videos/{timeStamp}/C.mp4',cv2.VideoWriter_fourcc('M','P','4','2'), fps, (640,480))
    out2 = cv2.VideoWriter(f'./videos/{timeStamp}/D.mp4',cv2.VideoWriter_fourcc('M','P','4','2'), fps, (640,480), 0)
    
    