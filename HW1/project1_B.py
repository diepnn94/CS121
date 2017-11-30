import collections
import string
import sys
import time
def reading_input(file_name:str):
    try:
        file = open(file_name, "r")
        result = file.readlines()
        file.close()
        return result
    except:
        return "error"
    
    
def remove_punctuation(file: list):
    result = []
    punctuation_list = """~`!@$#%^&*()-+=<>/?:;'"{}[]|_\,."""
    punctuation = str.maketrans(punctuation_list, " "*len(punctuation_list))
    new_line = str.maketrans("\n", " ")
    for i in range(len(file)):
        result.extend(file[i].translate(punctuation).translate(new_line).split())
    return result

def find_occurence(file1: list, file2: list):
    dictionary = dict()

    for i in file1:
        if i == string.punctuation:
            continue
        elif i.lower() not in dictionary:
            dictionary[i.lower()] = 0
    for i in file2:
        if i == string.punctuation:
            continue
        elif i.lower() in dictionary and dictionary[i.lower()] == 0:
            dictionary[i.lower()] = 1
    print(sum(list(dictionary.values())))

if __name__ == "__main__":

    start = time.time()
    if (len(sys.argv) != 3):
        print("The number of argument is incorrect.\n")
        sys.exit()
    file1_name = sys.argv[1]
    file2_name = sys.argv[2]
    file = reading_input(file1_name)
    file2 = reading_input(file2_name)
    
    if file== "error" or file2 == "error":
        msg = "file1" if "file1" == 0 else "file2"
        print("File ", msg, "is invalid.\n")
        sys.exit()
    if len(file) == 0 or len(file2) == 0:
        print("There is no common word between two files (one of the file is empty).\n")
        sys.exit()
        
    filter_file1 = remove_punctuation(file)
    filter_file2 = remove_punctuation(file2)

    del file
    del file2

    if (len(filter_file1) == 0 or len(filter_file2) == 0):
        print("There is no common word between two files (one of the file contains all punctuation).\n")
        sys.exit()
    find_occurence(filter_file1, filter_file2)
    end = time.time()
    print("The total time is ", end- start)





    
