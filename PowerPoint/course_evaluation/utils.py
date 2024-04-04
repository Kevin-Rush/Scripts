#useful functions used across multiple scripts

def print_loader (length, i):
    #print a loading bar for a dataframe
    percentage = int((i / length) * 100)
    loading_bar = '#' * (percentage // 2 + 2) + '-' * (50 - percentage // 2)
    print(f"\r[{loading_bar}] {percentage}%", end='')
    if percentage == 100:
        print()

def clean_filename(filename):
    #clean a filename to remove any special characters
    if "[Slides] " in filename:
        filename = filename.replace("[Slides] ", "")
    if " (1)" in filename:
        filename = filename.replace(" (1)", "")
    return filename