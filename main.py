import glob
import json
from random import randrange, random
import shutil
from unicodedata import name
import imagehash
from PIL import Image, ImageFont, ImageDraw
import math
import time
import os
import sys



folderPath = {
    "GIF": './gif',
    "TEMP": './temp',
    "RENDER": './render'
}

# input dimensions should be 600x600
sourceImg = "blury_tree.jpg"

# how many filter should be appended ?
# your value times 5 , 2 means 5*2=10
# the highest value in this case can be 10, the lowest 1
iterationScale = 1

# how many images should be created ?
countImg = 10

#select your effect list
effectListName="test.txt"

# JSON log ?
logToJson = False

# Draws the cards border with informations
drawInfo = True
drawInfoText = True
# if true, the previous image (with filters applied) will be rendered
# 1.png ==> FILTERS ==> 2.png
# if false, the src image will be rendered with filters
# src.png ==> FILTERS ==> 1.png
generateRecursive = False
# creates a gif with all images in the selected folder
createGif = False
# creates a .zip folder
createZip = False


def readFileAsList(fileName):
    text_file = open(r"./effect/"+fileName, "r")
    lines = text_file.readlines()
    text_file.close()
    sanitizedList =[]
    for line in lines:
        if "\n" in line:
            sanitizedString=" "+line[:-1]
        else:
            sanitizedString=line
        sanitizedList.append(sanitizedString.rjust(10))
    return sanitizedList



filterList=[]
filterList=readFileAsList(effectListName)

print(filterList)

# exit()


def make_archive(outname,inname):
    shutil.make_archive(outname, 'zip', inname)



def clearFolder(path):
    for file in os.listdir(path):
        if file.endswith('.png'):
            filePath = path+'/'+file
            if os.path.exists(filePath):
                os.remove(filePath)


clearFolder(folderPath["RENDER"])
clearFolder(folderPath["TEMP"])
print("cleared folders")


# returns the color for the background according to the rarerity of the image
def rareColor(i):
    switcher = {
        1: 'black',
        2: 'green',
        3: 'blue',
        4: 'purple',
        5: 'gold'
    }
    return switcher.get(i, "black")


jsonList = []


def createGIF(path,gifName):

    print("creating gif")
    frames = [Image.open(f) for f in sorted(glob.glob(f"{path}/*.png"))]
    frame_one = Image.open(sourceImg)
    frame_one.save(fp='./gif/{n}.gif'.format(n=gifName), format='GIF', append_images=frames,
                   save_all=True, duration=200, loop=0)
    print("finished gif")


def dumpToJson(list):
    jsonFile = open("json/data.json", "w")
    jsonFile.write(json.dumps(list))
    jsonFile.close()


tStartAll = time.time()
print("Starting loop, this could take a long time ")
# START creation loop


def gmicCreate(inImg, fileName, filter):
    os.system(
        "gmic {ing} {fil} output temp/{outg}".format(ing=inImg, fil=filter, outg=fileName))


countImgRender = 1

for images in range(countImg):

    fileName = ""
    filterArray = ""
    filterCount = randrange(1, 5*iterationScale, 1)
    rarity = math.ceil(filterCount/iterationScale)

    for x in range(filterCount):
        filterArray = filterArray + \
            str(filterList[randrange(0, len(filterList))])

    fileName = ''.join(str(images+1)+".png")

    tStartSingle = time.time()

    imageToRender = sourceImg

    if(generateRecursive):
        print("rekursive")
        if(countImgRender > 2):
            prevImage = './temp/'+str(countImgRender-1)+".png"
            if os.path.exists(prevImage):
                imageToRender = prevImage

    print("starting image no: "+fileName +
          " \n count filter : "+str(filterCount) +
          "\n src image" + imageToRender)

    gmicCreate(imageToRender, fileName, filterArray)
    countImgRender = countImgRender + 1

    try:
        img = Image.open("./temp/"+fileName).convert("RGB")
        img = img.resize((600, 600), Image.ANTIALIAS)
        if drawInfo:
            width, height = img.size
            font_size = 20
            # TODO Does not work in docker container

            
            isdockerfile = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)

            fontLocation="./font/Ubuntu-M.ttf"
            # if isdockerfile:
            # else:
            #     fontLocation ="usr/share/fonts/truetype/ubuntu/UbuntuMono-B.ttf"

            font = ImageFont.truetype(
              fontLocation, font_size, encoding="unic")

            imgHash = imagehash.whash(img)
            fillCol = rareColor(rarity)
            draw = ImageDraw.Draw(img)

            draw.line((0, 0, 0, height), fill=fillCol, width=100)
            draw.line((width, 0, width, height), fill=fillCol, width=100)
            draw.rectangle(((0, 0), (width, 50)), fill=fillCol)
            draw.rectangle(((0, height), (width, height-150)), fill=fillCol)
            if(drawInfoText):
                draw.text((40, height-120), "Number: " +
                          str(images+1), font=font, fill='white')
                draw.text((40, height-100), "Rarity: " +
                          str(rarity), font=font, fill='white')
                draw.text((40, height-80), "Hash: " +
                          str(imgHash), font=font, fill='white')
                draw.text((40, height-60), "Filter: " +
                          str(filterCount), font=font, fill='white')

        
        try:
            img.save("render/"+fileName, quality=100)
        except IOError:
            print ("cannot save  {s}".format(s=fileName))

        if(logToJson):
            jsonList.append({"number": images+1, "fName": fileName,
                             "iterations": rarity, "effects": filterArray, "rarity": rarity, "hash": str(imgHash)})
        countImgRender += 1
        outText = "\n succsess at image index: {img} ".format(
            img=str(images+1))
    except IOError:
        tb = sys.exc_info()[2]
        outText = "\n error at image index: {img} {tb}".format(img=str(images+1),err=tb)
    tEndSingle = time.time()
    print(
        outText+" elapsed time: {time} seconds".format(time=str(round(tEndSingle-tStartSingle))))


if logToJson:
    dumpToJson(jsonList)

tEndAll = time.time()

print("\n finished! rendered "+str(countImgRender-1) +
      " pictures in " + str(round(tEndAll-tStartAll))+" seconds")

if(createGif):
    createGIF(folderPath["RENDER"],"render")
    createGIF(folderPath["TEMP"],"temp")

if(createZip):
    make_archive("full_temp",folderPath["TEMP"])
    make_archive("full_render",folderPath["RENDER"])
