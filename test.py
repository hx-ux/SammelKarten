# import shutil

# def readEffectList():
#     lines=[]
#     sanitized=[]
#     with open('./effect/test.txt') as f:
#         lines = f.readlines()
#     for i in lines:
#        sanitized.append(i.replace("\n", ""))
#     return sanitized

# #TEST1

# filterList=readEffectList()
# print(filterList)


# folderPath = {
#     "GIF": './gif',
#     "TEMP": './temp',
#     "RENDER": './render'
# }



# make_archive('temp_',folderPath['TEMP'])



# import unittest

# class TestStringMethods(unittest.TestCase):


  
#     def test_readAsList(self):
#         exampleList=readFileAsList("ownSelection.txt",self)
#         self.assertEqual(exampleList(exampleList[0],'fx_whirls 20,3.88,0.2,1.672,11,0,50,50'))

# if __name__ == '__main__':
#     unittest.main()



import re


def readFileAsList(fileName):
    fileName = r"./effect/"+fileName
    text_file = open(fileName, "r")
    lines = text_file.readlines()
    # print (lines)
    text_file.close()
    return lines


testL =[]

testL=readFileAsList("ownSelection.txt")
print(testL[1])