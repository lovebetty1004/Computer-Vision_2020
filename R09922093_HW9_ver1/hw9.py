import cv2
import numpy as np
# import math
lena = cv2.imread("lena.bmp", 0)
lena_img = cv2.copyMakeBorder(lena,1,1,1,1,cv2.BORDER_REFLECT)
lena_img2 = cv2.copyMakeBorder(lena,2,2,2,2,cv2.BORDER_REFLECT)
def mask(image, i, j, kernel):
	result = 0
	for k in range(kernel.shape[0]):
		for l in range(kernel.shape[1]):
			result += image[i+k][j+l] * kernel[k][l]
	return result
r1 = np.array([[-1, 0],[0, 1]])
r2 = np.array([[0, -1],[1, 0]])
p1 = np.array([[-1, -1, -1],[ 0,  0,  0],[ 1,  1,  1]])
p2 = np.array([[-1,  0,  1],[-1,  0,  1],[-1,  0,  1]])
s1 = np.array([[-1, -2, -1],[ 0,  0,  0],[ 1,  2,  1]])
s2 = np.array([[-1,  0,  1],[-2,  0,  2],[-1,  0,  1]])
fc1 = np.array([[-1, -1*np.sqrt(2), -1],[ 0,  0,  0],[ 1,  np.sqrt(2),  1]])
fc2 = np.array([[-1,  0,  1],[-1*np.sqrt(2),  0,  np.sqrt(2)],[-1,  0,  1]])
def Edgedetector(image, threshold, array1, array2):
	resultimg = np.full((512, 512),255)
	for i in range(512):
		for j in range(512):
			value = mask(image, i, j, array1)**2 + mask(image, i, j, array2)**2
			if value > threshold*threshold:
				resultimg[i][j] = 0
			else: 
				resultimg[i][j] = 255
	return resultimg
robert_12 = Edgedetector(lena_img, 12, r1, r2)
cv2.imwrite("Robert_12.bmp", robert_12)
prewitt_24 = Edgedetector(lena_img, 24, p1, p2)
cv2.imwrite("Prewitt_24.bmp", prewitt_24)
sobel_38 = Edgedetector(lena_img, 38, s1, s2)
cv2.imwrite("sobel_38.bmp", sobel_38)
fc_30 = Edgedetector(lena_img, 30, fc1, fc2)
cv2.imwrite("FreiChen_30.bmp", fc_30)
k0 = np.array([[-3, -3,  5], [-3,  0,  5], [-3, -3,  5]])
k1 = np.array([[-3,  5,  5], [-3,  0,  5], [-3, -3, -3]])
k2 = np.array([[ 5,  5,  5], [-3,  0, -3], [-3, -3, -3]])
k3 = np.array([[ 5,  5, -3], [ 5,  0, -3], [-3, -3, -3]])
k4 = np.array([[ 5, -3, -3], [ 5,  0, -3], [ 5, -3, -3]])
k5 = np.array([[-3, -3, -3], [ 5,  0, -3], [ 5,  5, -3]])
k6 = np.array([[-3, -3, -3], [-3,  0, -3], [ 5,  5,  5]])
k7 = np.array([[-3, -3, -3], [-3,  0,  5], [-3,  5,  5]])
ks = [k0, k1, k2, k3, k4, k5, k6, k7]
R0 = np.array([[-1,  0,  1], [-2,  0,  2], [-1,  0,  1]])
R1 = np.array([[ 0,  1,  2], [-1,  0,  1], [-2, -1,  0]])
R2 = np.array([[ 1,  2,  1], [ 0,  0,  0], [-1, -2, -1]])
R3 = np.array([[ 2,  1,  0], [ 1,  0, -1], [ 0, -1, -2]])
R4 = np.array([[ 1,  0, -1], [ 2,  0, -2], [ 1,  0, -1]])
R5 = np.array([[ 0, -1, -2], [ 1,  0, -1], [ 2,  1,  0]])
R6 = np.array([[-1, -2, -1], [ 0,  0,  0], [ 1,  2,  1]])
R7 = np.array([[-2, -1,  0], [-1,  0,  1], [ 0,  1,  2]])
Rs = [R0, R1, R2, R3, R4, R5, R6, R7]
N0 = np.array([[ 100, 100, 100, 100, 100],
                [ 100, 100, 100, 100, 100],
                [   0,   0,   0,   0,   0],
                [-100,-100,-100,-100,-100],
                [-100,-100,-100,-100,-100]])

N1 = np.array([[ 100, 100, 100, 100, 100],
                [ 100, 100, 100,  78, -32],
                [ 100,  92,   0, -92,-100],
                [  32, -78,-100,-100,-100],
                [-100,-100,-100,-100,-100]])

N2 = np.array([[ 100, 100, 100,  32,-100],
                [ 100, 100,  92, -78,-100],
                [ 100, 100,   0,-100,-100],
                [ 100,  78, -92,-100,-100],
                [ 100, -32,-100,-100,-100]])

N3 = np.array([[-100,-100,   0, 100, 100],
                 [-100,-100,   0, 100, 100],
                 [-100,-100,   0, 100, 100],
                 [-100,-100,   0, 100, 100],
                 [-100,-100,   0, 100, 100]])

N4 = np.array([[-100,  32, 100, 100, 100],
                 [-100, -78,  92, 100, 100],
                 [-100,-100,   0, 100, 100],
                 [-100,-100, -92,  78, 100],
                 [-100,-100,-100, -32, 100]])

N5 = np.array([[ 100, 100, 100, 100, 100],
                 [ -32,  78, 100, 100, 100],
                 [-100, -92,   0,  92, 100],
                 [-100,-100,-100, -78,  32],
                 [-100,-100,-100,-100,-100]])
Ns = [N0, N1, N2, N3, N4, N5]
def Compass(image, threshold, arraylist):
	resultimg = np.full((512, 512),255)
	for i in range(512):
		for j in range(512):
			valuelist = []
			for k in range(len(arraylist)):
				valuelist.append(mask(image, i, j, arraylist[k]))
			value = max(valuelist)
			# print(value)
			if value > threshold:
				resultimg[i][j] = 0
			else: 
				resultimg[i][j] = 255
	return resultimg
Kirsch_135 = Compass(lena_img, 135, ks)
cv2.imwrite("Kirsch_135.bmp", Kirsch_135)
Robinson_43 = Compass(lena_img, 43, Rs)
cv2.imwrite("Robinson_43.bmp", Robinson_43)
Nevatia_Babu_12500 = Compass(lena_img2, 12500, Ns)
cv2.imwrite("Nevatia_Babu_12500.bmp", Nevatia_Babu_12500)