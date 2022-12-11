import copy
import math
import random
from os import listdir
from os.path import isfile, join

import numpy as np
import pyautogui
import cv2


def chooseSetup():
    print("Choose Option:")
    print("1: Setup Fresh File")
    print("2: Choose Prev Setup")
    inputVal = input("Enter: ")
    fileName = ""
    if inputVal == "1":
        print()
        fileName = input("Enter File Name: \n")
        with open('./SetupFiles/' + fileName + '.txt', 'w') as f:
            print("Move Cursor to Top Left")
            input("Press Enter to continue...")
            x, y = pyautogui.position()
            f.write(str(x) + ' ' + str(y) + '\n')
            print("Move Cursor to Bot Right")
            input("Press Enter to continue...")
            x, y = pyautogui.position()
            f.write(str(x) + ' ' + str(y) + '\n')
    elif inputVal == "2":
        print('\nFiles:')
        onlyfiles = [f for f in listdir("./SetupFiles") if isfile(join("./SetupFiles", f))]
        count = 1
        for file in onlyfiles:
            print(str(count) + ': ' + file)
            count = count + 1
        chosenFile = input("Choose File Number: \n")
        fileName = onlyfiles[int(chosenFile) - 1]

    return fileName


def readSetup(fileName):
    with open('./SetupFiles/' + fileName, 'r') as f:
        lines = f.readlines()

    x_1, y_1 = lines[0].strip('\n').split(' ')
    x_1 = int(x_1)
    y_1 = int(y_1)

    x_2, y_2 = lines[1].strip('\n').split(' ')
    x_2 = int(x_2)
    y_2 = int(y_2)

    return x_1, y_1, x_2, y_2


def readImage():
    print('\nFiles:')
    onlyfiles = [f for f in listdir("./Portraits") if isfile(join("./Portraits", f))]
    count = 1
    for file in onlyfiles:
        print(str(count) + ': ' + file)
        count = count + 1
    chosenFile = input("Choose File Number: \n")
    fileName = onlyfiles[int(chosenFile) - 1]
    img = cv2.imread("./Portraits/" + fileName)
    return img


def readImageResult():
    print('\nFiles:')
    onlyfiles = [f for f in listdir("./Results") if isfile(join("./Results", f))]
    count = 1
    for file in onlyfiles:
        print(str(count) + ': ' + file)
        count = count + 1
    chosenFile = input("Choose File Number: \n")
    fileName = onlyfiles[int(chosenFile) - 1]
    img = cv2.imread("./Results/" + fileName)
    return img, fileName


def scale(img, xCanvas, yCanvas):
    x, y, z = img.shape

    xScale = 1
    if x > xCanvas:
        print()
        xScale = xCanvas / x

    yScale = 1
    if y > yCanvas:
        yScale = yCanvas / y

    print('\nX Scale: ' + str(xCanvas) + '/' + str(x) + ' = ' + str(xScale))
    print('\nY Scale: ' + str(yCanvas) + '/' + str(y) + ' = ' + str(yScale))

    return xScale, yScale


def drawX(x, y):
    pyautogui.moveTo(x + 2, y + 2)
    pyautogui.dragTo(x - 2, y - 2)
    pyautogui.moveTo(x - 2, y + 2)
    pyautogui.dragTo(x + 2, y - 2)


def getInstances(grayImage):
    gray_vals = {}
    for row in grayImage:
        unique, counts = np.unique(row, return_counts=True)

        for i in range(len(unique)):
            gray_vals[unique[i]] = gray_vals.get(unique[i], 0) + counts[i]

    return gray_vals


def makeBuckets(vals, bucketSize):
    keyList = list(vals.keys())
    keyList.sort()

    count = 1
    bucketRange = {}
    for key in keyList:
        if key > bucketSize * count:
            count = count + 1
        vals[key] = count

        if bucketRange.get(count) is None:
            bucketRange[count] = [key]
        else:
            lsit = bucketRange.get(count)
            lsit.append(key)
            bucketRange[count] = lsit

    unique, counts = np.unique(list(vals.values()), return_counts=True)

    valCount = {}
    for i in range(len(unique)):
        valCount[unique[i]] = valCount.get(unique[i], 0) + counts[i]

    return vals, valCount, bucketRange


def dictLocs(gray_vals):
    dictLocs = {}
    for i, row in enumerate(gray_vals):
        for j, col in enumerate(row):
            loc = (i, j)
            if dictLocs.get(col) is None:
                dictLocs[col] = [loc]
            else:
                lsit = dictLocs.get(col)
                lsit.append(loc)
                dictLocs[col] = lsit
    return dictLocs


def cutResultToImage():
    image = readImage()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height = image.shape[0]
    width = image.shape[1]

    print('Image Height       : ', height)
    print('Image Width        : ', width)
    print(type(image))

    resultImage, fileName = readImageResult()
    resultImage = cv2.cvtColor(resultImage, cv2.COLOR_BGR2GRAY)
    heightResult = resultImage.shape[0]
    widthResult = resultImage.shape[1]

    print('Result Image Shape       : ', resultImage.shape)
    print('Result Image Height       : ', heightResult)
    print('Result Image Width        : ', widthResult)

    newResult = resultImage[:height, :width]
    newheightResult = resultImage.shape[0]
    newwidthResult = resultImage.shape[1]

    print('New Result Image Shape       : ', newResult.shape)
    print('New Result Image Height       : ', newheightResult)
    print('New Result Image Width        : ', newwidthResult)

    cv2.imshow('image', newResult)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print("Save Cut Image (y/n):")
    inputStr = input()

    if inputStr == 'y':
        cv2.imwrite('./Results/' + fileName, newResult)
    else:
        print("Not Saving Cut Image")


def drawCrossHatching():
    filename = chooseSetup()
    x1, y1, x2, y2 = readSetup(filename)
    image = readImage()
    xScaleFactor, yScaleFactor = scale(image, x2 - x1, y2 - y1)

    # cv2.imshow('image', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # cv2.imshow('image', gray_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #
    # gray_image2 = gray_image + 10
    #
    # cv2.imshow('image', gray_image2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    print(gray_image)

    height = gray_image.shape[0]
    width = gray_image.shape[1]

    print('Image Dimension    : ', gray_image.shape)
    print('Image Height       : ', height)
    print('Image Width        : ', width)

    drawX((x2 + x1) / 2, (y2 + y1) / 2)

    gray_instances = getInstances(gray_image)

    grayValLocs = dictLocs(gray_image)

    bucket_instances, bucket_count, bucket_range = makeBuckets(copy.deepcopy(gray_instances), 25)

    print("Gray Instances:")
    print(gray_instances)

    # print("Gray Val Locs:")
    # print(grayValLocs)

    print("Bucket Instances:")
    print(bucket_instances)

    print("Bucket Count:")
    print(bucket_count)

    print("Bucket Range:")
    print(bucket_range)

    iter = 1000
    numBuckets = len(bucket_count.keys())
    currBucket = 1

    for a in range(iter):
        print('Count: ' + str(a))
        if a == iter / numBuckets * currBucket:
            currBucket = currBucket + 1

        valList = bucket_range.get(currBucket)

        grayValToDraw = valList[random.randint(0, len(valList) - 1)]

        locList = grayValLocs.get(grayValToDraw)
        grayLocToDraw = locList[random.randint(0, len(locList) - 1)]

        print("Gray Val: " + str(grayValToDraw) + ", Drawing " + str(round((pow(math.e, (
                len(bucket_count.keys()) - bucket_instances.get(
            grayValToDraw)) / 3) / 2) + 1)) + " X from bucket: " + str(
            bucket_instances.get(grayValToDraw)) + " at loc: (" + str(grayLocToDraw[0] + x1) + "," + str(
            grayLocToDraw[1] + y1) + ")")

        xToDraw = round((pow(math.e, (len(bucket_count.keys()) - bucket_instances.get(grayValToDraw)) / 3) / 2) + 1)

        for b in range(xToDraw):
            drawX(grayLocToDraw[1] + x1 + random.randint(-5, 5), grayLocToDraw[0] + y1 + random.randint(-5, 5))


if __name__ == '__main__':
    # drawCrossHatching()
    cutResultToImage()
