import os

#get the current working directory
os.getcwd()

#check whether your file exists in the current working directory
print('File name : ', os.path.abspath("requirements.txt"))
print('File name : ', os.path.abspath("requirements_check.py"))
print()

f = open("requirements.txt", "r")

libraries = []

for i in f.readlines():
    lib_name = i.split("=", 1)[0]
    print(lib_name)