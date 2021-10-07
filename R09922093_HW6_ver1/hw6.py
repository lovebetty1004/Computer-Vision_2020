import cv2
import numpy as np 

lena = cv2.imread('lena.bmp', 0)
down_row = lena.shape[0]//8
down_column = lena.shape[1]//8
print(down_row, down_column)
down_sampling = np.full((down_row,down_column),0)
for i in range (down_row):
    for j in range (down_column):
        down_sampling[i][j] = lena[8 * i][8 * j]
        if down_sampling[i][j] < 128:
            down_sampling[i][j] = 0
        else :
            down_sampling[i][j] = 255

cv2.imwrite("down_sample.bmp",down_sampling)
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

yokoi = np.full((down_row,down_column),0)
for i in range (down_row):
    for j in range (down_column):
        if down_sampling[i][j] == 0:
            continue
        a = h(i,j,1,6,2)
        b = h(i,j,2,7,3)
        c = h(i,j,3,8,4)
        d = h(i,j,4,5,1)
        yokoi[i][j] = f(a, b, c, d)
        if yokoi[i][j] == 0:
            continue
        else:
            addnumber_to_photo(result, i, j , yokoi[i][j])
cv2.imwrite("yokoi.bmp", result)