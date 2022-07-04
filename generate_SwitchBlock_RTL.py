import sys;
import math;

set_W = 0;
seg_freq = [];
L = [];

number_of_tracks_per_segment = [];
new_W = 0;
new_seg_freq = [];

W = 0;

def get_args():
    for x in range (1,len(sys.argv)):
        if (sys.argv[x] == "-W"):
            set_W = int (sys.argv[x+1]);
        if (sys.argv[x] == "-seg_freq"):
            seg_freq.append(sys.argv[x+1]);
        if (sys.argv[x] == "-L"):
            L.append(sys.argv[x+1]);
        
    for x in range(len(seg_freq)):
        number_of_tracks = math.ceil(float(seg_freq[x])*int(set_W)/float(L[x])) * float(L[x]);
        number_of_tracks_per_segment.append(number_of_tracks);

    new_W = 0;
    for x in range (len(number_of_tracks_per_segment)):
        new_W = new_W + number_of_tracks_per_segment[x];

    W = new_W *2;
    
    """ to_print = f"W is {set_W}";
    print(to_print);
    to_print = f"seg_freq is {seg_freq}";
    print(to_print);
    to_print = f"L is {L}";
    print(to_print);
    to_print = f"number of tracks is {number_of_tracks_per_segment}";
    print(to_print);
    to_print = f"Cannot be implemented with W = {set_W}, setting W to {new_W}";
    print(to_print); """
    return int(W);

def generate_mux_rtl():

    #Mux2
    print ("module mux2(d0, d1, s, y);")
    print ("  input  d0, d1, s;")
    print ("  output y;")
    print ("  assign y = s ? d1 : d0;")
    print ("endmodule")
    print ("\n")
    
    #Bottom Mux
    print("module bottom_mux3(d0, d1, d2, s0, s1, y);")
    print("  input d0, d1, d2, s0, s1;")
    print("  output y;")
    print("  wire mux2_0_out;")
    print("  mux2 mux2_0 (d0, d1, s0, mux2_0_out);")
    print("  mux2 mux2_1 (mux2_0_out, d2, s1, y);")
    print("endmodule")
    print("\n")

    #Left Mux
    print("module left_mux3(d0, d1, d2, s0, s1, y);")
    print("  input d0, d1, d2, s0, s1;")
    print("  output y;")
    print("  wire mux2_0_out;")
    print("  mux2 mux2_0 (d0, d1, s0, mux2_0_out);")
    print("  mux2 mux2_1 (mux2_0_out, d2, s1, y);")
    print("endmodule")
    print("\n")

    #Right Mux
    print("module right_mux3(d0, d1, d2, s0, s1, y);")
    print("  input d0, d1, d2, s0, s1;")
    print("  output y;")
    print("  wire mux2_0_out;")
    print("  mux2 mux2_0 (d0, d1, s0, mux2_0_out);")
    print("  mux2 mux2_1 (mux2_0_out, d2, s1, y);")
    print("endmodule")
    print("\n")

    #Top Mux
    print("module top_mux3(d0, d1, d2, s0, s1, y);")
    print("  input d0, d1, d2, s0, s1;")
    print("  output y;")
    print("  wire mux2_0_out;")
    print("  mux2 mux2_0 (d0, d1, s0, mux2_0_out);")
    print("  mux2 mux2_1 (mux2_0_out, d2, s1, y);")
    print("endmodule")
    print("\n")

    #DFF with enable and reset
    print("module DFF_EN (clk, d, rst, en, q);");
    print("input clk, d, rst, en;");
    print("output reg q;");
    print("always @(posedge clk or posedge rst)");
    print("    if (rst)");
    print("        q <= 1'b0;");
    print("    else if (en)");
    print("    q <= d;");
    print ("endmodule");


def generate_config_bits():
    to_print = f"module dff_config_bits("
    print(to_print)
    print("clk,")
    print("en,")
    print("rst,")
    print("d,")
    print("                        s0_left,");
    print("                       s1_left,");
    print("                       s0_right,");
    print("                       s1_right,");
    print("                       s0_bottom,");
    print("                       s1_bottom,");
    print("                       s0_top,");
    print("                       s1_top);");
    
    print("input clk;")
    print("input d;")
    print("input rst;")
    print("input en;")
    #Total number of Multiplexers per side
    total_number_of_multiplexers = 0;
    for x in range (len(L)):
        total_number_of_multiplexers = int(total_number_of_multiplexers + int(number_of_tracks_per_segment[x])/int(L[x]));
        to_print=f"inout [0:{total_number_of_multiplexers-1}] s0_left;"
        print(to_print)
        to_print=f"inout [0:{total_number_of_multiplexers-1}] s1_left;"
        print(to_print)
        to_print=f"inout [0:{total_number_of_multiplexers-1}] s0_right;"
        print(to_print)
        to_print=f"inout [0:{total_number_of_multiplexers-1}] s1_right;"
        print(to_print)
        to_print=f"inout [0:{total_number_of_multiplexers-1}] s0_bottom;"
        print(to_print)
        to_print=f"inout [0:{total_number_of_multiplexers-1}] s1_bottom;"
        print(to_print)
        to_print=f"inout [0:{total_number_of_multiplexers-1}] s0_top;"
        print(to_print)
        to_print=f"inout [0:{total_number_of_multiplexers-1}] s1_top;"
        print(to_print)
        

    #S0
    print("\n")
    to_print=f"DFF_EN config{x} (.clk(clk), .d(d), .rst(rst), .en(en), .q(s0_left[0]));"
    print(to_print)
    current_flop = 1;
    previous_flop =0;
    for x in range (total_number_of_multiplexers-1):
        to_print=f"DFF_EN config{x+1} (.clk(clk), .d(s0_left[{previous_flop}]), .rst(rst), .en(en), .q(s0_left[{current_flop}]));"
        print(to_print)
        previous_flop = current_flop;
        current_flop += 1;
    
    to_print=f"DFF_EN config{total_number_of_multiplexers} (.clk(clk), .d(s0_left[{total_number_of_multiplexers-1}]), .rst(rst), .en(en), .q(s0_right[0]));"
    print(to_print)
    current_flop = 1;
    previous_flop =0;
    for x in range (total_number_of_multiplexers, 2*total_number_of_multiplexers-1):
        to_print=f"DFF_EN config{x+1} (.clk(clk), .d(s0_right[{previous_flop}]), .rst(rst), .en(en), .q(s0_right[{current_flop}]));"
        print(to_print)
        previous_flop = current_flop;
        current_flop += 1;

    to_print=f"DFF_EN config{2*total_number_of_multiplexers} (.clk(clk), .d(s0_right[{total_number_of_multiplexers-1}]), .rst(rst), .en(en), .q(s0_bottom[0]));"
    print(to_print)
    current_flop = 1;
    previous_flop =0;
    for x in range (2*total_number_of_multiplexers, 3*total_number_of_multiplexers-1):
        to_print=f"DFF_EN config{x+1} (.clk(clk), .d(s0_bottom[{previous_flop}]), .rst(rst), .en(en), .q(s0_bottom[{current_flop}]));"
        print(to_print)
        previous_flop = current_flop;
        current_flop += 1;

    to_print=f"DFF_EN config{3*total_number_of_multiplexers} (.clk(clk), .d(s0_bottom[{total_number_of_multiplexers-1}]), .rst(rst), .en(en), .q(s0_top[0]));"
    print(to_print)
    current_flop = 1;
    previous_flop =0;
    for x in range (3*total_number_of_multiplexers, 4*total_number_of_multiplexers-1):
        to_print=f"DFF_EN config{x+1} (.clk(clk), .d(s0_top[{previous_flop}]), .rst(rst), .en(en), .q(s0_top[{current_flop}]));"
        print(to_print)
        previous_flop = current_flop;
        current_flop += 1;

    #S1
    #left
    to_print=f"DFF_EN config{4*total_number_of_multiplexers} (.clk(clk), .d(s0_top[{total_number_of_multiplexers-1}]), .rst(rst), .en(en), .q(s1_left[0]));"
    print(to_print)
    current_flop = 1;
    previous_flop =0;
    for x in range (4*total_number_of_multiplexers,5*total_number_of_multiplexers-1):
        to_print=f"DFF_EN config{x+1} (.clk(clk), .d(s1_left[{previous_flop}]), .rst(rst), .en(en), .q(s1_left[{current_flop}]));"
        print(to_print)
        previous_flop = current_flop;
        current_flop += 1;
    #right
    to_print=f"DFF_EN config{5*total_number_of_multiplexers} (.clk(clk), .d(s1_left[{total_number_of_multiplexers-1}]), .rst(rst), .en(en), .q(s1_right[0]));"
    print(to_print)
    current_flop = 1;
    previous_flop =0;
    for x in range (5*total_number_of_multiplexers,6*total_number_of_multiplexers-1):
        to_print=f"DFF_EN config{x+1} (.clk(clk), .d(s1_right[{previous_flop}]), .rst(rst), .en(en), .q(s1_right[{current_flop}]));"
        print(to_print)
        previous_flop = current_flop;
        current_flop += 1;

    #bottom
    to_print=f"DFF_EN config{6*total_number_of_multiplexers} (.clk(clk), .d(s1_right[{total_number_of_multiplexers-1}]), .rst(rst), .en(en), .q(s1_bottom[0]));"
    print(to_print)
    current_flop = 1;
    previous_flop =0;
    for x in range (6*total_number_of_multiplexers,7*total_number_of_multiplexers-1):
        to_print=f"DFF_EN config{x+1} (.clk(clk), .d(s1_bottom[{previous_flop}]), .rst(rst), .en(en), .q(s1_bottom[{current_flop}]));"
        print(to_print)
        previous_flop = current_flop;
        current_flop += 1;
    
    #top
    to_print=f"DFF_EN config{7*total_number_of_multiplexers} (.clk(clk), .d(s1_bottom[{total_number_of_multiplexers-1}]), .rst(rst), .en(en), .q(s1_top[0]));"
    print(to_print)
    current_flop = 1;
    previous_flop =0;
    for x in range (7*total_number_of_multiplexers,8*total_number_of_multiplexers-1):
        to_print=f"DFF_EN config{x+1} (.clk(clk), .d(s1_top[{previous_flop}]), .rst(rst), .en(en), .q(s1_top[{current_flop}]));"
        print(to_print)
        previous_flop = current_flop;
        current_flop += 1;

    print("endmodule\n")
        
def generate_switch_block_wrapper():
    to_print = f"module Switch_Block_W{int(W/2)}_Wrapper("
    print(to_print)

    number_of_muxes_per_LT_input = 0
    for i in reversed (range (0,W,2)):
        #print(i)
        number_of_muxes_per_LT_input += 1;
        #print("                       left_in,")
        #print("                       right_out,")

    #print(number_of_muxes_per_LT_input)
    number_of_left_inputs = number_of_muxes_per_LT_input;
    number_of_left_outputs = W-number_of_left_inputs;
    number_of_right_outputs = number_of_left_inputs;
    number_of_right_inputs = number_of_left_outputs;
    number_of_top_inputs = number_of_left_outputs;
    number_of_top_outputs = number_of_left_inputs;
    number_of_bottom_inputs = number_of_top_outputs;
    number_of_bottom_outputs = number_of_top_inputs;


    print("clk,")
    print("en,")
    print("rst,")
    print("d,")
    print("                       left_in,");
    print("                       left_out,");
    print("                       right_in,");
    print("                       right_out,");
    print("                       bottom_in,");
    print("                       bottom_out,");
    print("                       top_in,");
    print("                       top_out);");
    #print("                       s0_left,");
    #print("                       s1_left,");
    #print("                       s0_right,");
    #print("                       s1_right,");
    #print("                       s0_bottom,");
    #print("                       s1_bottom,");
    #print("                       s0_top,");
    #print("                       s1_top);");
    #print("                       VDD,");
    #print("                       VSS);\n");

    #Total number of Multiplexers per side
    total_number_of_multiplexers = 0;
    for x in range (len(L)):
        total_number_of_multiplexers = int(total_number_of_multiplexers + int(number_of_tracks_per_segment[x])/int(L[x]));

    
    
    print("\t input clk;")
    print("\t input en;")
    print("\t input rst;")
    print("\t input d;")
    to_print = f"\t input            [0:{number_of_left_inputs-1}] left_in;";
    print(to_print);
    to_print = f"\t output           [0:{number_of_left_outputs-1}] left_out;";
    print(to_print);
    to_print = f"\t input            [0:{number_of_right_inputs-1}] right_in;";
    print(to_print);
    to_print = f"\t output           [0:{number_of_right_outputs-1}] right_out;";
    print(to_print);
    to_print = f"\t input            [0:{number_of_bottom_inputs-1}] bottom_in;";
    print(to_print);
    to_print = f"\t output           [0:{number_of_bottom_outputs-1}] bottom_out;";
    print(to_print);
    to_print = f"\t input            [0:{number_of_top_inputs-1}] top_in;";
    print(to_print);
    to_print = f"\t output           [0:{number_of_top_outputs-1}] top_out;";
    print(to_print);
    to_print = f"\t wire            [0:{total_number_of_multiplexers-1}] s0_left;";
    print(to_print);
    to_print = f"\t wire            [0:{total_number_of_multiplexers-1}] s1_left;";
    print(to_print);
    to_print = f"\t wire            [0:{total_number_of_multiplexers-1}] s0_right;";
    print(to_print);
    to_print = f"\t wire            [0:{total_number_of_multiplexers-1}] s1_right;";
    print(to_print);
    to_print = f"\t wire            [0:{total_number_of_multiplexers-1}] s0_top;";
    print(to_print);
    to_print = f"\t wire            [0:{total_number_of_multiplexers-1}] s1_top;";
    print(to_print);
    to_print = f"\t wire            [0:{total_number_of_multiplexers-1}] s0_bottom;";
    print(to_print);
    to_print = f"\t wire            [0:{total_number_of_multiplexers-1}] s1_bottom;";
    print(to_print);
    
    to_print = f"Switch_Block_W{int(W/2)} switch_block("
    print(to_print)
    to_print = f".left_in(left_in),"
    print(to_print)
    to_print = f".left_out(left_out),"
    print(to_print)
    to_print = f".right_in(right_in),"
    print(to_print)
    to_print = f".right_out(right_out),"
    print(to_print)
    to_print = f".bottom_in(bottom_in),"
    print(to_print)
    to_print = f".bottom_out(bottom_out),"
    print(to_print)
    to_print = f".top_in(top_in),"
    print(to_print)
    to_print = f".top_out(top_out),"
    print(to_print)
    to_print = f".s0_left(s0_left),"
    print(to_print)
    to_print = f".s1_left(s1_left),"
    print(to_print)
    to_print = f".s0_right(s0_right),"
    print(to_print)
    to_print = f".s1_right(s1_right),"
    print(to_print)
    to_print = f".s0_top(s0_top),"
    print(to_print)
    to_print = f".s1_top(s1_top),"
    print(to_print)
    to_print = f".s0_bottom(s0_bottom),"
    print(to_print)
    to_print = f".s1_bottom(s1_bottom));"
    print(to_print)

    print("\n")
    to_print = f"dff_config_bits dff_config_bits0("
    print(to_print)
    print(".clk(clk),")
    print(".en(en),")
    print(".rst(rst),")
    print(".d(d),")
    print(".s0_left(s0_left),");
    print(".s1_left(s1_left),");
    print(".s0_right(s0_right),");
    print(".s1_right(s1_right),");
    print(".s0_bottom(s0_bottom),");
    print(".s1_bottom(s1_bottom),");
    print(".s0_top(s0_top),");
    print(".s1_top(s1_top));");
    print("endmodule")


def generate_switch_block_rtl():
    to_print = f"module Switch_Block_W{int(W/2)}("
    print(to_print)

    number_of_muxes_per_LT_input = 0
    for i in reversed (range (0,W,2)):
        #print(i)
        number_of_muxes_per_LT_input += 1;
        #print("                       left_in,")
        #print("                       right_out,")

    #print(number_of_muxes_per_LT_input)
    number_of_left_inputs = number_of_muxes_per_LT_input;
    number_of_left_outputs = W-number_of_left_inputs;
    number_of_right_outputs = number_of_left_inputs;
    number_of_right_inputs = number_of_left_outputs;
    number_of_top_inputs = number_of_left_outputs;
    number_of_top_outputs = number_of_left_inputs;
    number_of_bottom_inputs = number_of_top_outputs;
    number_of_bottom_outputs = number_of_top_inputs;

    #to_print = f"LO:   {number_of_left_outputs}";
    #print(to_print);
    #to_print = f"LI:   {number_of_left_inputs}";
    #print(to_print);
    #to_print = f"RO:   {number_of_right_outputs}";
    #print(to_print);
    #to_print = f"RI:   {number_of_right_inputs}";
    #print(to_print);
    #to_print = f"TO:   {number_of_top_outputs}";
    #print(to_print);
    #to_print = f"TI:   {number_of_top_inputs}";
    #print(to_print);
    #to_print = f"BO:   {number_of_bottom_outputs}";
    #print(to_print);
    #to_print = f"BI:   {number_of_bottom_inputs}";
    #print(to_print);

    print("                       left_in,");
    print("                       left_out,");
    print("                       right_in,");
    print("                       right_out,");
    print("                       bottom_in,");
    print("                       bottom_out,");
    print("                       top_in,");
    print("                       top_out,");
    print("                       s0_left,");
    print("                       s1_left,");
    print("                       s0_right,");
    print("                       s1_right,");
    print("                       s0_bottom,");
    print("                       s1_bottom,");
    print("                       s0_top,");
    print("                       s1_top);");
    #print("                       VDD,");
    #print("                       VSS);\n");

    #Total number of Multiplexers per side
    total_number_of_multiplexers = 0;
    for x in range (len(L)):
        total_number_of_multiplexers = int(total_number_of_multiplexers + int(number_of_tracks_per_segment[x])/int(L[x]));

    
    
    to_print = f"\t input            [0:{number_of_left_inputs-1}] left_in;";
    print(to_print);
    to_print = f"\t output           [0:{number_of_left_outputs-1}] left_out;";
    print(to_print);
    to_print = f"\t input            [0:{number_of_right_inputs-1}] right_in;";
    print(to_print);
    to_print = f"\t output           [0:{number_of_right_outputs-1}] right_out;";
    print(to_print);
    to_print = f"\t input            [0:{number_of_bottom_inputs-1}] bottom_in;";
    print(to_print);
    to_print = f"\t output           [0:{number_of_bottom_outputs-1}] bottom_out;";
    print(to_print);
    to_print = f"\t input            [0:{number_of_top_inputs-1}] top_in;";
    print(to_print);
    to_print = f"\t output           [0:{number_of_top_outputs-1}] top_out;";
    print(to_print);
    to_print = f"\t input            [0:{total_number_of_multiplexers-1}] s0_left;";
    print(to_print);
    to_print = f"\t input            [0:{total_number_of_multiplexers-1}] s1_left;";
    print(to_print);
    to_print = f"\t input            [0:{total_number_of_multiplexers-1}] s0_right;";
    print(to_print);
    to_print = f"\t input            [0:{total_number_of_multiplexers-1}] s1_right;";
    print(to_print);
    to_print = f"\t input            [0:{total_number_of_multiplexers-1}] s0_top;";
    print(to_print);
    to_print = f"\t input            [0:{total_number_of_multiplexers-1}] s1_top;";
    print(to_print);
    to_print = f"\t input            [0:{total_number_of_multiplexers-1}] s0_bottom;";
    print(to_print);
    to_print = f"\t input            [0:{total_number_of_multiplexers-1}] s1_bottom;";
    print(to_print);
    #print("\t inout            VDD;");
    #print("\t inout            VSS; \n");

    #print("\t //Buffered Input Wires");
    #to_print = f"\t wire \t [0:{number_of_left_inputs-1}] left_in_b;";
    #print(to_print);
    #to_print = f"\t wire \t [0:{number_of_right_inputs-1}] right_in_b;";
    #print(to_print);
    #to_print = f"\t wire \t [0:{number_of_bottom_inputs-1}] bottom_in_b;";
    #print(to_print);
    #to_print = f"\t wire \t [0:{number_of_top_inputs-1}] top_in_b; \n";
    #print(to_print);

    #print("\t //Unbuffered Input Wires");
    #to_print = f"\t wire \t [0:{number_of_left_outputs-1}] left_out_ub;";
    #print(to_print);
    #to_print = f"\t wire \t [0:{number_of_right_outputs-1}] right_out_ub;";
    #print(to_print);
    #to_print = f"\t wire \t [0:{number_of_bottom_outputs-1}] bottom_out_ub;";
    #print(to_print);
    #to_print = f"\t wire \t [0:{number_of_top_outputs-1}] top_out_ub; \n";
    #print(to_print);

    #print("\t //Input Buffers");
    #to_print = f"\t assign left_in_b[0:{number_of_left_inputs-1}] = ~ left_in[0:{number_of_left_inputs-1}];";
    #print(to_print);
    #to_print = f"\t assign right_in_b[0:{number_of_right_inputs-1}] = ~ right_in[0:{number_of_right_inputs-1}];";
    #print(to_print);
    #to_print = f"\t assign top_in_b[0:{number_of_top_inputs-1}] = ~ top_in[0:{number_of_top_inputs-1}];";
    #print(to_print);
    #to_print = f"\t assign bottom_in_b[0:{number_of_bottom_inputs-1}] = ~ bottom_in[0:{number_of_bottom_inputs-1}];";
    #print(to_print);

    #print("\t //Input Buffers");
    #for x in range (number_of_left_inputs):
    #    to_print = f"\t INVxp33_ASAP7_75t_R li{x}(.A (left_in[{x}]), .Y (left_in_b[{x}]));";
    #    print(to_print);
    #for x in range (number_of_top_inputs):
    #    to_print = f"\t INVxp33_ASAP7_75t_R ti{x}(.A (top_in[{x}]), .Y (top_in_b[{x}]));";
    #    print(to_print);
    #for x in range (number_of_bottom_inputs):
    #    to_print = f"\t INVxp33_ASAP7_75t_R bi{x}(.A (bottom_in[{x}]), .Y (bottom_in_b[{x}]));";
    #    print(to_print);
    #for x in range (number_of_right_inputs):
    #    to_print = f"\t INVxp33_ASAP7_75t_R ri{x}(.A (right_in[{x}]), .Y (right_in_b[{x}]));";
    #    print(to_print);
    
    number_of_L1_tracks = 0;

    for x in range (len(L)):
        if (int(L[x]) == 1):
            number_of_L1_tracks = number_of_tracks_per_segment[x];
    #print(number_of_L1_tracks);

    left_tracks_inputs = [];
    right_tracks_inputs = [];
    bottom_tracks_inputs = [];
    top_tracks_inputs = [];

    for x in range (int(number_of_L1_tracks)):
        track = f"left_in[{x}]";
        left_tracks_inputs.append(track);
        track = f"right_in[{x}]";
        right_tracks_inputs.append(track);
        track = f"top_in[{x}]";
        top_tracks_inputs.append(track);
        track = f"bottom_in[{x}]";
        bottom_tracks_inputs.append(track);
    
    #print(left_tracks_inputs);
    #print(right_tracks_inputs);
    #print(bottom_tracks_inputs);
    #print(top_tracks_inputs);

    starting_track_number = 0;
    ending_track_number = -1;

    current_right_mux = 0;
    current_left_mux = 0;
    current_top_mux = 0;
    current_bottom_mux = 0;

    #L=1
    to_print = f"\n \t //L = 1 Tracks";
    print (to_print);
    for x in range (len(L)):
        if (int (L[x])==1):
            number_of_L1_tracks = int (number_of_tracks_per_segment[x]);
    if (number_of_L1_tracks != 0):
        # Left Muxes
        for t in range (number_of_L1_tracks):
            d0 = int(W/2) - t;
            d1 = t;
            d2 = int(W/2) + t - 1;

            to_print = f"\t left_mux3 \t left_mux_{t} \t (";
            print(to_print);
            to_print = f"\t \t \t \t \t \t .d0 ({top_tracks_inputs[d0%len(top_tracks_inputs)]}),";
            print(to_print);
            to_print = f"\t \t \t \t \t \t .d1 ({right_tracks_inputs[d1%len(right_tracks_inputs)]}),";
            print(to_print);
            to_print = f"\t \t \t \t \t \t .d2 ({bottom_tracks_inputs[d2%len(bottom_tracks_inputs)]}),";
            print(to_print);
            to_print = f"\t \t \t \t \t \t .s0 (s0_left[{t}]),";
            print(to_print);
            to_print = f"\t \t \t \t \t \t .s1 (s1_left[{t}]),";
            print(to_print);
            to_print = f"\t \t \t \t \t \t .y (left_out[{t}]));";
            print(to_print);
            #to_print = f"\t \t \t \t \t \t .VDD (VDD),";
            #print(to_print);
            #to_print = f"\t \t \t \t \t \t .VSS (VSS));";
            #print(to_print);

            current_left_mux = current_left_mux + 1;

        # Right Muxes
        for t in range (number_of_L1_tracks):
            d0 = int(W/2) + t - 1;
            d1 = t;
            d2 = int(W/2) - t - 2;

            to_print = f"\t right_mux3 \t right_mux_{t} \t (";
            print(to_print);
            to_print = f"\t \t \t \t \t \t .d0 ({top_tracks_inputs[d0%len(top_tracks_inputs)]}),";
            print(to_print);
            to_print = f"\t \t \t \t \t \t .d1 ({left_tracks_inputs[d1%len(left_tracks_inputs)]}),";
            print(to_print);
            to_print = f"\t \t \t \t \t \t .d2 ({bottom_tracks_inputs[d2%len(bottom_tracks_inputs)]}),";
            print(to_print);
            to_print = f"\t \t \t \t \t \t .s0 (s0_left[{t}]),";
            print(to_print);
            to_print = f"\t \t \t \t \t \t .s1 (s1_left[{t}]),";
            print(to_print);
            to_print = f"\t \t \t \t \t \t .y (right_out[{t}]));";
            print(to_print);
            #to_print = f"\t \t \t \t \t \t .VDD (VDD),";
            #print(to_print);
            #to_print = f"\t \t \t \t \t \t .VSS (VSS));";
            #print(to_print);

            current_right_mux = current_right_mux + 1;
        
        # Top Muxes
        for t in range(number_of_L1_tracks):
            d0 = int(W/2) - t;
            d1 = t;
            d2 = int(W/2) + t + 1;
            to_print = f"\t top_mux3 \t top_mux_{t} \t (";
            print(to_print);
            to_print = f"\t \t \t \t \t \t .d0 ({left_tracks_inputs[d0%len(left_tracks_inputs)]}),";
            print(to_print);
            to_print = f"\t \t \t \t \t \t .d1 ({bottom_tracks_inputs[d1%len(bottom_tracks_inputs)]}),";
            print(to_print);
            to_print = f"\t \t \t \t \t \t .d2 ({right_tracks_inputs[d2%len(right_tracks_inputs)]}),";
            print(to_print);
            to_print = f"\t \t \t \t \t \t .s0 (s0_top[{t}]),";
            print(to_print);
            to_print = f"\t \t \t \t \t \t .s1 (s1_top[{t}]),";
            print(to_print);
            to_print = f"\t \t \t \t \t \t .y (top_out[{t}]));";
            print(to_print);
            #to_print = f"\t \t \t \t \t \t .VDD (VDD),";
            #print(to_print);
            #to_print = f"\t \t \t \t \t \t .VSS (VSS));";
            #print(to_print);

            current_top_mux = current_top_mux + 1;

        for t in range(number_of_L1_tracks):
            d0 = int(W/2) + t + 1;
            d1 = t
            d2 = int(W/2) - t - 2;
            to_print = f"\t bottom_mux3 \t bottom_mux_{t} \t (";
            print(to_print);
            to_print = f"\t \t \t \t \t \t .d0 ({left_tracks_inputs[d0%len(left_tracks_inputs)]}),";
            print(to_print);
            to_print = f"\t \t \t \t \t \t .d1 ({top_tracks_inputs[d1%len(top_tracks_inputs)]}),";
            print(to_print);
            to_print = f"\t \t \t \t \t \t .d2 ({right_tracks_inputs[d2%len(right_tracks_inputs)]}),";
            print(to_print);
            to_print = f"\t \t \t \t \t \t .s0 (s0_bottom[{t}]),";
            print(to_print);
            to_print = f"\t \t \t \t \t \t .s1 (s1_bottom[{t}]),";
            print(to_print);
            to_print = f"\t \t \t \t \t \t .y (bottom_out[{t}]));";
            print(to_print);
            #to_print = f"\t \t \t \t \t \t .VDD (VDD),";
            #print(to_print);
            #to_print = f"\t \t \t \t \t \t .VSS (VSS));";
            #print(to_print);

            current_bottom_mux = current_bottom_mux + 1;

        ending_track_number = number_of_L1_tracks-1;
    # L>1 Tracks    
    left_input_tracks = [];
    right_input_tracks = [];
    top_input_tracks = [];
    bottom_input_tracks = [];
    left_output_tracks = [];
    right_output_tracks = [];
    top_output_tracks = [];
    bottom_output_tracks = [];
    seg_left_output_tracks = [];
    seg_right_output_tracks = [];
    seg_top_output_tracks = [];
    seg_bottom_output_tracks = [];

    for x in range (len(L)):
        #print(len(L))
        if (int(L[x]) != 1):
            current_length = int(L[x]);
            starting_track_number = ending_track_number + 1;
            current_number_of_tracks = int(number_of_tracks_per_segment[x]);
            ending_track_number = starting_track_number + int(number_of_tracks_per_segment[x])-1;
            #print (starting_track_number)
            left_input_tracks = [];
            right_input_tracks = [];
            top_input_tracks = [];
            bottom_input_tracks = [];
            left_output_tracks = [];
            right_output_tracks = [];
            top_output_tracks = [];
            bottom_output_tracks = [];
            seg_left_output_tracks = [];
            seg_right_output_tracks = [];
            seg_top_output_tracks = [];
            seg_bottom_output_tracks = [];
            for t in range (starting_track_number,ending_track_number+1):
                track = f"left_in[{t}]";
                left_input_tracks.append(track);
                track = f"right_in[{t}]";
                right_input_tracks.append(track);
                track = f"top_in[{t}]";
                top_input_tracks.append(track);
                track = f"bottom_in[{t}]";
                bottom_input_tracks.append(track);
                track = f"left_out[{t}]";
                left_output_tracks.append(track);
                track = f"right_out[{t}]";
                right_output_tracks.append(track);
                track = f"top_out[{t}]";
                top_output_tracks.append(track);
                track = f"bottom_out[{t}]";
                bottom_output_tracks.append(track);
            #print (ending_track_number);

            #number_of_multiplexers = len(left_input_tracks)/current_length;
            #for y in range (number_of_multiplexers):
            #    temp.append(left_input_tracks[(y+1)%len(left_input_tracks)]);
                

            # for x in range (len(right_output_tracks)):
            #     if (x%int(current_length)==0):
            #         to_print = f"assign right_out_ub[{x+starting_track_number}] = left_in_b[{x+starting_track_number+current_length-1}]";
            #         print(to_print);
            #     else:
            #         to_print = f"assign right_out_ub[{x+starting_track_number}] = left_in_b[{x+starting_track_number-1}]";
            #         print(to_print);

            # Right Track Shifting
            to_print = f"\n \t //L = {current_length} Tracks";
            print (to_print);
            for x in range (len(right_output_tracks)):
                if (x%int(current_length)==0):
                    #to_print = f"\t assign \t right_out_ub[{x+starting_track_number}] = left_in_b[{x+starting_track_number+current_length-1}];";
                    #print(to_print);
                    to_print = f"\t right_mux3 \t right_mux_{current_right_mux} \t (";
                    print(to_print);
                    to_print = f"\t \t \t \t \t \t .d0 (top_in[{x+starting_track_number+current_length-1}]),";
                    print(to_print);
                    to_print = f"\t \t \t \t \t \t .d1 (left_in[{x+starting_track_number+current_length-1}]),";
                    print(to_print);
                    to_print = f"\t \t \t \t \t \t .d2 (bottom_in[{x+starting_track_number+current_length-1}]),";
                    print(to_print);
                    to_print = f"\t \t \t \t \t \t .s0 (s0_right[{current_right_mux}]),";
                    print(to_print);
                    to_print = f"\t \t \t \t \t \t .s1 (s1_right[{current_right_mux}]),";
                    print(to_print);
                    to_print = f"\t \t \t \t \t \t .y (right_out[{x+starting_track_number}]),";
                    print(to_print);
                    #to_print = f"\t \t \t \t \t \t .VDD (VDD),";
                    #print(to_print);
                    #to_print = f"\t \t \t \t \t \t .VSS (VSS));";
                    #print(to_print);

                    current_right_mux = current_right_mux + 1;
                else:
                    to_print = f"\t assign \t right_out[{x+starting_track_number}] = left_in[{x+starting_track_number-1}];";
                    print(to_print);
            
            #Left Track Shifting
            for x in range (len(left_output_tracks)):
                if (x%int(current_length)==0):
                    #to_print = f"\t assign \t right_out_ub[{x+starting_track_number}] = left_in_b[{x+starting_track_number+current_length-1}];";
                    #print(to_print);
                    to_print = f"\t left_mux3 \t left_mux_{current_left_mux} \t (";
                    print(to_print);
                    to_print = f"\t \t \t \t \t \t .d0 (top_in[{x+starting_track_number+current_length-1}]),";
                    print(to_print);
                    to_print = f"\t \t \t \t \t \t .d1 (right_in[{x+starting_track_number+current_length-1}]),";
                    print(to_print);
                    to_print = f"\t \t \t \t \t \t .d2 (bottom_in[{x+starting_track_number+current_length-1}]),";
                    print(to_print);
                    to_print = f"\t \t \t \t \t \t .s0 (s0_left[{current_left_mux}]),";
                    print(to_print);
                    to_print = f"\t \t \t \t \t \t .s1 (s1_left[{current_left_mux}]),";
                    print(to_print);
                    to_print = f"\t \t \t \t \t \t .y (left_out[{x+starting_track_number}]),";
                    print(to_print);
                    #to_print = f"\t \t \t \t \t \t .VDD (VDD),";
                    #print(to_print);
                    #to_print = f"\t \t \t \t \t \t .VSS (VSS));";
                    #print(to_print);

                    current_left_mux = current_left_mux + 1;
                else:
                    to_print = f"\t assign \t left_out[{x+starting_track_number}] = right_in[{x+starting_track_number-1}];";
                    print(to_print);
            
            #Top Track Shifting
            for x in range (len(top_output_tracks)):
                if (x%int(current_length)==0):
                    #to_print = f"\t assign \t right_out_ub[{x+starting_track_number}] = left_in_b[{x+starting_track_number+current_length-1}];";
                    #print(to_print);
                    to_print = f"\t top_mux3 \t top_mux_{current_top_mux} \t (";
                    print(to_print);
                    to_print = f"\t \t \t \t \t \t .d0 (left_in[{x+starting_track_number+current_length-1}]),";
                    print(to_print);
                    to_print = f"\t \t \t \t \t \t .d1 (bottom_in[{x+starting_track_number+current_length-1}]),";
                    print(to_print);
                    to_print = f"\t \t \t \t \t \t .d2 (right_in[{x+starting_track_number+current_length-1}]),";
                    print(to_print);
                    to_print = f"\t \t \t \t \t \t .s0 (s0_left[{current_top_mux}]),";
                    print(to_print);
                    to_print = f"\t \t \t \t \t \t .s1 (s1_left[{current_top_mux}]),";
                    print(to_print);
                    to_print = f"\t \t \t \t \t \t .y (top_out[{x+starting_track_number}]),";
                    print(to_print);
                    #to_print = f"\t \t \t \t \t \t .VDD (VDD),";
                    #print(to_print);
                    #to_print = f"\t \t \t \t \t \t .VSS (VSS));";
                    #print(to_print);
                
                    current_top_mux = current_top_mux + 1;
                else:
                    to_print = f"\t assign \t top_out[{x+starting_track_number}] = bottom_in[{x+starting_track_number-1}];";
                    print(to_print);

            #Bottom Track Shifting
            for x in range (len(bottom_output_tracks)):
                if (x%int(current_length)==0):
                    #to_print = f"\t assign \t right_out_ub[{x+starting_track_number}] = left_in_b[{x+starting_track_number+current_length-1}];";
                    #print(to_print);
                    to_print = f"\t bottom_mux3 \t bottom_mux_{current_bottom_mux} \t (";
                    print(to_print);
                    to_print = f"\t \t \t \t \t \t .d0 (left_in[{x+starting_track_number+current_length-1}]),";
                    print(to_print);
                    to_print = f"\t \t \t \t \t \t .d1 (top_in[{x+starting_track_number+current_length-1}]),";
                    print(to_print);
                    to_print = f"\t \t \t \t \t \t .d2 (right_in[{x+starting_track_number+current_length-1}]),";
                    print(to_print);
                    to_print = f"\t \t \t \t \t \t .s0 (s0_bottom[{current_top_mux}]),";
                    print(to_print);
                    to_print = f"\t \t \t \t \t \t .s1 (s1_bottom[{current_top_mux}]),";
                    print(to_print);
                    to_print = f"\t \t \t \t \t \t .y (bottom_out[{x+starting_track_number}]),";
                    print(to_print);
                    #to_print = f"\t \t \t \t \t \t .VDD (VDD),";
                    #print(to_print);
                    #to_print = f"\t \t \t \t \t \t .VSS (VSS));";
                    #print(to_print);

                    current_bottom_mux = current_bottom_mux + 1;
                else:
                    to_print = f"\t assign \t bottom_out[{x+starting_track_number}] = top_in[{x+starting_track_number-1}];";
                    print(to_print);

    #print("\t //Output Buffers");
    #for x in range (number_of_left_outputs):
    #    to_print = f"\t INVxp33_ASAP7_75t_R lo{x}(.A (left_out_ub[{x}]), .Y (left_out[{x}]));";
    #    print(to_print);
    #for x in range (number_of_top_outputs):
    #    to_print = f"\t INVxp33_ASAP7_75t_R to{x}(.A (top_out_ub[{x}]), .Y (top_out[{x}]));";
    #    print(to_print);
    #for x in range (number_of_bottom_outputs):
    #    to_print = f"\t INVxp33_ASAP7_75t_R bo{x}(.A (bottom_out_ub[{x}]), .Y (bottom_out[{x}]));";
    #    print(to_print);
    #for x in range (number_of_right_outputs):
    #    to_print = f"\t INVxp33_ASAP7_75t_R ro{x}(.A (right_out_ub[{x}]), .Y (right_out[{x}]));";
    #    print(to_print);

    print ("endmodule");

            #print (left_input_tracks);
            #print (right_output_tracks)

    #print(starting_track_number);



if __name__ == "__main__":
    W = int(get_args());
    generate_mux_rtl();
    generate_config_bits();
    generate_switch_block_wrapper();
    generate_switch_block_rtl();

