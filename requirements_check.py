import os

#get the current working directory
os.getcwd()

#check whether your file exists in the current working directory
print('File name : ', os.path.abspath("requirements.txt"))
print('File name : ', os.path.abspath("requirements_check.py"))
print()

reqs_file = open("requirements.txt", "r")
libs_file = open("libraries.txt")

libraries = []

for i in reqs_file.readlines():
    lib_name = i.split("=", 1)[0]
    libraries.append(lib_name)

excluded_libs = []
for i in libs_file.readlines():
    if i[0] == "#":
        continue
    lib_name = i.split(" ")
    
    if lib_name[-1] == "\n":
        lib_name.pop(-1)
    lib_name[-1] = lib_name[-1].split("\n")[0]
    print(lib_name)