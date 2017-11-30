
import time
import string
import sys
dictionary = dict()



def remove_punctuation(file: str):

    punctuation_list = """~`!@#$%^&*()-+=<>/?:;'"{}[]_|\,."""
    punctuation = str.maketrans(punctuation_list, " "*len(punctuation_list))
    
    file = file.translate(punctuation).split()
    return file

def find_frequency(file: list):
    
    for i in file:
        
        if i.lower() in dictionary:
            dictionary[i.lower()] += 1
        else:
            dictionary[i.lower()] = 1

def reading_input(file_name:str):
    try:
        file = open(file_name, "r")
        for i in file:
            find_frequency(remove_punctuation(i))
        file.close()
        if len(dictionary) == 0:
            return "empty"
    except:
        return "error"
   

def output_frequency(dictionary: dict):
    dict_items = sorted(dictionary.items(), key = lambda x: [-x[1], x[0]]) 
    for i in dict_items:
        try:
            print(i[0], "-", i[1])
        except:
            pass


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
    elif file == "empty":
        print("The file is empty.\n")
        sys.exit()
        
    output_frequency(dictionary)
    end = time.time()
    print("The total time is ", end - start)
    
    
    
    
