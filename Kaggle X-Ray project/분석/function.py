import numpy as np
import pydicom
from pydicom.pixel_data_handlers.util import apply_voi_lut
import cv2


#matplotlib inline


def read_xray(path, voi_lut = True, fix_monochrome = True):
    dicom = pydicom.read_file(path)
    
    
    # VOI LUT (if available by DICOM device) is used to transform raw DICOM data to "human-friendly" view
    if voi_lut:
        data = apply_voi_lut(dicom.pixel_array, dicom)
    else:
        data = dicom.pixel_array
               
    # depending on this value, X-ray may look inverted - fix that:
    if fix_monochrome and dicom.PhotometricInterpretation == "MONOCHROME1":
        data = np.amax(data) - data
        
    data = data - np.min(data)
    data = data / np.max(data)
    data = (data * 255).astype(np.uint8)
        
    return data

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

blue = (255, 0, 0)
green = (0, 255, 0)
red = (0, 0, 255)

# https://kuklife.tistory.com/125
def get_iou(a, b, epsilon=1e-5):
    """ Given two boxes `a` and `b` defined as a list of four numbers:
            [x1,y1,x2,y2]
        where:
            x1,y1 represent the upper left corner
            x2,y2 represent the lower right corner
        It returns the Intersect of Union score for these two boxes.
 
    Args:
        a:          (list of 4 numbers) [x1,y1,x2,y2]
        b:          (list of 4 numbers) [x1,y1,x2,y2]
        epsilon:    (float) Small value to prevent division by zero
 
    Returns:
        (float) The Intersect of Union score.
    """
    # COORDINATES OF THE INTERSECTION BOX
    x1 = max(a[0], b[0])
    y1 = max(a[1], b[1])
    x2 = min(a[2], b[2])
    y2 = min(a[3], b[3])
 
    # AREA OF OVERLAP - Area where the boxes intersect
    width = (x2 - x1)
    height = (y2 - y1)
    # handle case where there is NO overlap
    if (width<0) or (height <0):
        return 0.0
    area_overlap = width * height
 
    # COMBINED AREA
    area_a = (a[2] - a[0]) * (a[3] - a[1])
    area_b = (b[2] - b[0]) * (b[3] - b[1])
    area_combined = area_a + area_b - area_overlap
 
    # RATIO OF AREA OF OVERLAP OVER COMBINED AREA
    iou = area_overlap / (area_combined+epsilon)
    return iou


boxA = (244, 656, 1184, 2655)
boxB = (949, 1458, 1009, 1527)

iou = get_iou(boxA, boxB)
print(iou)

boxA = (1044.0, 1579.0, 2098.0, 1971.0)
boxB = (1109.0, 1552.0, 2416.0, 2033.0)
iou = get_iou(boxA, boxB)
print(iou)
