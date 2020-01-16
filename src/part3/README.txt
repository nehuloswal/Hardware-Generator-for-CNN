For Part 3 generator:
1. Please copy all the files in this folder to the desired location.
2. cd to the location and type "python hardware_gen.py 2 N M1 M2 M3 T A"
3. To test the generated design simply do "./testnetwork"

Explaination of files generated.
A separate .sv file for each of the 3 layers (named layer*_N_M_T_P.sv).
lib_conv.sv which contains the required modules of each of the layer.
.sv file containing the top level module and connection of all the three layers (filename starting with multi_*).
A testbench file for testing(named tb_multi_*)