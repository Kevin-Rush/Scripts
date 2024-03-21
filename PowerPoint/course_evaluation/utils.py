#useful functions used across multiple scripts

def print_loader_df (length, i):
    #print a loading bar for a dataframe
    percentage = int((i / length) * 100)
    loading_bar = '#' * (percentage // 2 + 2) + '-' * (50 - percentage // 2)
    print(f"\r[{loading_bar}] {percentage}%", end='')