import shutil

def readEffectList():
    lines=[]
    sanitized=[]
    with open('./effect/test.txt') as f:
        lines = f.readlines()
    for i in lines:
       sanitized.append(i.replace("\n", ""))
    return sanitized

#TEST1

filterList=readEffectList()
print(filterList)


folderPath = {
    "GIF": './gif',
    "TEMP": './temp',
    "RENDER": './render'
}



make_archive('temp_',folderPath['TEMP'])



