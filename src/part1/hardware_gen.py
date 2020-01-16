import argparse
import sys
import math
import os
parser = argparse.ArgumentParser()
parser.add_argument("integers",type=int,nargs = 4)
args = parser.parse_args()

os.system('make')
def find_log_size(num):
	start = math.log(num, 2)

	if ((start - int(start)) != 0):
		start += + 1
	return int(start) 

n = args.integers[0]
m = args.integers[1]
width = args.integers[2]
t = args.integers[3]

const_file_command = './testgen 1 ' + str(n) + ' ' + str(m) + ' ' + str(width) + ' ' + str(t)
os.system(const_file_command)

const_file_name = 'const_' + str(n) + '_' + str(m) + '_' + str(width) + '_' + str(t) + '.txt'
generate_rom_command = './gen 1 ' + str(n) + ' ' + str(m) + ' ' + str(width) + ' ' + str(t) + " " + const_file_name
os.system(generate_rom_command)

addrx = find_log_size(n)
addrf = find_log_size(m)

sModname_rom = "conv_" + str(n) + "_" + str(m) + "_" + str(width) + "_" + str(t) + "_f_rom"
sModname_gen = "conv_" + str(n) + "_" + str(m) + "_" + str(width) + "_" + str(t)

#get template
with open('templete.sv', 'r') as file:
    templete = file.read()

#get rom 
romname = 'conv_' + str(n) + '_' + str(m) + '_' + str(width) + '_' + str(t) + '.sv'
i = 0
sRom = ''
with open(romname, 'r') as file:
    rom = file.readline()
    i = 1
    while rom:
      rom = file.readline()
      i += 1
      if (i > 4):
        sRom += rom 

templete = templete.replace('$$ROM$$', sRom).replace('$WIDTH$', str(width)).replace('$ADDRX$', str(addrx)).replace('$ADDRF$', str(addrf))
templete = templete.replace('$N$', str(n)).replace('$M$', str(m))
templete = templete.replace('$rommodname$', sModname_rom).replace('$modnamegen$', sModname_gen)


outputfile = open(romname, 'w')
outputfile.write(templete)
outputfile.close()

tbname = "tb_conv_" + str(n) + "_" + str(m) + "_" + str(width) + "_" + str(t) + ".sv"

with open(tbname, 'r') as file:
    tbfile = file.read()
    
writecontent = templete + "\n" + tbfile
tbench = open(tbname, 'w')
tbench.write(writecontent)

test = 'vlog +acc ' + tbname + '\n'

test+= "vsim " + tbname[:-3] + ' -c -do "run -all"'

out = open("testlayer", 'w+')
out.write(test)
out.close()
os.system("chmod 777 testlayer")
print(test)

''''sim_command = "./testlayer " + str(n) + ' ' + str(m) + ' ' + str(width) + ' ' + str(t)
os.system(sim_command)'''
#print templete