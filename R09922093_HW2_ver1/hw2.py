import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageDraw

im = Image.open('lena.bmp', 'r')
width, height = im.size
new = Image.new("L",(width,height))
print(im.size)

def binarize(threshold):
	for i in range(width):
			for j in range(height):
				pixel = im.getpixel((i, j))
				if pixel < threshold:
					new.putpixel((i, j), 0)
				else:
					new.putpixel((i, j), 255)
	new.save("binarize.bmp")

im = Image.open('lena.bmp', 'r')
def histogram(im):
	width, height = im.size
	pixel_values = list(im.getdata())
	plt.figure(figsize=(10,7))
	plt.hist(pixel_values,range(0,255), color = "black")
	plt.savefig("plt.jpg")
# new = Image.open('binarize.bmp', 'r')
current = 0
label = np.zeros((width,height))
pairs = {}
def connect(i, j):
	pixel_values = new.getpixel((i, j))
	if(i -1 < 0) :
		if(j - 1 < 0):
			return -1
		elif(new.getpixel((i, j-1))== pixel_values):
			return label[i][j-1]
		else:
			return -1
	elif(j - 1 < 0):
		if (new.getpixel((i-1, j))== pixel_values):
			return label[i-1][j]
		else:
			return -1
	else:
		if(new.getpixel((i-1, j))!= pixel_values and new.getpixel((i, j-1)) != pixel_values):
			return -1
		elif(new.getpixel((i-1, j)) != pixel_values and new.getpixel((i, j-1)) == pixel_values):
			return label[i][j-1]
		elif(new.getpixel((i-1, j)) == pixel_values and new.getpixel((i, j-1)) != pixel_values):
			return label[i-1][j]
		else:
			maxx = max(label[i][j-1],label[i-1][j])
			minn = min(label[i][j-1],label[i-1][j])
			if maxx == minn:
				return minn
			else:
				pairs[maxx] = minn 
				return minn
def check(i, j):
	pixel_values = new.getpixel((i, j))
	if(i + 1 > width-1 and j + 1 < height and new.getpixel((i, j+1)) == pixel_values):
		label[i][j] = label[i][j+1]
	elif(i + 1 < width and j + 1 > height-1 and new.getpixel((i+1, j)) == pixel_values):
		label[i][j] = label[i + 1][j]
	elif(i+1 < width and j+1 < height):
		if (new.getpixel((i, j+1))!= pixel_values and new.getpixel((i+1, j)) == pixel_values):
			label[i][j] = label[i+1][j]
		elif (new.getpixel((i, j+1)) == pixel_values and new.getpixel((i+1, j)) != pixel_values):
			label[i][j] = label[i][j+1]
		elif (new.getpixel((i, j+1)) == pixel_values and new.getpixel((i+1, j)) == pixel_values):
			maxx = max(label[i+1][j],label[i][j+1])
			minn = min(label[i+1][j],label[i][j+1])
			label[i][j] = minn
			if maxx!=minn:
				pairs[maxx] = minn
def findbound(key, value):
	mid_i= 0
	mid_j= 0

	draw = ImageDraw.Draw(bound)
	boundaries = [511, 511, 0, 0]
	for j in range(height):
		for i in range(width):
			if label[i][j] == key:
				if i > boundaries[2]:
					boundaries[2] = i
				if i < boundaries[0]:
					boundaries[0] = i
				if j > boundaries[3]:
					boundaries[3] = j
				if j < boundaries[1]:
					boundaries[1] = j
	# print(boundaries[0], boundaries[2], boundaries[1], boundaries[3])
	for i in range(boundaries[0], boundaries[2]+1):
		for j in range(boundaries[1], boundaries[3]+1):
			if(label[i, j] == key):
				mid_i += i
				mid_j += j
	mid_i = mid_i // value
	mid_j = mid_j // value
	draw.rectangle(boundaries, outline='GREEN',width = 3)
	draw.line((mid_i,mid_j-5,mid_i,mid_j+5),fill="RED", width = 3)
	draw.line((mid_i-5,mid_j,mid_i+5,mid_j),fill="RED", width = 3)

##binarize
threshold = 128
binarize(threshold)
for i in range(width):
	for j in range(height):
		if (new.getpixel((i, j)) != 0 and new.getpixel((i, j))!= 255):
			print("ERROR!")
##histogram
histogram(im)

##connected_compnent
bound = new.convert("RGB")

for j in range(height):
	for i in range(width):
		if(new.getpixel((i, j))== 255):
			connected = connect(i, j)
			if(connected == -1):
				current += 1
				label[i][j] = current
			else:
				label[i][j] = connected
	if(len(pairs) > 0):
		for i in range(width):
			if (pairs. __contains__(label[i][j])):
				label[i][j] = pairs.get(label[i][j])
	pairs.clear()

for j in range(height):
	for i in range(width):
		if(new.getpixel((width-i-1, height-j-1))) == 255:
			check(width-i-1, height-j-1)
	if (len(pairs) > 0):
		for i in range(width):
			if (pairs. __contains__(label[width-i-1][height-j-1])):
				label[width-i-1][height-j-1] = pairs.get(label[width-i-1][height-j-1])
	pairs.clear()

unique, count = np.unique(label, return_counts=True)
component = dict(zip(unique, count))
for key,value in component.items():
	if value >= 500 and key != 0:
		findbound(key, value)
bound.save("conected_component.bmp")
