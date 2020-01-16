// ESE 507 Project 3 Handout Code
// Fall 2019
// You may not redistribute this code

// Getting started:
// The main() function contains the code to read the parameters. 
// For Parts 1 and 2, your code should be in the genLayer() function. Please
// also look at this function to see an example for how to create the ROMs.
//
// For Part 3, your code should be in the genAllLayers() function.



#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cstdlib>
#include <cstring>
#include <assert.h>
#include <math.h>
using namespace std;

void printUsage();
void genLayer(int N, int M, int T, int P, vector<int>& constvector, string modName, ofstream &os);
void genAllLayers(int N, int M1, int M2, int M3, int T, int A, vector<int>& constVector, string modName, ofstream &os);
void readConstants(ifstream &constStream, vector<int>& constvector);
void genROM(vector<int>& constVector, int bits, string modName, ofstream &os);




int main(int argc, char* argv[]) {

    // If the user runs the program without enough parameters, print a helpful message
    // and quit.
    if (argc < 7) {
        printUsage();
        return 1;
    }

    int mode = atoi(argv[1]);

    ifstream const_file;
    ofstream os;
    vector<int> constVector;

    //----------------------------------------------------------------------
    // Look here for Part 1 and 2
    if ((mode == 1) && (argc == 7)) {
        // Mode 1: Generate one layer with given dimensions and one testbench

        // --------------- read parameters, etc. ---------------
        int N = atoi(argv[2]);
        int M = atoi(argv[3]);
        int T = atoi(argv[4]);
        int P = atoi(argv[5]);
        const_file.open(argv[6]);
        if (const_file.is_open() != true) {
            cout << "ERROR reading constant file " << argv[6] << endl;
            return 1;
        }

        // Read the constants out of the provided file and place them in the constVector vector
        readConstants(const_file, constVector);

        string out_file = "conv_" + to_string(N) + "_" + to_string(M) + "_" + to_string(T) + "_" + to_string(P) + ".sv";

        os.open(out_file);
        if (os.is_open() != true) {
            cout << "ERROR opening " << out_file << " for write." << endl;
            return 1;
        }
        // -------------------------------------------------------------

        // call the genLayer function you will write to generate this layer
        string modName = "conv_" + to_string(N) + "_" + to_string(M) + "_" + to_string(T) + "_" + to_string(P);
        genLayer(N, M, T, P, constVector, modName, os); 

    }
    //--------------------------------------------------------------------


    // ----------------------------------------------------------------
    // Look here for Part 3
    else if ((mode == 2) && (argc == 9)) {
        // Mode 2: Generate three layer with given dimensions and interconnect them

        // --------------- read parameters, etc. ---------------
        int N  = atoi(argv[2]);
        int M1 = atoi(argv[3]);
        int M2 = atoi(argv[4]);
        int M3 = atoi(argv[5]);
        int T  = atoi(argv[6]);
        int A  = atoi(argv[7]);
        const_file.open(argv[8]);
        if (const_file.is_open() != true) {
            cout << "ERROR reading constant file " << argv[8] << endl;
            return 1;
        }
        readConstants(const_file, constVector);

        string out_file = "multi_" + to_string(N) + "_" + to_string(M1) + "_" + to_string(M2) + "_" + to_string(M3) + "_" + to_string(T) + "_" + to_string(A) + ".sv";


        os.open(out_file);
        if (os.is_open() != true) {
            cout << "ERROR opening " << out_file << " for write." << endl;
            return 1;
        }
        // -------------------------------------------------------------

        string mod_name = "multi_" + to_string(N) + "_" + to_string(M1) + "_" + to_string(M2) + "_" + to_string(M3) + "_" + to_string(T) + "_" + to_string(A);

        // call the genAllLayers function
        genAllLayers(N, M1, M2, M3, T, A, constVector, mod_name, os);

    }
    //-------------------------------------------------------

    else {
        printUsage();
        return 1;
    }

    // close the output stream
    os.close();

}

// Read values from the constant file into the vector
void readConstants(ifstream &constStream, vector<int>& constvector) {
    string constLineString;
    while(getline(constStream, constLineString)) {
        int val = atoi(constLineString.c_str());
        constvector.push_back(val);
    }
}

// Generate a ROM based on values constVector.
// Values should each be "bits" number of bits.
void genROM(vector<int>& constVector, int bits, string modName, ofstream &os) {

        int numWords = constVector.size();
        int addrBits = ceil(log2(numWords));

        os << "module " << modName << "(clk, addr, z);" << endl;
        os << "   input clk;" << endl;
        os << "   input [" << addrBits-1 << ":0] addr;" << endl;
        os << "   output logic signed [" << bits-1 << ":0] z;" << endl;
        os << "   always_ff @(posedge clk) begin" << endl;
        os << "      case(addr)" << endl;
        int i=0;
        for (vector<int>::iterator it = constVector.begin(); it < constVector.end(); it++, i++) {
            if (*it < 0)
                os << "        " << i << ": z <= -" << bits << "'d" << abs(*it) << ";" << endl;
            else
                os << "        " << i << ": z <= "  << bits << "'d" << *it      << ";" << endl;
        }
        os << "      endcase" << endl << "   end" << endl << "endmodule" << endl << endl;
}

// Parts 1 and 2
// Here is where you add your code to produce a neural network layer.
void genLayer(int N, int M, int T, int P, vector<int>& constVector, string modName, ofstream &os) {

    os << "module " << modName << "();" << endl;
    os << "   // your stuff here!" << endl;
    os << "endmodule" << endl << endl;

    // At some point you will want to generate a ROM with values from the pre-stored constant values.
    // Here is code that demonstrates how to do this for the simple case where you want to put all of
    // the matrix values W in one ROM, and all of the bias values B into another ROM. (This is probably)
    // all that you will need for the ROMs.

    // Check there are enough values in the constant file.
    if (M > constVector.size()) {
        cout << "ERROR: constVector does not contain enough data for the requested design" << endl;
        cout << "The design parameters requested require " << M << " numbers, but the provided data only have " << constVector.size() << " constants" << endl;
        assert(false);
    }

    // Generate a ROM for f with constants in constVector, T bits, and the given name
    string romModName = modName + "_f_rom";
    genROM(constVector, T, romModName, os);

}


// Part 3: Generate a hardware system with three layers interconnected.
// Layer 1: Input length: N, filter length: M1, output length: L1 = N-M1+1
// Layer 2: Input length: L1, filter length: M2, output length: L2 = L1-M2+1
// Layer 3: Input length: M2, filter length: M3, output length: L3 = L2-M3+1
// T is the number of bits
// A is the number of multipliers your overall design may use.
// Your goal is to build the highest-throughput design that uses A or fewer multipliers
// constVector holds all the constants for your system (all three layers, in order)
void genAllLayers(int N, int M1, int M2, int M3, int T, int A, vector<int>& constVector, string modName, ofstream &os) {

    // Here you will write code to figure out the best values to use for P1, P2, and P3, given
    // mult_budget. 
    int P1 = 1; // replace this with your optimized value
    int P2 = 1; // replace this with your optimized value
    int P3 = 1; // replace this with your optimized value

    // output top-level module


    os << "module " << modName << "();" << endl;
    os << "   // this module should instantiate three convolution modules and wire them together" << endl;
    os << "endmodule" << endl;





    // -------------------------------------------------------------------------
    // Split up constVector for the three layers
    int start = 0;
    int stop = M1;
    vector<int> constVector1(&constVector[start], &constVector[stop]);

    // layer 2's W matrix is M2 x M1 and its B vector has size M2
    start = stop;
    stop = start+M2;
    vector<int> constVector2(&constVector[start], &constVector[stop]);

    // layer 3's W matrix is M3 x M2 and its B vector has size M3
    start = stop;
    stop = start+M3;
    vector<int> constVector3(&constVector[start], &constVector[stop]);

    if (stop > constVector.size()) {
        cout << "ERROR: constVector does not contain enough data for the requested design" << endl;
        cout << "The design parameters requested require " << stop << " numbers, but the provided data only have " << constVector.size() << " constants" << endl;
        assert(false);
    }
    // --------------------------------------------------------------------------


    // generate the three layer modules
    string subModName1 = "layer1_" + to_string(N) + "_" + to_string(M1) + "_" + to_string(T) + "_" + to_string(P1);
    genLayer(N, M1, T, P1, constVector1, subModName1, os);
    int L1 = N-M1+1;

    string subModName2 = "layer2_" + to_string(L1) + "_" + to_string(M2) + "_" + to_string(T) + "_" + to_string(P2);
    genLayer(L1, M2, T, P2, constVector2, subModName2, os);

    int L2 = L1-M2+1;
    string subModName3 = "layer3_" + to_string(L2) + "_" + to_string(M2) + "_" + to_string(T) + "_" + to_string(P3);
    genLayer(L2, M3, T, P3, constVector3, subModName3, os);

    // You will need to add code in the module at the top of this function to stitch together insantiations of these three modules

}



void printUsage() {
    cout << "Usage: ./gen MODE ARGS" << endl << endl;

    cout << "   Mode 1: Produce one convolution module (Part 1 and Part 2)" << endl;
    cout << "      ./gen 1 N M T P const_file" << endl;
    cout << "      See project description for explanation of parameters." << endl;
    cout << "      Example: produce a convolution with input vector of length 16, filter of length 4, parallelism 1" << endl;
    cout << "               and 16 bit words, with constants stored in file const.txt" << endl;
    cout << "                   ./gen 1 16 4 16 1 const.txt" << endl << endl;

    cout << "   Mode 2: Produce a system with three interconnected convolution module (Part 3)" << endl;
    cout << "      Arguments: N, M1, M2, M3, T, A, const_file" << endl;
    cout << "      See project description for explanation of parameters." << endl;
    cout << "              e.g.: ./gen 2 16 4 5 6 15 16 const.txt" << endl << endl;
}
