
with open('css to be fixed.txt', 'r', encoding="utf8") as cs:
    for line in cs:
        line = line.split("}")

outF = open('fixedcss.txt', 'w')
for fixed in line:
    outF.write(fixed)
    outF.write('}')
    outF.write('\n')
outF.close()

