import glob
import json
from random import randrange, random
from unicodedata import name
import imagehash
from PIL import Image , ImageFont , ImageDraw
import math
import time
import os
import sys

from pyparsing import line


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


# JSON log ?
logToJson = False

# Draws the cards border with informations
drawInfo = True
drawInfoText = True
# if true, the previous image (with filters applied) will be rendered
# 1.png ==> FILTERS ==> 2.png
# if false, the src image will be rendered with filters
# src.png ==> FILTERS ==> 1.png
generateRecursive = True
# creates a gif with all images in the selected folder
createGif = True





# Filter used
pWhearl = " fx_whirls 20,3.88,0.2,1.672,11,0,50,50"
pBlurAngular = " fx_blur_angular 0.52,50,50,3.5,1,7,0"
pRodilus = " rodilius 10"
pDots = " fx_polka_dots 18.1,16.28,50,50,0,0.5,0.1,1,255,255,255,255"
pBW = " fx_blackandwhite 0.299,0,0.587,0,0.114,0,0,0,0,0,0,0,0,0,2,0,0,0,16,4,0,0,0,50,50"
pSegment = " fx_segment_watershed 2,1,0,0,0,50,50"
pTwirl = " fx_twirl -0.22,50,50,3"
pDirty = " fx_dirty 30,1,0,0,0,50,50"
pPixelSort = " fx_pixelsort 1,0,0,1,0,66.2,0,0,0"
pOverlayBC = " frame_cube 28.98,0,0,0,0,0,0"
pPolaRoid = " fx_polaroid 10,20,0,0,3,0,0,50,70,95"
pHope2020 = " fx_poster_hope -0.174,3,0,50,50"
pScanLines = " fx_marble 4.74,1,0,0,0.4,0.054,7.24,1.1,0,100"
pSponge = " fx_sponge 9,0,0,50,50"
pKorb = " weave 14,50.5,0,0.5,0,0,0,0,0"
pWarp = " fx_warp_by_intensity 1.104,-0.708,128,128,0,0,3,0,0,50,50"
pFractal = " fractalize 0.8"
pPloy = " fx_polygonize 2000,85.7,10,10,10,0,0,0,255,0,50,50"
pBitCrush = " fx_8bits 25,800,16,0,50,50"
pRTiles = " fx_shift_tiles 10,10,10,1"
pVigentte = " fx_vignette 70,70,95,0,0,0,255"
pBWCircle = " fx_shapes 1,16,10,2,5,90,0,0,1,1,0"
pTunnel = " fx_tunnel 4,80,50,50,0.2,0"

filterList = [pDots, pWhearl, pBlurAngular, pRodilus, pBW, pSegment,
              pTwirl, pDirty, pPixelSort, pOverlayBC, pHope2020, pScanLines, pSponge, pKorb, pBitCrush, pWarp, pFractal, pPloy, pRTiles,
              pVigentte, pBWCircle, pTunnel]



# def readEffectList():
#     lines=[]
#     sanitized=[]
#     with open('./effect/test.txt') as f:
#         lines = f.readlines()
#     for i in lines:
#        sanitized.append(i.replace("\n", ""))
#     return sanitized

# filterList=readEffectList()
# print(filterList)

# exit()

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
        filterArray = filterArray + str(filterList[randrange(0, len(filterList))])

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
          " \n count filter : "+str(filterCount)+
          "\n src image" + imageToRender)
    
    gmicCreate(imageToRender, fileName, filterArray)
    countImgRender=countImgRender +1

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
        outText = "\n succsess at image index: {img} ".format(img=str(images+1))
    except IOError:
        tb = sys.exc_info()[2]
        outText = "\n error at image index: {img} {tb}".format(img=str(images+1),err=tb)
    tEndSingle = time.time()
    print(outText+" elapsed time: {time} seconds".format(time=str(round(tEndSingle-tStartSingle))))


if logToJson:
    dumpToJson(jsonList)

tEndAll = time.time()

print("\n finished! rendered "+str(countImgRender-1) +
      " pictures in " + str(round(tEndAll-tStartAll))+" seconds")

if(createGif):
    createGIF(folderPath["RENDER"],"render")
    createGIF(folderPath["TEMP"],"temp")

