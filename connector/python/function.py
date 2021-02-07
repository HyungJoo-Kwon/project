import cv2
import numpy as np

def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):       # numpy로 파일을 우회하여야 업로드
    try: 
        n = np.fromfile(filename, dtype) 
        img = cv2.imdecode(n, flags) 
        return img 
    except Exception as e: 
        print(e) 
        return None

def FitToWindowSize(image): # image resize https://076923.github.io/posts/Python-opencv-8/
    #윈도우 크기 얻기
    from win32api import GetSystemMetrics
    # print("Width =", GetSystemMetrics(0))
    # print("Height =", GetSystemMetrics(1))
    #이미지 크기 얻기
    #print('image {}'.format(image.shape))
    win_w=GetSystemMetrics(0)
    win_h=GetSystemMetrics(1)
    img_h, img_w = image.shape[:2]

    if(img_h > win_h or img_w > win_w):   
        rate_width =  (win_w / img_w)*0.95
        rate_height =  (win_h / img_h)*0.95
        scale = rate_width if (rate_width < rate_height) else rate_height

    image_resized = cv2.resize(image, dsize=(0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
    # cv2.imshow('image_resize',image_resized)
    return image_resized

red = (0,0,255)
green = (0,255,0)
blue = (255,0,0)
yellow = (0,255,255)
cyan = (255,255,0)
black = (0,0,0)
white = (255,255,255)