import cv2
import numpy as np
import function
import copy
import math

# sort시 데이터프레임 사용해야할듯, 필요한 부분잘라서 구하는것도 좋을듯

def point_to_line(P, A, B): # 점과 두점을 이은 직선 수직거리
    area = abs ( (A[0] - P[0]) * (B[1] - P[1]) - (A[1] - P[1]) * (B[0] - P[0]) )
    AB = ( (A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2 ) ** 0.5
    return ( area / AB )

def point_to_point(x1, y1, x2, y2): # 두 점 사이의 거리
    x = abs(x2-x1)
    y = abs(y2-y1)
    length = math.sqrt((x*x) + (y*y))
    
    return length


def select_near_point(list, y): # 제일 가까운 contour 찾기, 전역변수에다 집어넣는 방식 이용
    try:
        global center_x
        global cnt_list_x
    
        list.index(y)

        global target_index1, target_index2
        target_index1 = list.index(y)
        target_index2 = list.index(y)

        if(cnt_list_x[target_index1] < target_x or cnt_list_x[target_index2] < target_x ) :
            raise ValueError
        
    except ValueError:
        y -= 1
        select_near_point(list, y)

def equation(A, B): # 두점을 지나는 방정식의 기울기, 절편 구하기
    # A(A[0], [A[1]]), B(B[0], B[1])
    a = (B[1]-A[1]) / (B[0] - A[0])
    b = A[1] - a * A[0]

    return [a,b] # 기울기, 절편 return

def meet_point(a1, b1, a2, b2): # 두 직선의 기울기와 절편을 이용해 교점 구하기
    x = (b2-b1)/(a1-a2)
    y = a1*((b2-b1)/(a1-a2)) + b1
    return (int(x), int(y))

img = function.imread("./images/03_connector_2-01/핀 - 각도/1. 원본.bmp")
src = img.copy()
check = img.copy()
src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(src_gray, 70, 255, cv2.THRESH_BINARY_INV) 
binary[:src.shape[0], int(src.shape[1]*5/6) : src.shape[1]] = 0 # slice 시 행과 열 반대로
# kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (15, 15))
# binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=5)

contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
max = max(contours, key= cv2.contourArea)

check = cv2.isContourConvex(max)
if not check:   # cv2.isContourConvex() : 인자로 입력된 contour가 conver인지 체크
    hull = cv2.convexHull(max)
    #cv2.drawContours(src, [hull], 0, function.cyan, 3)

convex_x = []
convex_y = []
for i in range(len(hull)):
    point = (hull[i][0][0], hull[i][0][1])
    convex_x.append(point[0])
    convex_y.append(point[1])
    cv2.circle(src, point, 5, function.blue, -1)

# cv2.convexityDefects()
#https://m.blog.naver.com/PostView.nhn?blogId=samsjang&logNo=220524551089&proxyReferer=https:%2F%2Fwww.google.com%2F

# find rect center
check_center_y = copy.deepcopy(convex_y)
check_center_y.sort()
center_y = (check_center_y[0] + check_center_y[-1] )/ 2
print("center_y", center_y)
check_center_x = copy.deepcopy(convex_x)
check_center_x.sort()
center_x = (check_center_x[0] + check_center_x[-1] )/ 2
big_rect_max_x = check_center_x[-1]
print("center_x", center_x)
# cv2.circle(src, (int(center_x), int(center_y)), 5, function.,yellow -1)

# find left 2points
convex_left_up = []
convex_left_down = []
convex_left_up_x = []
convex_left_down_x = []
convex_left_up_y = []
convex_left_down_y = []

check = [] # left
for i in range(len(hull)):
    if hull[i][0][0] < center_x :
        point = (hull[i][0][0], hull[i][0][1])
        if hull[i][0][1] > center_y: # left_down
            convex_left_down_x.append(point[0])
            convex_left_down_y.append(point[1])
            convex_left_down.append((center_y - hull[i][0][1]))
        else: # left up
            convex_left_up_x.append(point[0])
            convex_left_up_y.append(point[1])
            convex_left_up.append((center_y - hull[i][0][1]))

check = copy.deepcopy(convex_left_up)
check.sort()
left_up_index = convex_left_up.index(check[0])
left_up = (convex_left_up_x[left_up_index], convex_left_up_y[left_up_index])
cv2.circle(src, left_up, 5, function.red, -1) 
check = copy.deepcopy(convex_left_down)
check.sort(reverse=True)
left_down_index = convex_left_down.index(check[0])
left_down = (convex_left_down_x[left_down_index], convex_left_down_y[left_down_index])
cv2.circle(src, left_down, 5, function.red, -1) 

left = [left_up, left_down]

# find target rect center
check = [] 
del convex_x[:]
del convex_y[:]
for i in range(len(hull)):
    if hull[i][0][0] < center_x :
        point = (hull[i][0][0], hull[i][0][1])
        convex_x.append(point[0])
        convex_y.append(point[1])
check = copy.deepcopy(convex_x)
check.sort()
target_x_min_index, target_x_max_index = convex_x.index(check[0]), convex_x.index(check[-1])
target_x = int((convex_x[target_x_min_index] + convex_x[target_x_max_index]) / 2)
check = copy.deepcopy(convex_y)
check.sort()
target_y_min_index, target_y_max_index = convex_y.index(check[0]), convex_y.index(check[-1])
target_y = int((convex_y[target_y_min_index] + convex_y[target_y_max_index]) / 2)
#cv2.circle(src, (target_x, target_y), 5, function.green, -1)

# find top points
convex_top_left = []
convex_top_right = []
convex_top_left_x = []
convex_top_right_x = []
convex_top_left_y = []
convex_top_right_y = []

for i in range(len(hull)):
    if hull[i][0][0] < center_x and target_y > hull[i][0][1]:
        point = (hull[i][0][0], hull[i][0][1])
        if hull[i][0][0] > target_x: # top right
            convex_top_right_x.append(point[0])
            convex_top_right_y.append(point[1])
            convex_top_right.append((target_x - hull[i][0][0]))
        else: # top left
            convex_top_left_x.append(point[0])
            convex_top_left_y.append(point[1])
            convex_top_left.append((target_x - hull[i][0][0]))

check = copy.deepcopy(convex_top_right)
check.sort(reverse=True)
top_right_index = convex_top_right.index(check[0])
top_right = (convex_top_right_x[top_right_index], convex_top_right_y[top_right_index])
cv2.circle(src, top_right, 5, function.red, -1) 
check = copy.deepcopy(convex_top_left)
check.sort()
top_left_index = convex_top_left.index(check[0])
top_left = (convex_top_left_x[top_left_index], convex_top_left_y[top_left_index])
cv2.circle(src, top_left, 5, function.red, -1) 

top = [top_left, top_right]

# find down points
convex_down_left = []
convex_down_right = []
convex_down_left_x = []
convex_down_right_x = []
convex_down_left_y = []
convex_down_right_y = []

for i in range(len(hull)):
    if hull[i][0][0] < center_x and target_y < hull[i][0][1]:
        point = (hull[i][0][0], hull[i][0][1])
        if hull[i][0][0] > target_x: # top right
            convex_down_right_x.append(point[0])
            convex_down_right_y.append(point[1])
            convex_down_right.append((target_x - hull[i][0][0]))
        else: # top left
            convex_down_left_x.append(point[0])
            convex_down_left_y.append(point[1])
            convex_down_left.append((target_x - hull[i][0][0]))

check = copy.deepcopy(convex_down_right)
check.sort(reverse=True)
down_right_index = convex_down_right.index(check[0])
down_right = (convex_down_right_x[down_right_index], convex_down_right_y[down_right_index])
cv2.circle(src, down_right, 5, function.red, -1) 
check = copy.deepcopy(convex_down_left)
check.sort()
down_left_index = convex_down_left.index(check[0])
down_left = (convex_down_left_x[down_left_index], convex_down_left_y[down_left_index])
cv2.circle(src, down_left, 5, function.red, -1) 

down = [down_left, down_right]

# find right points

max_right_up_y = []
max_right_down_y = []

for i in range(len(hull)):
    if  center_x < hull[i][0][0]:
        if center_y > hull[i][0][1]:
            max_right_up_y.append(hull[i][0][1])
        else:
            max_right_down_y.append(hull[i][0][1])

check = copy.deepcopy(max_right_up_y)
check.sort()
index = max_right_up_y.index(check[0])
right_up_y = max_right_up_y[index]

check = copy.deepcopy(max_right_down_y)
check.sort(reverse=True)
index = max_right_down_y.index(check[0])
right_down_y = max_right_down_y[index]

if top_left[1] > top_right[1]:
    val1 = top_right[1]
else:
    val1 = top_left[1]

if down_left[1] > down_right[1]:
    val2 = down_left[1]
else:
    val2 = down_right[1]

target_val1 = int((right_up_y+val1) / 2)
target_val2 = int((right_down_y+val2) / 2)

print(target_val1, target_val2)

cnt_list_x = []
cnt_list_y = []
for i in range(len(max)):
    cnt_list_x.append(max[i][0][0])
    cnt_list_y.append(max[i][0][1])

# cv2.drawContours(src, [max], 0, function.green, 2)

target_index1, target_index2 = 0, 0
select_near_point(cnt_list_y, target_val1)
cv2.circle(src, (cnt_list_x[target_index1], cnt_list_y[target_index1]), 5, function.red, -1)
right_up =  (cnt_list_x[target_index1], cnt_list_y[target_index1])
select_near_point(cnt_list_y, target_val2)
cv2.circle(src, (cnt_list_x[target_index2], cnt_list_y[target_index2]), 5, function.red, -1)
right_down = (cnt_list_x[target_index2], cnt_list_y[target_index2])

right = [right_up, right_down]

# top = [top_left, top_right]
# down = [down_left, down_right]
# right = [right_up, right_down]
# left = [left_up, left_down]

# 점마다 기울기 절편 추출
up_value = equation(top_left, top_right)
left_value = equation(left_up, left_down)
down_value = equation(down_left, down_right)
right_value = equation(right_up, right_down)

# 교점 구하기
left_up_point = meet_point(up_value[0], up_value[1], left_value[0], left_value[1])
cv2.circle(src, left_up_point, 7, function.cyan, -1)
right_up_point = meet_point(up_value[0], up_value[1], right_value[0], right_value[1])
cv2.circle(src, right_up_point, 7, function.cyan, -1)
left_down_point = meet_point(down_value[0], down_value[1], left_value[0], left_value[1])
cv2.circle(src, left_down_point, 7, function.cyan, -1)
right_down_point = meet_point(down_value[0], down_value[1], right_value[0], right_value[1])
cv2.circle(src, right_down_point, 7, function.cyan, -1)

cv2.line(src, left_up_point, right_up_point, function.yellow, 2)
cv2.line(src, left_up_point, left_down_point, function.yellow, 2)
cv2.line(src, left_down_point, right_down_point, function.yellow, 2)
cv2.line(src, right_up_point, right_down_point, function.yellow, 2)

target_center_top = (int((left_up_point[0] + right_up_point[0])/2), int((left_up_point[1] + right_up_point[1])/2)) 
target_center_bottom = (int((left_down_point[0] + right_down_point[0])/2), int((left_down_point[1] + right_down_point[1])/2))
target_center = (int((left_up_point[0] + right_down_point[0])/2), int((left_up_point[1] + right_down_point[1])/2))
cv2.line(src, target_center_top, target_center_bottom, function.yellow, 2)
cv2.circle(src, target_center, 3, function.yellow, -1)


# 사각형만큼 따오기
mask = np.zeros(src.shape, dtype="uint8")
cv2.line(mask, left_up_point, right_up_point, function.yellow, 2)
cv2.line(mask, left_up_point, left_down_point, function.yellow, 2)
cv2.line(mask, left_down_point, right_down_point, function.yellow, 2)
cv2.line(mask, right_up_point, right_down_point, function.yellow, 2)

mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
_, mask_binary = cv2.threshold(mask, 100, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(mask_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for i in range(len(contours)):
    cv2.drawContours(mask_binary, [contours[i]], 0, (255,255,255), -1)

mask_binary = cv2.merge((mask_binary, mask_binary, mask_binary))
target_rect = cv2.bitwise_and(mask_binary, img) # 같은차원이어야 bitwise되는듯

# 안에거 검출
target_rect = cv2.cvtColor(target_rect, cv2.COLOR_BGR2GRAY)
_, target_rect = cv2.threshold(target_rect, 110, 255, cv2.THRESH_BINARY)
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5,5))
target_rect = cv2.morphologyEx(target_rect, cv2.MORPH_CLOSE, kernel, iterations= 1)
target_rect = cv2.morphologyEx(target_rect, cv2.MORPH_OPEN, kernel, iterations= 3)

contours, hierarchy = cv2.findContours(target_rect, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cX_right = []
cY_right = []
cX_left = []
cY_left = []
for i in range(len(contours)):
    moment = cv2.moments(contours[i])
    cX = int(moment["m10"] / (moment["m00"] + 1e-5))
    cY = int(moment["m01"] / (moment["m00"] + 1e-5))
    length = point_to_line((cX, cY), target_center_bottom, target_center_top)
    area = cv2.contourArea(contours[i])
    cv2.drawContours(img, [contours[i]], 0, function.black, -1)
    if length < 150:
        cv2.drawContours(src, [contours[i]], 0, function.green, 2)
        
        #cv2.circle(src, (cX,cY), 3, function.red, -1)
        #print(length)
        if length < 110 and area > 500:    
            if cX < target_center[0]:
                cX_left.append(cX)
                cY_left.append(cY)
            else:
                cX_right.append(cX)
                cY_right.append(cY)

cX_check = []
for i in range(len(cX_left)-1): 
    cX_check.append(point_to_point(cX_left[i], cY_left[i], cX_left[i+1], cY_left[i+1]))
    print("cX_left["+str(i)+"] and cX_left["+str(i+1)+"] and ",  cX_check[i])

left_count = 1 
check = copy.deepcopy(cY_left)
check.sort()
for i in range(len(cY_left)):
    index = cY_left.index(check[i])
    cX, cY = cX_left[index], cY_left[index]
    cv2.putText(src, str(left_count), (cX +20, cY +10), cv2.FONT_HERSHEY_COMPLEX, 1, function.green, 2)
    left_count += 1
first = (cX_left[cY_left.index(check[0])] -10, cY_left[cY_left.index(check[0])])
last = (cX_left[cY_left.index(check[-1])] -10, cY_left[cY_left.index(check[-1])])
left_boundary = [first, last] # 경계잡기
cv2.line(src, first, last, function.red, 2) 

check = copy.deepcopy(cY_right)
check.sort()
right_count = left_count
for i in range(len(cY_right)):
    index = cY_right.index(check[i])
    cX, cY = cX_right[index], cY_right[index]
    cv2.putText(src, str(right_count), (cX -55, cY +10), cv2.FONT_HERSHEY_COMPLEX, 1, function.green, 2)
    right_count += 1

first = (cX_right[cY_right.index(check[0])] +10, cY_right[cY_right.index(check[0])])
last = (cX_right[cY_right.index(check[-1])] +10, cY_right[cY_right.index(check[-1])])
first_boundary = [first, last] # 경계잡기
cv2.line(src, first, last, function.red, 2) 





target_rect = function.FitToWindowSize(target_rect)
cv2.imshow("target_rect", target_rect)

src = function.FitToWindowSize(src) 
cv2.imshow("src", src)




cv2.waitKey(0)
cv2.destroyAllWindows()