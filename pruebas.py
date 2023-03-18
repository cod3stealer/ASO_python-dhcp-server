import os

#os.popen('rm -r control.txt')

os.popen('ip a > control.txt')

f = open("control.txt", "r")
for i in f:
    print(i)
f.close()
