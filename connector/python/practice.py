import cv2
import numpy as np
import function

def appear_result(circle_count, no_circle_count):
    if (circle_count != 6):
        sentence = "Holl Error"
        cv2.putText(img, sentence, result_point, cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255) , 2)
    else :
        if (no_circle_count < 12 and no_circle_count > 14):
            sentence = "Rectangle Error"
            cv2.putText(img, sentence, result_point, cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255) , 2)

def cal_moment(contour):
    moment = cv2.moments(contour)
    cX = int(moment["m10"] / (moment["m00"] + 1e-5))
    cY = int(moment["m01"] / (moment["m00"] + 1e-5))

    return (cX, cY)

def sort_contours(contours, center):
    center_x, center_y = center[0], center[1]
    contours_size = len(contours)
    left = []
    right = []
    center = []
    for i in range(len(moment_point)):
        if moment_point[i][0] < center_x:
            left.append(contours[i])
        else:
            right.append(contours[i])
    
    
        

def entire_moment(img): # 제품의 무게중심
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, gray = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY_INV)

    contours, hierarchy = cv2.findContours(gray, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    c = max(contours, key= cv2.contourArea)  

    moment = cv2.moments(c)
    cX = int(moment["m10"] / moment["m00"] + 1e-5) # 분모가 0이 되지 않게 아주 작은 1e-5값을 더함
    cY = int(moment["m01"] / moment["m00"] + 1e-5)

    return (cX, cY)
    

src = function.imread("./images\pcb\양품1_1.bmp")
# 홀불량6_1.bmp 불가
src = function.FitToWindowSize(src)
img = src.copy()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#print(img.shape)

i = 0 # contour 개수 저장
cnt_area = [] # 각 contour에 면적을 저장하는 리스트
cnt_per = [] # 각 contour에 호 길이를 저장하는 리스트
cnt_point = [] # 각 contour를 boundingRect()한 좌표 (x,y,w,h)
moment_point = [] # 각 contour의 무게중심을 저장하는 리스트
circle_count = 0
no_circle_count = 0
#result_point = (int(img.shape[0]*2/4), int(i                                                                                                                         g.shape[1]*3/4 - 100)) # 처리 결과 적을 포인트

check_circle_area = 1500 # 면적으로 원 추출 할 수 있는 넓이

_, binary = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)

kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
close_img = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=1)
close_img = cv2.morphologyEx(close_img, cv2.MORPH_OPEN, kernel, iterations=1)

contours, hierarchy = cv2.findContours(close_img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

for i in range(len(contours)):
    
    x,y,w,h = cv2.boundingRect(contours[i])
    cnt_point.append((x,y,w,h))
    min_point = (cnt_point[i][0], cnt_point[i][1])  # boundingRect의 시작점
    max_point = (cnt_point[i][0] + cnt_point[i][2], cnt_point[i][1]+ cnt_point[i][3]) # boundingRect의 끝점

    sentence = str(i) + " (" + str(contours[i][0][0][0]) + "," + str(contours[i][0][0][1]) + ")" 
    cv2.putText(img, sentence, (tuple(contours[i][0][0])), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)                                   

    cnt_area.append(cv2.contourArea(contours[i])) # 면적
    #print(i, cnt_area[i])
    cnt_per.append(cv2.arcLength(contours[i], True)) # 호 길이

    if((cnt_area[i] < 2000 and cnt_area[i] > 1000) or cnt_area[i] <50):
        cv2.drawContours(img, [contours[i]], 0, (255, 0, 0), 2) # 원
        circle_count += 1
    else:
        cv2.drawContours(img, [contours[i]], 0, (0, 0, 255), 2) # 원 외의 것
        no_circle_count += 1
    #print(i, cnt_area[i])

    moment_point.append(cal_moment(contours[i]))
    cv2.circle(img, moment_point[i], 2, (0, 0, 255), -1)


# 결과와 카운트 출력
sentence = "circle_count = " + str(circle_count) + ", " + "no_circle_count = " + str(no_circle_count)
cv2.putText(img, sentence, (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255) , 2)
appear_result(circle_count, no_circle_count)    

entire_moment_point = entire_moment(img)        # 전체 제품의 무게 중심
cv2.circle(img, entire_moment_point, 5, (0, 0, 255), -1)



# print(contours[0].shape)
# print(contours[0][0][0][0])

#print(cnt_point[0][0])
#print("contour count", i)

cv2.imshow("img", img)
#cv2.imshow("9x9 kernel close_img", close_img)

cv2.waitKey(0)
cv2.destroyAllWindows()

