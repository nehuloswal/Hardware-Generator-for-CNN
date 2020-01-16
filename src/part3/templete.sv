$$ROM$$


module $modnamegen$(clk, reset, s_data_in_x, s_valid_x, s_ready_x, m_data_out_y, m_valid_y, m_ready_y);
  parameter WIDTH = $WIDTH$, ADDRX = $ADDRX$, ADDRF = $ADDRF$, LENX = $N$, LENF = $M$, P=$P$, SIZE = LENX - LENF + 1, LOGSIZE = ADDRX;
  input clk, reset, s_valid_x, m_ready_y;
  input signed [WIDTH-1:0] s_data_in_x;
  output s_ready_x, m_valid_y;
  output signed [WIDTH-1:0] m_data_out_y;
  logic [WIDTH-1:0] w_to_multx [P-1:0];
  logic [WIDTH-1:0] w_to_multf;
  logic w_wr_en_x, w_conv_done, w_read_done_x, w_hold_state, w_wr_en, w_valid_op;
  logic [ADDRX-1:0] w_to_addrx [P-1:0];  
  logic [ADDRX-1:0] w_read_addr_x [P-1:0]; 
  logic [ADDRX-1:0] w_write_addr_x;
  logic [ADDRF-1:0] w_to_addrf, w_read_addr_f;
  logic [ADDRX-1:0] w_start_addr;
  logic e_acc,c_acc;
  logic w_all_done;
  logic  w_en_acc, w_clr_acc;
  logic signed [WIDTH-1:0] conv_op [P-1:0];
  logic [ADDRX-1:0] w_read_addr_op;  
  logic [ADDRX-1:0] w_write_addr_op;
  logic w_write_done;

  
  always_comb begin
    int i;
    if (w_wr_en_x == 1)
      for (i = 0; i < P; i++)
          w_to_addrx[i] = w_write_addr_x;
        //w_to_addrx[P-1:1] = 0;
    else begin
      for (i = 0; i < P; i++)
        w_to_addrx[i] = w_read_addr_x[i];
    end
  w_to_addrf = w_read_addr_f;
  end
    genvar i;
    generate
      for (i = 0; i < P; i++)  
        memory #(WIDTH, LENX, ADDRX) mx(.clk(clk), .data_in(s_data_in_x), .data_out(w_to_multx[i]), .addr(w_to_addrx[i]), .wr_en(w_wr_en_x));
    endgenerate

  $rommodname$ mf (.clk(clk), .addr(w_to_addrf), .z(w_to_multf));

  memory_control_xf #(ADDRX, LENX) cx (.clk(clk), .reset(reset), .s_valid_x(s_valid_x), .s_ready_x(s_ready_x), .m_addr_x(w_write_addr_x), .ready_write(w_wr_en_x), .read_done(w_read_done_x), .all_done(w_all_done));


  conv_control #(ADDRX, ADDRF, LENX, LENF, P) cc(.reset(reset), .clk(clk), .m_addr_read_x(w_read_addr_x), .m_addr_read_f(w_read_addr_f), .conv_done(w_conv_done), .read_done_x(w_read_done_x), .en_acc(w_en_acc), .clr_acc(w_clr_acc), .start_addr(w_start_addr), .valid_op(w_valid_op), .write_done(w_write_done),.all_done(w_all_done));


  genvar j;
  generate
    for(j = 0; j < P; j++)
      convolutioner #(WIDTH, ADDRX, ADDRF) mac_unit(.clk(clk), .reset(reset), .m_addr_read_x(w_to_addrx[j]), .m_addr_read_f(w_to_addrf), .m_data_out_y(conv_op[j]), .en_acc(w_en_acc), .clr_acc(w_clr_acc), .m_data_x(w_to_multx[j]), .m_data_f(w_to_multf));
  endgenerate

  op_memory #(WIDTH,SIZE,LOGSIZE,P) om(.clk(clk), .data_in(conv_op), .data_out(m_data_out_y), .wr_en(w_valid_op), .waddr(w_write_addr_op), .raddr(w_read_addr_op));

  output_control #(SIZE,P,LOGSIZE) oc(.clk(clk), .reset(reset), .conv_done(w_conv_done), .m_valid_y(m_valid_y), .m_ready_y(m_ready_y), .start_addr(w_start_addr), .valid_op(w_valid_op), .wr_en(w_wr_en), .read_addr(w_read_addr_op), .send_addr(w_write_addr_op), .write_done(w_write_done), .all_done(w_all_done));

endmodule


