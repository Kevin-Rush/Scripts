import os

#get the current working directory
os.getcwd()

#check whether your file exists in the current working directory
print('File name : ', os.path.abspath("requirements.txt"))
print('File name : ', os.path.abspath("requirements_check.py"))
print()

reqs_file = open("requirements.txt", "r")
libs_file = open("libraries.txt")

req_libraries = []

for i in reqs_file.readlines():
    lib_name = i.split("=", 1)[0]
    req_libraries.append(lib_name)

all_libs = []                   #clean up the input from the libraries.txt file and save all libraries in a single list
for i in libs_file.readlines():
    if i[0] == "#":
        continue
    libs_line = i.split(" ")
    
    if libs_line[-1] == "\n":
        libs_line.pop(-1)
    libs_line[-1] = libs_line[-1].split("\n")[0]

    libs_line.remove("import")
    k = 0
    while k < len(libs_line):
        if libs_line[k] == "as" or libs_line[k] == "from":

            libs_line.pop(k)
            k -=1
        k += 1
    
    libs_line.pop(1)
    current_lib = libs_line[0]
    current_lib = current_lib.split(".")
    current_lib = current_lib[0]
    if current_lib not in all_libs:
        all_libs.append(current_lib)
    
print(all_libs)