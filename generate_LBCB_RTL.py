import math;
import sys;
import os;

with open("arch.txt", "r") as arch_file:
    k = (arch_file.readline())
    N = (arch_file.readline())
    W = (arch_file.readline());
    Fcin = (arch_file.readline());
    Fcout = (arch_file.readline());
arch_file.close();

k = int(k)
N = int(N)
W = int(W);
Fcin = float(Fcin)
Fcout = float(Fcout)
I = math.ceil((k/2)*(N+1));

#Mux2 Module
def create_mux2():
  #Mux2
    print ("module mux2(d0, d1, s, y);")
    print ("  input  d0, d1, s;")
    print ("  output y;")
    print ("  assign y = s ? d1 : d0;")
    print ("endmodule")
    print ("\n")
    print("\n");

#Mux4 Module
def create_mux4():
  print("module mux4(d0, d1, d2, d3, s0, s1, y);");
  print("\t input d0, d1, d2, d3, s0, s1;");
  print("\t output y;");
  #print("\t wire d0, d1, d2, d3, s0, s1;");
  #print("\t wire y;");
  print("\t wire mux2_0_w, mux2_1_w;");
  print("\t mux2 mux2_0 (.d0 (d0), .d1 (d1), .s (s0), .y (mux2_0_w));");
  print("\t mux2 mux2_1 (.d0 (d2), .d1 (d3), .s (s0), .y (mux2_1_w));");
  print("\t mux2 mux2_2 (.d0 (mux2_0_w), .d1 (mux2_1_w), .s (s1), .y (y));");
  print("endmodule");
  print("\n");

#DFF with enable and reset
def create_DFF():
  print("module DFF_EN (clk, d, rst, en, q);");
  print("input clk, d, rst, en;");
  print("output reg q;");
  print("always @(posedge clk or posedge rst)");
  print("    if (rst)");
  print("        q <= 1'b0;");
  print("    else if (en)");
  print("    q <= d;");
  print ("endmodule");

#Local Routing Multiplexer Module
def create_rmux():
  number_of_rmux_inputs = I + N;
  number_of_rmux = k*N;
  number_of_rmux_select_lines = math.ceil(math.log(number_of_rmux_inputs,10)/math.log(2,10));
  

  #print(number_of_rmux_select_lines);
  #print(number_of_rmux_inputs);

  remainder = number_of_rmux_inputs%2;

  #Rmux module
  print("module rmux (");
  for x in range (number_of_rmux_inputs):
    to_print = f"\t d{x},";
    print(to_print);
  for x in range (number_of_rmux_select_lines):
    to_print = f"\t s{x},";
    print(to_print);
  print("\t y);");

  for x in range (number_of_rmux_inputs):
    to_print = f"\t input d{x};";
    print(to_print);
  for x in range (number_of_rmux_select_lines):
    to_print = f"\t input s{x};";
    print(to_print);
  print("\t output y;");

  stage_outputs = [];
  current_stage = 0;
  #stage 0
  for x in range (0,number_of_rmux_inputs,2):
    if (x == number_of_rmux_inputs-3):
      to_print = f"\t mux2 st{current_stage}_rmux_{int(x/2)} (";
      print(to_print);
      to_print = f"\t .d0 (d{x}),";
      print(to_print);
      x = x+1;
      to_print = f"\t .d1 (d{x}),";
      print(to_print);
      x= x+1;
      to_print = f"\t .s (s{current_stage}),";
      print(to_print);
      stage_output = f"st{current_stage}_rmux_{int(x/2)-1}_y";
      to_print = f"\t .y ({stage_output}));";
      print(to_print);
      stage_outputs .append(stage_output);
      break;
    else:
      to_print = f"\t mux2 st{current_stage}_rmux_{int(x/2)} (";
      print(to_print);
      to_print = f"\t .d0 (d{x}),";
      print(to_print);
      x = x+1;
      to_print = f"\t .d1 (d{x}),";
      print(to_print);
      x= x+1;
      to_print = f"\t .s (s{current_stage}),";
      print(to_print);
      stage_output = f"st{current_stage}_rmux_{int(x/2)-1}_y";
      to_print = f"\t .y ({stage_output}));";
      print(to_print);
      stage_outputs .append(stage_output);
      #x=x+1;
  if(remainder !=0):
    stage_outputs.append(f"d{number_of_rmux_inputs-1}");

  #print(stage_outputs);

  while (len(stage_outputs)>1):
    stage_inputs = stage_outputs;
    current_stage = current_stage + 1;
    stage_outputs = [];

    remainder = len(stage_inputs)%2;

    #print(stage_inputs)

    if (remainder == 0):
      for x in range(0, len(stage_inputs),2):
        to_print = f"\t mux2 st{current_stage}_rmux_{int(x/2)} (";
        print(to_print);
        to_print = f"\t .d0 ({stage_inputs[x]}),";
        print(to_print);
        x = x+1;
        to_print = f"\t .d1 ({stage_inputs[x]}),";
        print(to_print);
        to_print = f"\t .s (s{current_stage}),";
        print(to_print);
        stage_output = f"st{current_stage}_rmux_{int(x/2)}_y";
        to_print = f"\t .y ({stage_output}));";
        print(to_print);
        stage_outputs .append(stage_output);
    else:
      for x in range(0, len(stage_inputs)-1,2):
        to_print = f"\t mux2 st{current_stage}_rmux_{int(x/2)} (";
        print(to_print);
        to_print = f"\t .d0 ({stage_inputs[x]}),";
        print(to_print);
        x = x+1;
        to_print = f"\t .d1 ({stage_inputs[x]}),";
        print(to_print);
        to_print = f"\t .s (s{current_stage}),";
        print(to_print);
        stage_output = f"st{current_stage}_rmux_{int(x/2)}_y";
        to_print = f"\t .y ({stage_output}));";
        print(to_print);
        stage_outputs .append(stage_output);
      stage_outputs.append(f"{stage_inputs[len(stage_inputs)-1]}");
  to_print = f"assign y = {stage_outputs[len(stage_outputs)-1]};";
  print(to_print);
  print("endmodule \n");

#Connection block Multiplexer Module
def create_cbmux():
  number_of_cbmux_inputs = math.ceil(Fcin*W);
  number_of_cbmux = k*N;
  number_of_cbmux_select_lines = math.ceil(math.log(number_of_cbmux_inputs,10)/math.log(2,10));
  

  #print(number_of_rmux_select_lines);
  #print(number_of_rmux_inputs);

  remainder = number_of_cbmux_inputs%2;

  #cbmux module
  print("module cbmux (");
  for x in range (number_of_cbmux_inputs):
    to_print = f"\t d{x},";
    print(to_print);
  for x in range (number_of_cbmux_select_lines):
    to_print = f"\t s{x},";
    print(to_print);
  print("\t y);");

  for x in range (number_of_cbmux_inputs):
    to_print = f"\t input d{x};";
    print(to_print);
  for x in range (number_of_cbmux_select_lines):
    to_print = f"\t input s{x};";
    print(to_print);
  print("\t output y;");

  stage_outputs = [];
  current_stage = 0;
  #stage 0
  for x in range (0,number_of_cbmux_inputs,2):
    if (x == number_of_cbmux_inputs-3):
      to_print = f"\t mux2 st{current_stage}_cbmux_{int(x/2)} (";
      print(to_print);
      to_print = f"\t .d0 (d{x}),";
      print(to_print);
      x = x+1;
      to_print = f"\t .d1 (d{x}),";
      print(to_print);
      x= x+1;
      to_print = f"\t .s (s{current_stage}),";
      print(to_print);
      stage_output = f"st{current_stage}_cbmux_{int(x/2)-1}_y";
      to_print = f"\t .y ({stage_output}));";
      print(to_print);
      stage_outputs .append(stage_output);
      break;
    else:
      to_print = f"\t mux2 st{current_stage}_cbmux_{int(x/2)} (";
      print(to_print);
      to_print = f"\t .d0 (d{x}),";
      print(to_print);
      x = x+1;
      to_print = f"\t .d1 (d{x}),";
      print(to_print);
      x= x+1;
      to_print = f"\t .s (s{current_stage}),";
      print(to_print);
      stage_output = f"st{current_stage}_cbmux_{int(x/2)-1}_y";
      to_print = f"\t .y ({stage_output}));";
      print(to_print);
      stage_outputs .append(stage_output);
      #x=x+1;
  if(remainder !=0):
    stage_outputs.append(f"d{number_of_cbmux_inputs-1}");

  #print(stage_outputs);

  while (len(stage_outputs)>1):
    stage_inputs = stage_outputs;
    current_stage = current_stage + 1;
    stage_outputs = [];

    remainder = len(stage_inputs)%2;

    #print(stage_inputs)

    if (remainder == 0):
      for x in range(0, len(stage_inputs),2):
        to_print = f"\t mux2 st{current_stage}_cbmux_{int(x/2)} (";
        print(to_print);
        to_print = f"\t .d0 ({stage_inputs[x]}),";
        print(to_print);
        x = x+1;
        to_print = f"\t .d1 ({stage_inputs[x]}),";
        print(to_print);
        to_print = f"\t .s (s{current_stage}),";
        print(to_print);
        stage_output = f"st{current_stage}_cbmux_{int(x/2)}_y";
        to_print = f"\t .y ({stage_output}));";
        print(to_print);
        stage_outputs .append(stage_output);
    else:
      for x in range(0, len(stage_inputs)-1,2):
        to_print = f"\t mux2 st{current_stage}_cbmux_{int(x/2)} (";
        print(to_print);
        to_print = f"\t .d0 ({stage_inputs[x]}),";
        print(to_print);
        x = x+1;
        to_print = f"\t .d1 ({stage_inputs[x]}),";
        print(to_print);
        to_print = f"\t .s (s{current_stage}),";
        print(to_print);
        stage_output = f"st{current_stage}_cbmux_{int(x/2)}_y";
        to_print = f"\t .y ({stage_output}));";
        print(to_print);
        stage_outputs .append(stage_output);
      stage_outputs.append(f"{stage_inputs[len(stage_inputs)-1]}");
  to_print = f"assign y = {stage_outputs[len(stage_outputs)-1]};";
  print(to_print);
  print("endmodule \n");

#BLE Module
def create_BLE():
  number_of_data_inputs = 2**k;
  to_print = f"module BLE{k} (";
  print(to_print);

  #Data inputs from SRAMs
  for x in range(number_of_data_inputs):
    to_print = f"\t d{x},";
    print(to_print);

  #Select lines
  for x in range(k):
    to_print = f"\t s{x},";
    print(to_print);

  #Clock
  print ("\t clk,");

  #Reset and Enable
  print ("\t rst,");
  print ("\t en,");

  #Out mux Select Line
  print ("\t sout,");

  #Output
  print("\t y);");


  #Define IOs
  for x in range(number_of_data_inputs):
    to_print = f"\t input d{x};";
    print(to_print);

  for x in range(k):
    to_print = f"\t input s{x};";
    print(to_print);

  print("\t input clk;");
  print("\t input rst;");
  print("\t input en;");
  print("\t input sout;");
  print("\t output y;");

  print("\t wire y_lut;");
  print("\t wire y_DFF;");


  number_of_stages = k;
  number_of_mux4_per_stage = [];
  last_mux_is_mux2 = False;
  number_of_stage_outputs = number_of_data_inputs;

  if (number_of_data_inputs%4 == 0):
    #number_of_mux4 = number_of_data_inputs/4;
    #number_of_mux4_per_stage.append(number_of_mux4);
    #number_of_stage_outputs = number_of_mux4;
    for x in range (int(number_of_stages/2)):
      if (number_of_stage_outputs%4==0):
        number_of_mux4 = number_of_stage_outputs/4;
        number_of_mux4_per_stage.append(number_of_mux4);
        number_of_stage_outputs = number_of_mux4;
      if (number_of_stage_outputs%2==0 and x==int(number_of_stages/2)-1):
        last_mux_is_mux2 = True;

  list_of_data_inputs = [];
  for x in range(number_of_data_inputs):
    add_to_list = f"d{x}";
    list_of_data_inputs.append(add_to_list);

  list_of_select_lines = [];
  for x in range(k):
    add_to_list = f"s{x}";
    list_of_select_lines.append(add_to_list);

  list_of_int_sigs = [];
  for x in range (len(number_of_mux4_per_stage)):
    for y in range (int(number_of_mux4_per_stage[x])):
      add_to_list = f"st{x}_mux4_{y}_y";
      list_of_int_sigs.append(add_to_list);

  if(last_mux_is_mux2):
    add_to_list = f"st{len(number_of_mux4_per_stage)}_mux2_0";
    list_of_int_sigs.append(add_to_list);

  last_int_sig = " ";


  for x in range (len(number_of_mux4_per_stage)):
    i_list_of_data_inputs = 0;
    i_list_of_select_lines = 0;
    i_list_of_int_sigs = 0;
    if (x==0):
      for y in range (int(number_of_mux4_per_stage[x])):
        to_print = f"mux4 st{x}_mux4_{y} (";
        print(to_print);
        to_print = f"\t .d0 ({list_of_data_inputs[i_list_of_data_inputs]}),";
        print(to_print);
        i_list_of_data_inputs = i_list_of_data_inputs + 1;
        to_print = f"\t .d1 ({list_of_data_inputs[i_list_of_data_inputs]}),";
        print(to_print);
        i_list_of_data_inputs = i_list_of_data_inputs + 1;
        to_print = f"\t .d2 ({list_of_data_inputs[i_list_of_data_inputs]}),";
        print(to_print);
        i_list_of_data_inputs = i_list_of_data_inputs + 1;
        to_print = f"\t .d3 ({list_of_data_inputs[i_list_of_data_inputs]}),";
        print(to_print);
        i_list_of_data_inputs = i_list_of_data_inputs + 1;
        to_print = f"\t .s0 ({list_of_select_lines[i_list_of_select_lines]}),";
        print(to_print);
        i_list_of_select_lines = i_list_of_select_lines+1;
        to_print = f"\t .s1 ({list_of_select_lines[i_list_of_select_lines]}),";
        print(to_print);
        to_print = f"\t .y ({list_of_int_sigs[i_list_of_int_sigs]}));";
        print(to_print);
        last_int_sig = f"{list_of_int_sigs[i_list_of_int_sigs]}";
        i_list_of_int_sigs = i_list_of_int_sigs + 1;
        i_list_of_select_lines = x;
    elif (x!=0):
      i_list_of_int_sigs = 0;
      for y in range (int(number_of_mux4_per_stage[x])):
        i_list_of_select_lines = x+1;
        to_print = f"mux4 st{x}_mux4_{y} (";
        print(to_print);
        to_print = f"\t .d0 ({list_of_int_sigs[i_list_of_int_sigs]}),";
        print(to_print);
        i_list_of_int_sigs = i_list_of_int_sigs + 1;
        to_print = f"\t .d1 ({list_of_int_sigs[i_list_of_int_sigs]}),";
        print(to_print);
        i_list_of_int_sigs = i_list_of_int_sigs + 1;
        to_print = f"\t .d2 ({list_of_int_sigs[i_list_of_int_sigs]}),";
        print(to_print);
        i_list_of_int_sigs = i_list_of_int_sigs + 1;
        to_print = f"\t .d3 ({list_of_int_sigs[i_list_of_int_sigs]}),";
        print(to_print);
        i_list_of_int_sigs = i_list_of_int_sigs + 1;
        to_print = f"\t .s0 ({list_of_select_lines[i_list_of_select_lines]}),";
        print(to_print);
        i_list_of_select_lines = i_list_of_select_lines+1;
        to_print = f"\t .s1 ({list_of_select_lines[i_list_of_select_lines]}),";
        print(to_print);  
        #to_print = f"\t .y ({list_of_int_sigs[i_list_of_int_sigs]}),";
        to_print = f"\t .y (st{x}_mux4_{y}_y));";
        #f"st{x}_mux4_{y}_y"
        print(to_print);
        last_int_sig = f"{list_of_int_sigs[i_list_of_int_sigs]}";
        #i_list_of_int_sigs = i_list_of_int_sigs + 1;
        #i_list_of_select_lines = x;
      i_list_of_int_sigs = i_list_of_int_sigs - 4;
  if (last_mux_is_mux2):
    i_list_of_int_sigs = len(list_of_int_sigs) - 3;
    to_print = f"mux2 st{len(number_of_mux4_per_stage)}_mux2_0 (";
    print(to_print);
    to_print = f"\t .d0 ({list_of_int_sigs[i_list_of_int_sigs]}),";
    print(to_print);
    i_list_of_int_sigs = i_list_of_int_sigs + 1;
    to_print = f"\t .d1 ({list_of_int_sigs[i_list_of_int_sigs]}),";
    print(to_print);
    to_print = f"\t .s (s{k-1}),";
    print(to_print);
    to_print = f"\t .y (y_lut));";
    print(to_print);
  else:
    print("\n");
    to_print = f"assign y_lut = {last_int_sig};";
    print(to_print);

  print("\n");
  print ("DFF_EN q_reg(.clk (clk), .d (y_lut), .rst(rst), .en(en), .q (y_DFF));");
  print("\n");

  to_print = f"mux2 out_mux (";
  print(to_print);
  to_print = f"\t .d0 (y_lut),";
  print(to_print);
  to_print = f"\t .d1 (y_DFF),";
  print(to_print);
  to_print = f"\t .s (sout),";
  print(to_print);
  to_print = f"\t .y (y));";
  print(to_print);

  print("endmodule");
  print("\n");

def generate_config_bits():
    to_print = f"module dff_config_bits("
    print(to_print)
    print("clk,")
    #print("en,")
    #print("rst,")
    print("d,")
    total_number_of_BLE_inputs = (2**k)*N;
    total_number_of_BLE_select_lines = k*N;
    number_of_rmux_inputs = I + N;
    total_number_of_rmux_select_lines = math.ceil(math.log(I+N,10)/math.log(2,10)) * k * N;
    total_number_of_rmuxes = k * N;
    number_of_rmux_select_lines = math.ceil(math.log(number_of_rmux_inputs,10)/math.log(2,10));
    ##ADDED
    number_of_tracks_to_LB_inputs = int (Fcin * W);
    number_of_tracks_to_LB_outputs = int (Fcout * W);
    number_of_cbmux_inputs = math.ceil(Fcin*W);
    number_of_cbmux_select_lines = math.ceil(math.log(number_of_cbmux_inputs,10)/math.log(2,10));
    total_number_of_cb_select_lines = number_of_cbmux_select_lines*I;
    total_number_cbmuxes = I;
        #A model for Area-Efficient and Tileable FPGA Tiles
    
    # LUT SRAMs
    for x in range(total_number_of_BLE_inputs):
        to_print = f"\t d{x},";
        print(to_print);

    #Rmux select lines
    for x in range(total_number_of_rmux_select_lines):
        to_print = f"\t s{x},";
        print(to_print);

    #CB Select lines
    for  x in range(total_number_of_cb_select_lines):
        to_print = f"\t s_cb{x},";
        print(to_print);

    for x in range(N):
        to_print = f"\t sout{x},";
        print(to_print);
    print("en,")
    print("rst);")

    print("input clk;")
    print("input d;")

    # LUT SRAMs
    for x in range(total_number_of_BLE_inputs):
        to_print = f"\t inout d{x};";
        print(to_print);

    #Rmux select lines
    for x in range(total_number_of_rmux_select_lines):
        to_print = f"\t inout s{x};";
        print(to_print);

    #CB Select lines
    for  x in range(total_number_of_cb_select_lines):
        to_print = f"\t inout s_cb{x};";
        print(to_print);

    for x in range(N):
        to_print = f"\t inout sout{x};";
        print(to_print);

    print("input en;")
    print("input rst;")

    #LUT SRAMs
    print("\n")
    print("\n")
    to_print=f"DFF_EN config0 (.clk(clk), .d(d), .rst(rst), .en(en), .q(d0));"
    print(to_print)
    current_flop = 1;
    previous_flop =0;
    for x in range (total_number_of_BLE_inputs-1):
        to_print=f"DFF_EN config{x+1} (.clk(clk), .d(d{previous_flop}), .rst(rst), .en(en), .q(d{current_flop}));"
        print(to_print)
        previous_flop = current_flop;
        current_flop += 1;

    #RMUX Select Lines
    to_print=f"DFF_EN config{total_number_of_BLE_inputs} (.clk(clk), .d(d{total_number_of_BLE_inputs-1}), .rst(rst), .en(en), .q(s0));"
    print(to_print)
    current_flop = 1;
    previous_flop =0;
    for x in range (total_number_of_BLE_inputs, total_number_of_BLE_inputs+total_number_of_rmux_select_lines-1):
        to_print=f"DFF_EN config{x+1} (.clk(clk), .d(s{previous_flop}), .rst(rst), .en(en), .q(s{current_flop}));"
        print(to_print)
        previous_flop = current_flop;
        current_flop += 1;

    #CB Select Lines
    to_print=f"DFF_EN config{total_number_of_BLE_inputs+total_number_of_rmux_select_lines} (.clk(clk), .d(s{total_number_of_rmux_select_lines-1}), .rst(rst), .en(en), .q(s_cb0));"
    print(to_print)
    current_flop = 1;
    previous_flop =0;
    for x in range (total_number_of_BLE_inputs+total_number_of_rmux_select_lines, total_number_of_BLE_inputs+total_number_of_rmux_select_lines+total_number_of_cb_select_lines-1):
        to_print=f"DFF_EN config{x+1} (.clk(clk), .d(s_cb{previous_flop}), .rst(rst), .en(en), .q(s_cb{current_flop}));"
        print(to_print)
        previous_flop = current_flop;
        current_flop += 1;

    #Output Muxes Select Lines
    to_print=f"DFF_EN config{total_number_of_BLE_inputs+total_number_of_rmux_select_lines+total_number_of_rmux_select_lines} (.clk(clk), .d(s_cb{total_number_of_cb_select_lines-1}), .rst(rst), .en(en), .q(sout0));"
    print(to_print)
    current_flop = 1;
    previous_flop =0;
    for x in range (total_number_of_BLE_inputs+total_number_of_rmux_select_lines+total_number_of_cb_select_lines, total_number_of_BLE_inputs+total_number_of_rmux_select_lines+total_number_of_cb_select_lines+N-1):
        to_print=f"DFF_EN config{x+1} (.clk(clk), .d(sout{previous_flop}), .rst(rst), .en(en), .q(sout{current_flop}));"
        print(to_print)
        previous_flop = current_flop;
        current_flop += 1;

    print("endmodule")

def create_LB_CB_Wrapper():
    to_print = f"module LB_CB_Wrapper_k{k}_N{N} (";
    print(to_print);
    total_number_of_BLE_inputs = (2**k)*N;
    total_number_of_BLE_select_lines = k*N;
    number_of_rmux_inputs = I + N;
    total_number_of_rmux_select_lines = math.ceil(math.log(I+N,10)/math.log(2,10)) * k * N;
    total_number_of_rmuxes = k * N;
    number_of_rmux_select_lines = math.ceil(math.log(number_of_rmux_inputs,10)/math.log(2,10));
    ##ADDED
    number_of_tracks_to_LB_inputs = int (Fcin * W);
    number_of_tracks_to_LB_outputs = int (Fcout * W);
    number_of_cbmux_inputs = math.ceil(Fcin*W);
    number_of_cbmux_select_lines = math.ceil(math.log(number_of_cbmux_inputs,10)/math.log(2,10));
    total_number_of_cb_select_lines = number_of_cbmux_select_lines*I;
    total_number_cbmuxes = I;
    print("clk,")
    print("rst,")
    print("en,")
    print("d,")

    #Logic Block Inputs
    for x in range(I):
        for y in range (number_of_tracks_to_LB_inputs):
            to_print = f"\t i{x}_{y},"
            print(to_print);

    #Logic Block Outputs
    for x in range (N):
        to_print = f"\t y{x},";
        print(to_print);

    print("prog_rst,")
    print("prog_en);")

    print("input clk;")
    print("input rst;")
    print("input en;")
    print("input d;")

    #Logic Block Inputs
    for x in range(I):
        for y in range (number_of_tracks_to_LB_inputs):
            to_print = f"\t input i{x}_{y};"
            print(to_print);

    for x in range (N):
        to_print = f"\t output y{x};";
        print(to_print);

    print("input prog_rst;")
    print("input prog_en;")

        #WIRES
    # LUT SRAMs
    for x in range(total_number_of_BLE_inputs):
        to_print = f"\t wire d{x};";
        print(to_print);

    #Rmux select lines
    for x in range(total_number_of_rmux_select_lines):
        to_print = f"\t wire s{x};";
        print(to_print);

    #CB Select lines
    for  x in range(total_number_of_cb_select_lines):
        to_print = f"\t wire s_cb{x};";
        print(to_print);

    for x in range(N):
        to_print = f"\t wire sout{x};";
        print(to_print);

    for x in range (N):
        to_print = f"\t wire y{x};";
        print(to_print);

    to_print = f"dff_config_bits config_bits0("
    print(to_print)
    print(".clk (clk),")
    print(".d (d),")
    total_number_of_BLE_inputs = (2**k)*N;
    total_number_of_BLE_select_lines = k*N;
    number_of_rmux_inputs = I + N;
    total_number_of_rmux_select_lines = math.ceil(math.log(I+N,10)/math.log(2,10)) * k * N;
    total_number_of_rmuxes = k * N;
    number_of_rmux_select_lines = math.ceil(math.log(number_of_rmux_inputs,10)/math.log(2,10));
    ##ADDED
    number_of_tracks_to_LB_inputs = int (Fcin * W);
    number_of_tracks_to_LB_outputs = int (Fcout * W);
    number_of_cbmux_inputs = math.ceil(Fcin*W);
    number_of_cbmux_select_lines = math.ceil(math.log(number_of_cbmux_inputs,10)/math.log(2,10));
    total_number_of_cb_select_lines = number_of_cbmux_select_lines*I;
    total_number_cbmuxes = I;
        #A model for Area-Efficient and Tileable FPGA Tiles
    
    # LUT SRAMs
    for x in range(total_number_of_BLE_inputs):
        to_print = f"\t .d{x} (d{x}),";
        print(to_print);

    #Rmux select lines
    for x in range(total_number_of_rmux_select_lines):
        to_print = f"\t .s{x} (s{x}),";
        print(to_print);

    #CB Select lines
    for  x in range(total_number_of_cb_select_lines):
        to_print = f"\t .s_cb{x} (s_cb{x}),";
        print(to_print);

    for x in range(N):
        to_print = f"\t .sout{x} (sout{x}),";
        print(to_print);
    
    print(".en (prog_en),")
    print(".rst (prog_rst));")

    ##LB CB
    to_print = f"logic_block_k{k}_N{N} logic_block_k{k}_N{N}_0(";
    print(to_print);
    total_number_of_BLE_inputs = (2**k)*N;
    total_number_of_BLE_select_lines = k*N;
    number_of_rmux_inputs = I + N;
    total_number_of_rmux_select_lines = math.ceil(math.log(I+N,10)/math.log(2,10)) * k * N;
    total_number_of_rmuxes = k * N;
    number_of_rmux_select_lines = math.ceil(math.log(number_of_rmux_inputs,10)/math.log(2,10));
    ##ADDED
    number_of_tracks_to_LB_inputs = int (Fcin * W);
    number_of_tracks_to_LB_outputs = int (Fcout * W);
    number_of_cbmux_inputs = math.ceil(Fcin*W);
    number_of_cbmux_select_lines = math.ceil(math.log(number_of_cbmux_inputs,10)/math.log(2,10));
    total_number_of_cb_select_lines = number_of_cbmux_select_lines*I;
    total_number_cbmuxes = I;
        #A model for Area-Efficient and Tileable FPGA Tiles
    

    # LUT SRAMs
    for x in range(total_number_of_BLE_inputs):
        to_print = f"\t .d{x}(d{x}),";
        print(to_print);
    
    #Logic Block Inputs
    for x in range(I):
        for y in range (number_of_tracks_to_LB_inputs):
            to_print = f"\t .i{x}_{y} (i{x}_{y}),"
            print(to_print);

    #Rmux select lines
    for x in range(total_number_of_rmux_select_lines):
        to_print = f"\t .s{x} (s{x}),";
        print(to_print);

    #CB Select lines
    for  x in range(total_number_of_cb_select_lines):
        to_print = f"\t .s_cb{x} (s_cb{x}),";
        print(to_print);

    for x in range(N):
        to_print = f"\t .sout{x} (sout{x}),";
        print(to_print);

    

    for x in range (N):
        to_print = f"\t .y{x} (y{x}),";
        print(to_print);

    print ("\t .clk (clk),");
    print ("\t .rst (rst),");
    print ("\t .en (en));");
    print("endmodule")

  #print(number_of_mux4_per_stage);
  #print(list_of_int_sigs)
  #print(last_mux_is_mux2);

def create_logic_block():
  to_print = f"module logic_block_k{k}_N{N} (";
  print(to_print);
  total_number_of_BLE_inputs = (2**k)*N;
  total_number_of_BLE_select_lines = k*N;
  number_of_rmux_inputs = I + N;
  total_number_of_rmux_select_lines = math.ceil(math.log(I+N,10)/math.log(2,10)) * k * N;
  total_number_of_rmuxes = k * N;
  number_of_rmux_select_lines = math.ceil(math.log(number_of_rmux_inputs,10)/math.log(2,10));
  ##ADDED
  number_of_tracks_to_LB_inputs = int (Fcin * W);
  number_of_tracks_to_LB_outputs = int (Fcout * W);
  number_of_cbmux_inputs = math.ceil(Fcin*W);
  number_of_cbmux_select_lines = math.ceil(math.log(number_of_cbmux_inputs,10)/math.log(2,10));
  total_number_of_cb_select_lines = number_of_cbmux_select_lines*I;
  total_number_cbmuxes = I;
    #A model for Area-Efficient and Tileable FPGA Tiles
  

  # LUT SRAMs
  for x in range(total_number_of_BLE_inputs):
    to_print = f"\t d{x},";
    print(to_print);
  
  #Logic Block Inputs
  for x in range(I):
    for y in range (number_of_tracks_to_LB_inputs):
      to_print = f"\t i{x}_{y},"
      print(to_print);

  #Rmux select lines
  for x in range(total_number_of_rmux_select_lines):
    to_print = f"\t s{x},";
    print(to_print);

  #CB Select lines
  for  x in range(total_number_of_cb_select_lines):
    to_print = f"\t s_cb{x},";
    print(to_print);

  for x in range(N):
    to_print = f"\t sout{x},";
    print(to_print);

  

  for x in range (N):
    to_print = f"\t y{x},";
    print(to_print);

  print ("\t clk,");
  print ("\t rst,");
  print ("\t en);");

  # LUT SRAMs
  for x in range(total_number_of_BLE_inputs):
    to_print = f"\t input d{x};";
    print(to_print);
  
  #Logic Block Inputs
  for x in range(I):
    for y in range (number_of_tracks_to_LB_inputs):
      to_print = f"\t input i{x}_{y};";
      print(to_print);

  #Rmux select lines
  for x in range(total_number_of_rmux_select_lines):
    to_print = f"\t input s{x};";
    print(to_print);

  #CB Select lines
  for  x in range(total_number_of_cb_select_lines):
    to_print = f"\t input s_cb{x};";
    print(to_print);

  for x in range(N):
    to_print = f"\t input sout{x};";
    print(to_print);

  print ("\t input clk;");
  print ("\t input rst;");
  print ("\t input en;");

  for x in range (N):
    to_print = f"\t output y{x};";
    print(to_print);

  #Logic Input Wires
  for x in range(I):
    to_print = f"\t wire i{x};"
    print(to_print);

  count_cb_data = 0;
  count_cbmux_select = 0;
  count_cbmux = 0;
  for x in range(total_number_cbmuxes):
    to_print = f"cbmux cbmux_{x} (";
    print(to_print);
    for y in range (number_of_cbmux_inputs):
      to_print = f"\t .d{y} (i{x}_{y}),";
      print(to_print);
    for y in range (number_of_cbmux_select_lines):
      to_print = f"\t .s{y} (s_cb{count_cbmux_select}),";
      print(to_print);
      count_cbmux_select += 1;
    to_print = f"\t .y (i{x}));";
    print(to_print);
  
  
  count_rmux_data = 0;
  count_rmux_select = 0;
  count_rmux = 0;
  for x in range (total_number_of_rmuxes):
    to_print = f"rmux rmux_{x} (";
    print(to_print);
    for y in range (number_of_rmux_inputs-N):
      to_print = f"\t .d{y} (i{y}),";
      print(to_print);
    for y in range (N):
      to_print = f"\t .d{y+number_of_rmux_inputs-N} (y_BLE{k}_{y}),";
      print(to_print);
    for y in range(number_of_rmux_select_lines):
      to_print = f"\t .s{y} (s{count_rmux_select}),";
      print(to_print);
      count_rmux_select = count_rmux_select + 1;
    to_print = f"\t .y (y_rmux{x}));";
    print(to_print);

  count_ble_d = 0;
  count_ble_s = 0;
  count_sout = 0;
  for x in range (N):
    to_print = f"BLE{k} BLE{k}_{x} (";
    print(to_print);
    for y in range (2**k):
      to_print = f"\t .d{y} (d{count_ble_d}),";
      print(to_print);
      count_ble_d = count_ble_d + 1;
    for y in range(k):
      to_print = f"\t .s{y} (y_rmux{count_ble_s}),";
      print(to_print);
      count_ble_s = count_ble_s + 1;
    print("\t .clk (clk),");
    print ("\t .rst (rst),");
    print ("\t .en (en),");
    to_print = f"\t .sout (sout{count_sout}),";
    print(to_print);
    count_sout = count_sout + 1;
    to_print = f"\t .y (y_BLE{k}_{x}));";
    print(to_print);
  for x in range (N):
    to_print = f"assign y{x} = y_BLE{k}_{x};";
    print (to_print);
  print("endmodule");




  

if __name__ == "__main__":
  create_mux2();
  create_mux4();
  create_DFF();
  create_rmux();
  create_cbmux();
  create_BLE();
  create_logic_block();
  generate_config_bits();
  create_LB_CB_Wrapper();