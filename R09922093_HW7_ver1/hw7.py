import cv2
import numpy as np 

def downsample(image) :
    d_row = image.shape[0]//8
    d_column = image.shape[1]//8
    for i in range (d_row):
        for j in range (d_column):
            down_sampling[i][j] = image[8 * i][8 * j]
            if down_sampling[i][j] < 128:
                down_sampling[i][j] = 0
            else :
                down_sampling[i][j] = 255
    return d_row,d_column, down_sampling

lena = cv2.imread('lena.bmp', 0)
down_sampling= np.full((lena.shape[0]//8,lena.shape[1]//8),0)
down_row, down_column, down_sampling = downsample(lena)
cv2.imwrite("down_sample.bmp",down_sampling)

mark = np.full((down_row, down_column),0)
def getvalue(i,j,check):
    if check == 1:
        if j+1 >= down_column:
            return 0
        else:
            return down_sampling[i][j+1]
    elif check == 2:
        if i-1 < 0:
            return 0
        else: 
            return down_sampling[i-1][j]
    elif check == 3:
        if j-1 < 0:
            return 0
        else:
            return down_sampling[i][j-1]
    elif check == 4:
        if i+1 >= down_row:
            return 0
        else:
            return down_sampling[i+1][j]
    elif check == 5:
        if i+1 >= down_row or j+1 >= down_column:
            return 0
        else:
            return down_sampling[i+1][j+1]
    elif check == 6:
        if i-1 < 0 or j+1 >= down_column:
            return 0
        else:
            return down_sampling[i-1][j+1]
    elif check == 7:
        if i-1 < 0 or j-1 < 0:
            return 0
        else:
            return down_sampling[i-1][j-1]
    elif check == 8:
        if i+1 >= down_row or j-1 < 0:
            return 0
        else:
            return down_sampling[i+1][j-1]
        
def h(i,j,p1,p2,p3):
    v_0 = down_sampling[i][j]
    v_1 = getvalue(i,j,p1)
    v_2 = getvalue(i,j,p2)
    v_3 = getvalue(i,j,p3)
    if v_0 != v_1:
        return 2
    elif v_0 == v_2 and v_0 == v_3:
        return 1
    else:
        return 0
        
def f(a,b,c,d):
    if a==b and b==c and c==d and d == 1:
        return 5
    cnt = 0
    if a == 0:
        cnt+=1
    if b == 0:
        cnt+=1
    if c == 0:
        cnt+=1
    if d == 0:
        cnt+=1
    return cnt

def addnumber_to_photo(image, row, column, number):
	txt = str(number)
	x = column * 15
	y = (row +1 ) * 15
	cv2.putText(image, txt, (x,y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, 0, 1, cv2.LINE_AA)

result = np.zeros((64*15 + 15//2, 64 * 15), np.uint8)
result.fill(255)

def yokoi_connectivity(time):
    for i in range (down_row):
        for j in range (down_column):
            if down_sampling[i][j] == 0:
                yokoi_result[i][j] == 0
                continue
            else:
                a = h(i,j,1,6,2)
                b = h(i,j,2,7,3)
                c = h(i,j,3,8,4)
                d = h(i,j,4,5,1)
                yokoi_result[i][j] = f(a, b, c, d)
                addnumber_to_photo(result, i, j, yokoi_result[i][j])
def pair_relation(i, j):
    if i+1 < down_row:
        if yokoi_result[i+1][j] == 1: 
            return 1
    if i-1 >= 0:
        if yokoi_result[i-1][j] == 1: 
            return 1
    if j+1 < down_column:
        if yokoi_result[i][j+1] == 1: 
            return 1
    if j-1 >= 0:
        if yokoi_result[i][j-1] == 1: 
            return 1
    return 0

def thining_mark():
    for i in range (down_row):
        for j in range (down_column):
            if yokoi_result[i][j] == 0:
                thining[i][j] = 0
            elif yokoi_result[i][j] == 1 and pair_relation(i,j) == 1:
                thining[i][j] = 1
            else:
                thining[i][j] = -1

def h_shrink(i,j,p1,p2,p3):
    v_0 = down_sampling[i][j]
    v_1 = getvalue(i,j,p1)
    v_2 = getvalue(i,j,p2)
    v_3 = getvalue(i,j,p3)
    if v_0 == v_1:
        if v_0 != v_2 or v_0 != v_3:
            return 1
    return 0

def f_shrink(i, j, a,b,c,d):
    if a+b+c+d == 1: 
        return 0
    else:
        return down_sampling[i][j]
yokoi_result = np.full((down_row,down_column),0)
thining = np.full((down_row, down_column),0)
for time in range(7):
    yokoi_result = np.full((down_row,down_column),0)
    yokoi_connectivity(time)
    thining = np.full((down_row, down_column),0)
    thining_mark()
    for i in range (down_row):
        for j in range (down_column):      
            if thining[i][j] == 1:
                a = h_shrink(i,j,1,6,2)
                b = h_shrink(i,j,2,7,3)
                c = h_shrink(i,j,3,8,4)
                d = h_shrink(i,j,4,5,1)
                down_sampling[i][j] = f_shrink(i, j, a, b, c, d)
cv2.imwrite("thining_result.bmp", down_sampling)