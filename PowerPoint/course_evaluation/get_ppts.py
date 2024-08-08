import os
import shutil

def delete_dependencies(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Do something with each file
            file_path = os.path.join(root, file)
            # print(file_path)  # Replace this with your desired action

        for dir in dirs:
            if dir == "Dependencies":
                print(f"Deleting {dir}")
                shutil.rmtree(os.path.join(root, dir))

def organize_ppts(folder_path, original_path=None):
    # delete_dependencies(folder_path)
    original_path = folder_path

    # Get a list of all files and folders in the given folder path
    all_items = os.listdir(folder_path)
    print(f"folder_path 1: {folder_path}")
    print(f"all_items: {all_items}")

    # Iterate over each item in the folder
    for item in all_items:
        #if item is a folder called Dependencies, delete
        if item == "Dependencies":
            shutil.rmtree(os.path.join(folder_path, item))
        item_path = os.path.join(folder_path, item)
        print(f"item_path 2: {item_path}")
        print(f"folder_path 2: {folder_path}")

        # Check if the item is a directory
        if os.path.isdir(item_path):
            # Recursively call the function on the subfolder
            organize_ppts(item_path)

        # Check if the item is a file and starts with "[Slides]"
        elif os.path.isfile(item_path) and item.startswith("[Slides]"):
            print(f"item_path 3: {item_path}")
            print(f"folder_path 3: {folder_path}")
            # Move the file to the original folder path
            shutil.move(item_path, folder_path)

        # If the item is neither a file nor a folder, delete it
        else:
            os.remove(item_path)

    # Delete the empty subfolders
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path) and not os.listdir(item_path):
            os.rmdir(item_path)

def move_slides_to_folder(folder_path, final_path):
    # Get a list of all files and folders in the given folder path
    all_items = os.listdir(folder_path)

    # Iterate over each item in the folder
    for item in all_items:
        item_path = os.path.join(folder_path, item)

        # Check if the item is a file and starts with "[Slides]"
        if os.path.isfile(item_path) and item.startswith("[Slides]"):
            # Move the file to the final folder path
            print(f"item_path: {item_path}")
            # Extract the name of the folder the slides file is in
            folder_name = os.path.basename(os.path.dirname(item_path))
            print(f"Folder name: {folder_name}")
            # Get the current file name
            file_name = os.path.basename(item_path)
            # Create the new file name by combining the folder name and the current file name
            new_file_name = f"{folder_name}_{file_name}"
            # Create the new file path by joining the final path and the new file name
            new_file_path = os.path.join(final_path, new_file_name)
            # Move the file to the final folder path with the new file name
            shutil.move(item_path, new_file_path)
    
        # Check if the item is a directory
        elif os.path.isdir(item_path):
            # Recursively call the function on the subfolder
            move_slides_to_folder(item_path, final_path)

# Call the function to organize the PowerPoint files in the given folder
folder_path = "C:/Users/kevin/Downloads/AI for Sustainability"
final_path = folder_path + " - Clean"

# Create the final folder
os.mkdir(final_path)
move_slides_to_folder(folder_path, final_path)
