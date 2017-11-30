
import collections
import time
import string
import sys


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
    
    punctuation_list = """~`!@#$%^&*()-+=<>/?:;'"{}[]_|\,."""
    punctuation = str.maketrans(punctuation_list, " "*len(punctuation_list))
    new_line = str.maketrans("\n", " ")
    for i in range(len(file)):
        result.extend(file[i].translate(punctuation).translate(new_line).split())
    del file
    return result

def find_frequency(file: list):
    dictionary = dict()
    for i in file:
        if i == string.punctuation:
            continue
        elif i.lower() in dictionary:
            dictionary[i.lower()] += 1
        else:
            dictionary[i.lower()] = 1
    del file
    return dictionary

def output_frequency(dictionary: dict):
    dict_items = sorted(dictionary.items(), key = lambda x: [-x[1], x[0]])
    for i in dict_items:
        print(i[0], "-", i[1])


if __name__ == "__main__":

    start = time.time()
    
    if (len(sys.argv) != 2):
        print("The number of argument is incorrect.\n")
        sys.exit()
    file_name = sys.argv[1]
    file = reading_input(file_name)
    if file == "error":
        print("The file is invalid.\n")
        sys.exit()
    if len(file) == 0:
        print("The file is empty.\n")
        sys.exit()
        
    filter_file = remove_punctuation(file)
    if len(filter_file) == 0:
        print("The file contain all punctuation.\n")
        sys.exit()
        
    frequency_list = find_frequency(filter_file)
    output_frequency(frequency_list)
    end = time.time()
    print("The total time is ", end - start)
    
    
    
    
