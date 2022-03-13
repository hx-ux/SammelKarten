import glob
import gmic
import json
from random import randrange, random
import imagehash
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import math
import time
import os


folderPath={
    "GIF":'./gif',
    "TEMP":'./temp',
    "RENDER":'./render'
}

# input dimensions should be 600x600
sourceImg = "blury_tree.jpg"
# how many filter should be appended ?
# your value times 5 , 2 means 5*2=10
# the highest value in this case can be 10, the lowest 1
interationScale = 1
# how many images should be created ?
countImg = 20
# set your seed
# JSON log ?
logToJson = False
# Draws the cards border with informations
drawInfo = True
drawInfoText = True
#if true, the previous image (with filters applied) will be rendered 
# 1.png ==> FILTERS ==> 2.png
#if false, the src image will be rendered with filters
# src.png ==> FILTERS ==> 1.png
generateRecursive=True
#creates a gif with all images in the selected folder
createGif=True
GifInputPath=folderPath["TEMP"]




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


def clearFolder(path):
    for file in os.listdir(path):
        if file.endswith('.png'):
            filePath=path+'/'+file
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


countImgRender = 1
jsonList = []

def createGIF(path):
    
    print("creating gif")
    # frames=Image.open(sourceImg)
    frames= [Image.open(f) for f in sorted(glob.glob(f"{path}/*.png"))]
    
    frame_one=Image.open(sourceImg)
    frame_one.save(fp='./gif/render.gif', format='GIF', append_images=frames,
         save_all=True, duration=200, loop=0)
    print("finished gif")


def dumpToJson(list):
    jsonFile = open("json/data.json", "w")
    jsonFile.write(json.dumps(list))
    jsonFile.close()


tStartAll = time.time()
print("Starting loop, this could take a long time ")
# START creation loop

def gmicCreate(inImg, fileName, fChoice):
    gmic.run(inImg+fChoice + " output "+"temp/"+fileName)

for c in range(countImg):

    fileName = ""
    fChoice = ""
    fCount = randrange(1, 5*interationScale, 1)
    rare = math.ceil(fCount/interationScale)
    for x in range(fCount):
        fChoice = fChoice + str(filterList[randrange(0, len(filterList))])

    fileName = ''.join(str(c+1)+".png")
    tStartSingle = time.time()
    print("starting image no: "+fileName +
          " \n count filter : "+str(fCount))
    im=sourceImg

    if(generateRecursive):
        if(countImgRender >2):
            prevIm='./temp/'+str(countImgRender-1)+".png"
            if os.path.exists(prevIm):
                im=prevIm

         
    print("src-file"+im)
    gmicCreate(im, fileName, fChoice)

    try:
        img = Image.open("temp/"+fileName).convert("RGB")
        if drawInfo:
            width, height = img.size
            font_size = 20
            font = ImageFont.truetype(
                "usr/share/fonts/truetype/ubuntu/UbuntuMono-B.ttf", font_size, encoding="unic")

            imgHash = imagehash.whash(img)
            fillCol = rareColor(rare)
            draw = ImageDraw.Draw(img)

            draw.line((0, 0, 0, height), fill=fillCol, width=100)
            draw.line((width, 0, width, height), fill=fillCol, width=100)
            draw.rectangle(((0, 0), (width, 50)), fill=fillCol)
            draw.rectangle(((0, height), (width, height-150)), fill=fillCol)
            if(drawInfoText):
                draw.text((40, height-120), "Number: " +
                          str(c+1), font=font, fill='white')
                draw.text((40, height-100), "Rarity: " +
                          str(rare), font=font, fill='white')
                draw.text((40, height-80), "Hash: " +
                          str(imgHash), font=font, fill='white')
                draw.text((40, height-60), "Filter: " +
                          str(fCount), font=font, fill='white')

       
        img=img.resize((600,600),Image.NEAREST)
        img.save("render/"+fileName, quality=100)
        if(logToJson):
            jsonList.append({"number": c+1, "fName": fileName,
                             "iterations": rare, "effects": fChoice, "rarity": rare, "hash": str(imgHash)})
        countImgRender += 1
        outText = "\n succsess at image index: "+str(c+1)
    except IOError:
        outText = "\n error at image index: "+str(c+1)
    tEndSingle = time.time()
    print(outText+" elapsed time: "+str(round(tEndSingle-tStartSingle))+" seconds")


  

if logToJson:
    dumpToJson(jsonList)

tEndAll = time.time()

print("\n finished! rendered "+str(countImgRender-1) +
      " pictures in " + str(round(tEndAll-tStartAll))+" seconds")

if(createGif):
    createGIF(GifInputPath)