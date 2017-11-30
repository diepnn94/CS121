
import string
import sys
import time


def remove_punctuation(file: str):
    punctuation_list = """~`!@#$%^&*()-+=<>/?:;'"{}[]_|\,."""
    punctuation = str.maketrans(punctuation_list, " "*len(punctuation_list))
    
    file = file.translate(punctuation).split()
    for i in range(len(file)):
        if file[i].isalnum() == False:
            result = ""
            for e in file[i]:
                if e in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890':
                    result+= e.lower()
            file[i] = result
                
    return file


def reading_input_output_common_words(file_name:str, file_name2: str):
    ##try:
        file = open(file_name, "r")
        count = 0
        dictionary = dict()
        for i in file:
            for e in remove_punctuation(i):
                ##try:
                    if e.lower() not in dictionary:
                        dictionary[e.lower()] = 0
                ##except:
                    ##pass
        if len(dictionary) == 0:
            return "empty"
                    
        file1 = open(file_name2, "r")
        for a in file1:
            for b in remove_punctuation(a):
                ##try:
                    if b.lower() in dictionary:
                        count+=1;
                        del dictionary[b.lower()]
                ##except:
                    ##pass
        
        file.close()
        file1.close()
        print(count)
        if count == 0:
            return "empty"
        
        return "success"
    ##except:
        ##return "error"

if __name__ == "__main__":

    start = time.time()
    if (len(sys.argv) != 3):
        print("The number of argument is incorrect.\n")
        sys.exit()
    file1_name = sys.argv[1]
    file2_name = sys.argv[2]

    message = reading_input_output_common_words(file1_name, file2_name)

    if message == "empty":
        print("One of the files is either empty or contains only punctuations. No common words found.\n")
        sys.exit()
        
    elif message == "error":
        
        print("One of the files is invalid.\n")
        sys.exit()
    
    end = time.time()
    print("The total time is ", end- start)





    
