import cv2

##upsdie down 
def upsidedown(image):
	lena = image.copy()
	for i in range(lena.shape[0]//2):
		for j in range(lena.shape[1]):
			a = lena[i,j].copy()
			lena[i, j] = lena[lena.shape[0] - i - 1, j]
			lena[lena.shape[0] - i - 1, j] = a
	cv2.imwrite("upside-down lena.bmp",lena)
##right-left
def rightsideleft(image):
	lena = image.copy()
	for i in range(lena.shape[0]):
		for j in range(lena.shape[1]//2):
			a = lena[i,j].copy()
			lena[i, j] = lena[i, lena.shape[1] - j - 1]
			lena[i, lena.shape[1] - j -1] = a
	cv2.imwrite("right-side-left lena.bmp",lena)
##diagonal
def diagonallyflip(image):
	lena = image.copy()
	for i in range(lena.shape[0]):
		for j in range(i):
			a = lena[i,j].copy()
			lena[i, j] = lena[j,i]
			lena[j,i] = a
	cv2.imwrite("diagonally flip lena.bmp",lena)

image = cv2.imread('lena.bmp')
upsidedown(image)
rightsideleft(image)
diagonallyflip(image)