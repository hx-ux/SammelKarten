import gmic
import json
from random import randrange
import imagehash
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import math


# input dimensions should be 600x600
inImg = "blury_tree.jpg"
# how many filter should be appended ?
# your value times 5 , 2 means 5*2=10
# the highest value in this case can be 10, the lowest 1
interationScale = 1
# how many images should be created ?
countImg = 5
# JSON log ?
logToJson = False
# Draws the cards border with informations
drawInfo = True


# Filter used
pWhearl = " fx_whirls 20,3.88,0.2,1.672,11,0,50,50"
pBlurAngular = " fx_blur_angular 0.52,50,50,3.5,1,7,0"
pRodilus = " rodilius 10"
pDots = " fx_polka_dots 18.1,16.28,50,50,0,0.5,0.1,1,255,255,255,255"
pBW = " fx_blackandwhite 0.299,0,0.587,0,0.114,0,0,0,0,0,0,0,0,0,2,0,0,0,16,4,0,0,0,50,50"
pSegment = " fx_segment_watershed 2,1,0,0,0,50,50"
# pWaterDrops = " fx_drop_water 0,20,2,80,0,3,35,10,1,0.5,0.25,0.5,0.75,0.05,0.15,1"
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
pRTiles=" fx_shift_tiles 10,10,10,1"

pMosaic=  " fx_lavalampbw 14,30,1,49.21,0.15,0.01,0"
pVigentte=" fx_vignette 70,70,95,0,0,0,255"
filterList = [pDots, pWhearl, pBlurAngular, pRodilus, pBW, pSegment,
              pTwirl, pDirty, pPixelSort, pOverlayBC, pHope2020, pScanLines, pSponge, pKorb, pBitCrush, pWarp, pFractal, pPloy,pRTiles,
              
              pMosaic,pVigentte]


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


countImgRender = 0
jsonList = []


def dumpToJson(list):
    jsonFile = open("json/data.json", "w")
    jsonFile.write(json.dumps(list))
    jsonFile.close()


print("Starting loop, this could take a long time ")
# START creation loop
for c in range(countImg):
    fName = ""
    fChoice = ""
    nI = randrange(1, 5*interationScale, 1)
    rare = math.ceil(nI/interationScale)
    for x in range(nI):
        fChoice = fChoice + str(filterList[randrange(0, len(filterList))])

    fName = str(c+1)+".png"
    print("starting image no: "+fName)
    gmic.run(inImg+fChoice + " output "+"temp/"+fName)

    try:
        img = Image.open("temp/"+fName).convert("RGB")
        if drawInfo:
            width, height = img.size
            font_size = 20
            font = ImageFont.truetype(
            "usr/share/fonts/truetype/ubuntu/UbuntuMono-B.ttf", font_size, encoding="unic")

            hash = imagehash.whash(img)
            fillCol = rareColor(rare)
            draw = ImageDraw.Draw(img)

            draw.line((0, 0, 0, height), fill=fillCol, width=100)
            draw.line((width, 0, width, height), fill=fillCol, width=100)
            draw.rectangle(((0, 0), (width, 50)), fill=fillCol)
            draw.rectangle(((0, height), (width, height-150)), fill=fillCol)

            draw.text((40, height-120), "Number: " +
                  str(c+1), font=font, fill='white')
            draw.text((40, height-100), "Rarity: " +
                  str(rare), font=font, fill='white')
            draw.text((40, height-80), "Hash: "+str(hash), font=font, fill='white')
            draw.text((40, height-60), "Filter: " +
                  str(nI), font=font, fill='white')
        
        img.save("render/"+fName, quality=100)
        if(logToJson):
            jsonList.append({"number": c+1, "fName": fName,
                             "iterations": rare, "effects": fChoice, "rarity": rare, "hash": str(hash)})
        countImgRender += 1
        print("succsess at image index: "+str(c+1))
    except IOError:
        print("error at image index: "+str(c+1))
# END creation loop

if logToJson:
    dumpToJson(jsonList)

print("finished! rendered "+str(countImgRender)+" pictures")
