import argparse
import sys
import math
import os
parser = argparse.ArgumentParser()
parser.add_argument("integers",type=int,nargs = 7)
args = parser.parse_args()

os.system('make')
def find_log_size(num):
    start = math.log(num, 2)

    if ((start - int(start)) != 0):
        start += + 1
    return int(start) 

n1 = args.integers[1]
m1 = args.integers[2]
m2 = args.integers[3]
m3 = args.integers[4]
width = args.integers[5]
total = args.integers[6]
n2 = n1 - m1 + 1
n3 = n2 - m2 + 1
p1 = 1
p3 = 1
p2 = 1
best_p3 = 1
best_p1 = 1
best_p2 = 1
t1 = m1 + 2.0
t2 = m2 + 2.0
t3 = m3 + 2.0
l1 = n1-m1+1
l2 = n2-m2+1
l3 = n3-m3+1

min_cost = 2147483647 
while(p3 < total - 2):
    while(p2 < total - 2):
        while(p1 < (total - 2) ):
            if((total - (p1 + p2 + p3)) >= 0):
                cost = ((l1*t1)/(p1)) + ((l2 * t2)/p2) + ((l3*t3)/p3)
                if(cost < min_cost):
                    min_cost = cost
                    best_p1 = p1
                    best_p2 = p2
                    best_p3 = p3
                if((total - (p1 + p2 + p3)) >= 0):
                    p1 += 1
                    while((l1%p1) != 0 and ((total - (p1 + p2 + p3)) >= 0)):
                        p1 += 1
            else:
                break
        p2 = p2 + 1
        p1 = 1
        while((l2%p2) != 0 and ((total - (p1 + p2 + p3)) >= 0)):
            p2 = p2 + 1
    p3 = p3+1
    p1 = 1
    p2 = 1
    while((l3%p3) != 0 and ((total - (p1 + p2 + p3)) >= 0)):
        p3 = p3+1
        
p = [best_p1,best_p2,best_p3]
n = [n1,n2,n3]
m = [m1,m2,m3]


const_file_command = './testgen 2 ' + str(n1) + ' ' + str(m1) + ' ' + str(m2) + ' ' +  str(m3) + ' '  + str(width) + ' ' + str(total)
os.system(const_file_command)

const_file_name = 'const_' + str(n1) + '_' + str(m1) + '_' + str(m2)+ '_' + str(m3) + '_'  + str(width) + '_' + str(total) + '.txt'
generate_rom_command = './gen 2 ' + str(n1) + ' ' + str(m1) + ' ' + str(m2) + ' ' + str(m3) + ' '  + str(width) + ' ' + str(total) +  ' ' + const_file_name
os.system(generate_rom_command)

rom1 = 'module layer1_' + str(n1) + '_' + str(m1) + '_' + str(width) + '_' + str(1) + '_f_rom' 
rom2 = 'module layer2_' + str(n2) + '_' + str(m2) + '_' + str(width) + '_' + str(1) + '_f_rom' 
rom3 = 'module layer3_' + str(n3) + '_' + str(m3) + '_' + str(width) + '_' + str(1) + '_f_rom' 

rom_name = [rom1,rom2,rom3]
romname = 'multi_' + str(n1) + '_' + str(m1) + '_' + str(m2) + '_' + str(m3) + '_' + str(width) + '_' + str(total) +  '.sv'

sRom = ''
rom_list = []
with open(romname, 'r') as file:
    rom = file.readline()
    while rom:
        rom = file.readline()
        if (rom1 in rom):
            sRom += 'module layer1_' + str(n1) + '_' + str(m1) + '_' + str(width) + '_' + str(best_p1) + '_f_rom' + '(clk, addr, z);\n'
            while('endmodule' not in rom):
                rom = file.readline()
                sRom += rom
            #sRom += 'endmodule'
            rom_list.append(sRom)
        sRom = ''
        
        if (rom2 in rom):
            sRom += 'module layer2_' + str(n2) + '_' + str(m2) + '_' + str(width) + '_' + str(best_p2) + '_f_rom' + '(clk, addr, z);\n'
            #rom = file.readline()
            while('endmodule' not in rom):
                rom = file.readline()
                sRom += rom
            #sRom += 'endmodule'
            rom_list.append(sRom)
        sRom = ''
        
        if (rom3 in rom):
            sRom += 'module layer3_' + str(n3) + '_' + str(m3) + '_' + str(width) + '_' + str(best_p3) + '_f_rom' + '(clk, addr, z);\n'
            #rom = file.readline()
            while('endmodule' not in rom):
                rom = file.readline()
                sRom += rom
            #sRom += 'endmodule'
            rom_list.append(sRom)
        sRom = ''
#print(rom_list)


rom1 = 'layer1_' + str(n1) + '_' + str(m1) + '_' + str(width) + '_' + str(best_p1) + '_f_rom' 
rom2 = 'layer2_' + str(n2) + '_' + str(m2) + '_' + str(width) + '_' + str(best_p2) + '_f_rom' 
rom3 = 'layer3_' + str(n3) + '_' + str(m3) + '_' + str(width) + '_' + str(best_p3) + '_f_rom' 

rom_name = [rom1,rom2,rom3]

for i in range(0,3):

  addrx = find_log_size(n[i])
  addrf = find_log_size(m[i])

  sModname_rom = rom_name[i]
  sModname_gen = "layer" + str(i+1) + "_" + str(n[i]) + "_" + str(m[i]) + "_" + str(width) + "_" + str(p[i])
  filename = 'layer' + str(i+1) + '_' + str(n[i]) + '_' + str(m[i]) +  '_' + str(width) + '_' + str(p[i]) +  '.sv'
#get template
  if (p[i] == 1):
	  with open('templete1.sv', 'r') as file:
		  templete = file.read()
  else:
	  with open('templete.sv', 'r') as file:
		  templete = file.read()


  templete = templete.replace('$$ROM$$', rom_list[i]).replace('$WIDTH$', str(width)).replace('$ADDRX$', str(addrx)).replace('$ADDRF$', str(addrf))
  templete = templete.replace('$N$', str(n[i])).replace('$M$', str(m[i])).replace('$P$', str(p[i]))
  templete = templete.replace('$rommodname$', sModname_rom).replace('$modnamegen$', sModname_gen)


  outputfile = open(filename, 'w+')
  outputfile.write(templete)
  outputfile.close()

with open("top_temp.sv", 'r') as file:
    temp_main = file.read()
temp_main = temp_main.replace('$WIDTH$', str(width))

for i in range(0, 3):
    sModname_gen = "layer" + str(i+1) + "_" + str(n[i]) + "_" + str(m[i]) + "_" + str(width) + "_" + str(p[i])
    replacestr = "$modname" + str(i+1) + "$"
    temp_main = temp_main.replace(replacestr, sModname_gen)
 
with open(romname, 'r') as file:
    rom = file.readline()

rom = rom[:-3]
rom += str("clk, reset, s_data_in_x, s_valid_x, s_ready_x, m_data_out_y, m_valid_y, m_ready_y);\n")
rom += temp_main
out = open(romname, 'w+')
out.write(rom)
out.close

testlayer = "vlog +acc lib_conv.sv\n"
for i in range(0,3):
  vlog_file_command = 'vlog +acc ' + 'layer' + str(i+1) + '_' + str(n[i]) + '_' + str(m[i]) +  '_' + str(width) + '_' + str(p[i]) +  '.sv\n'
  testlayer += vlog_file_command
  #os.system(vlog_file_command)


tbname = "tb_multi_" + str(n1) + "_" + str(m1) + "_" + str(m2) + "_" + str(m3)  + "_" + str(width) + "_" + str(total) + ".sv"
testlayer += 'vlog +acc ' + tbname + '\n'
with open(tbname, 'r') as file:
    tbfile = file.read()
    
writecontent = rom + "\n" + tbfile
tbench = open(tbname, 'w')
tbench.write(writecontent)

testlayer += "vsim " + tbname[:-3] + ' -c -do "run -all"'

out = open("testnetwork", 'w+')
out.write(testlayer)
out.close()
os.system("chmod 777 testnetwork")
'''sim_command = "./testlayer " + str(n) + ' ' + str(m) + ' ' + str(width) + ' ' + str(t)
os.system(sim_command)'''
#print templete