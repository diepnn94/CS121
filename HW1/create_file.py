
file = open('big1.txt', 'w')
file1=open('aniketsh_input.txt', 'r')
data = file1.readlines()
for i in range(2000):
    file.write(str(data))

file1.close()
file.close()
