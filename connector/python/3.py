import cv2
import numpy as np
import function
import copy
import math
import matplotlib as plt

# del list[:] # list 안의 데이터만 삭제
# 리스트 자체를 메모리에서 지우고자 할때는
# del list # 리스트 자체를 삭제



def point_to_point(x1, y1, x2, y2): # 두 점 사이의 거리
    x = abs(x2-x1)
    y = abs(y2-y1)
    length = math.sqrt((x*x) + (y*y))
    
    return length

def select_near_point(list, x): # 전역변수에다 집어넣는 방식 이용
    try:
        global src
        if(x < src.shape[1]/2):
            list.index(x)
        
            global check_rect_mean1_y_index, check_rect_mean2_y_index
        
            check_rect_mean1_y_index = list.index(x)
            check_rect_mean2_y_index = list.index(x)
            print("x",x)
        else:
            pass
        
    except ValueError:
        x += 1
        select_near_point(list, x)
        


img = function.imread("./connector/python/images/01_connecter_1/6.bmp")
src = img.copy()
src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(src_gray, 120, 255, cv2.THRESH_BINARY_INV) 
rect = binary.copy()
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (9,9))
rect = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations= 10)

contours, hierarchy = cv2.findContours(rect, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
max = max(contours, key= cv2.contourArea)
print(type(contours))
cv2.drawContours(src, [max], 0, (0, 0, 255), 1)

for i in range(len(contours)):
    cv2.drawContours(src, [contours[i]], 0, (0,255,0),2)

cnt_list_x = []
cnt_list_y = []
for i in range(len(max)):
    cnt_list_x.append(max[i][0][0])
    cnt_list_y.append(max[i][0][1])
temp = copy.deepcopy(cnt_list_x)
temp.sort()

rect_min_x = temp[0]    # contour 젤 작은 x값
rect_max_x = temp[-1]   # contour 젤 큰 x값

del temp[:]
temp = copy.deepcopy(cnt_list_y)
temp.sort()

rect_min_y = temp[0]
rect_max_y = temp[-1]

cv2.line(src, (rect_min_x, 0), (rect_min_x,src.shape[0]), (255, 0, 0), 2)
cv2.line(src, (rect_max_x, 0), (rect_max_x,src.shape[0]), (255, 0, 0), 2)
cv2.line(src, (0, rect_max_y), (src.shape[1], rect_max_y), (255, 0, 0), 2)
cv2.line(src, (0, rect_min_y), (src.shape[1], rect_min_y), (255, 0, 0), 2)

# https://m.blog.naver.com/sw4r/221976911807
# 중복된 원소들의 인덱스 모두 찾기
# 리스트를 배열로 만든후 np.where 사용

temp = np.array(cnt_list_y)
check = np.where(temp == 0)[0]
check = check.tolist()

check_val = []
for i in range(len(check)):
    check_val.append(cnt_list_x[check[i]])
check_max_x = check_val[-1]
check_min_x = check_val[0]

cv2.line(src, (check_min_x, 0), (check_min_x, src.shape[0]), (255, 0, 0), 2)
cv2.line(src, (check_max_x, 0), (check_max_x, src.shape[0]), (255, 0, 0), 2)

check_rect_mean1_x = int(abs(rect_min_x + check_min_x)/2)
cv2.line(src, (check_rect_mean1_x, 0), (check_rect_mean1_x, src.shape[0]), (0, 0, 255), 2)
check_rect_mean2_x = int(abs(rect_max_x + check_max_x)/2)
cv2.line(src, (check_rect_mean2_x, 0), (check_rect_mean2_x, src.shape[0]), (0, 0, 255), 2)

check_rect_mean1_y_index, check_rect_mean2_y_index = 0, 0 # select_near_point() 함수에서 전역변수로 이용
select_near_point(cnt_list_x, check_rect_mean1_x)
check_rect_mean1_y = cnt_list_y[check_rect_mean1_y_index]
select_near_point(cnt_list_x, check_rect_mean2_x)
check_rect_mean2_y = cnt_list_y[check_rect_mean2_y_index]

target_p1 = (check_rect_mean1_x, check_rect_mean1_y)
target_p2 = (check_rect_mean2_x, check_rect_mean2_y) 
target_rect_p1 = (rect_min_x, check_rect_mean1_y)
target_rect_p2 = (rect_max_x, check_rect_mean2_y)
cv2.line(src, target_rect_p1, target_rect_p2, (255, 255, 0), 2)

mask = np.zeros(src.shape, dtype="uint8")
if target_rect_p1[1] > target_rect_p2[1]:
    target = (target_rect_p1[0], target_rect_p2[1])
    cv2.rectangle(mask, target, (rect_max_x,rect_max_y),(255, 255, 255), -1)
    p1 = (target[0], int((rect_max_y+target[1])/2) )
    p2 = (rect_max_x, int((rect_max_y+target[1])/2) )
    #cv2.line(src, p1, p2, (0, 255, 0), 2)
    center_rect = (int((p1[0]+p2[0])/2), int((p1[1]+p2[1])/2))
else:
    cv2.rectangle(mask, target_rect_p1, (rect_max_x,rect_max_y),(255, 255, 255), -1)
    p1 = (target_rect_p1[0], int((rect_max_y+target_rect_p1[1] )/2))
    p2 = (rect_max_x, int((rect_max_y+target_rect_p1[1])/2))
    #cv2.line(src, p1, p2, (0, 255, 0), 2)
    center_rect = (int((p1[0]+p2[0])/2), int((p1[1]+p2[1])/2))

cv2.circle(src, center_rect, 5, (0, 255, 0), -1)


mask = cv2.bitwise_and(img, mask)
mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(mask_gray, 130, 255, cv2.THRESH_BINARY) # gray -> threshold 순으로

contours, hierarchy = cv2.findContours(binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
moment_up_x = []
moment_up_y = []
moment_down_x = []
moment_down_y = []
for i in range(len(contours)):
    moment = cv2.moments(contours[i])
    cX = int(moment["m10"] / (moment["m00"] + 1e-5))
    cY = int(moment["m01"] / (moment["m00"] + 1e-5))
    area = cv2.contourArea(contours[i])
    if area > 200: 
        if check_rect_mean1_x < cX and cX < check_rect_mean2_x:
            
            length = point_to_point(0,center_rect[1], 0, cY)
            if length < 120 :
                cv2.drawContours(src, [contours[i]], 0, (0,255,0),2)
                cv2.circle(src, (cX,cY), 5, (0, 0, 255), -1)  
                if cY > center_rect[1]:
                    moment_down_x.append(cX)
                    moment_down_y.append(cY)
                else :
                    moment_up_y.append(cY)
                    moment_up_x.append(cX)

moment_down_x_sort = copy.deepcopy(moment_down_x)
moment_down_x_sort.sort()
moment_up_x_sort = copy.deepcopy(moment_up_x)
moment_up_x_sort.sort()

print("len(moment_up_x)", len(moment_up_x))
print("len(moment_down_x)", len(moment_down_x))

up_count = 1
for i in range(len(moment_up_x)):
    m_index = moment_up_x.index(moment_up_x_sort[i])
    target_point = (moment_up_x[m_index]-10, moment_up_y[m_index]+50)
    cv2.putText(src, str(up_count), target_point, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255) , 2)
    up_count += 1

down_count = 1  
for i in range(len(moment_up_x)):
    m_index = moment_down_x.index(moment_down_x_sort[i])
    target_point = (moment_down_x[m_index]-10, moment_down_y[m_index]-30)
    cv2.putText(src, str(down_count), target_point, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255) , 2)
    down_count += 1  
        

test = binary.copy()
src = function.FitToWindowSize(src) 
img = function.FitToWindowSize(img)
test = function.FitToWindowSize(test)

cv2.imshow("src",src)
cv2.imshow("img", img)
#cv2.imshow("test", test)




cv2.waitKey(0)
cv2.destroyAllWindows()