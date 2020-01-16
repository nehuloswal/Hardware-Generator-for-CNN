$$ROM$$

module $modnamegen$(clk, reset, s_data_in_x, s_valid_x, s_ready_x, m_data_out_y, m_valid_y, m_ready_y);
  parameter WIDTH = $WIDTH$, ADDRX = $ADDRX$, ADDRF = $ADDRF$, LENX = $N$, LENF = $M$, P=$P$, SIZE = LENX - LENF + 1, LOGSIZE = ADDRX;
  input clk, reset, s_valid_x, m_ready_y;
  input signed [WIDTH-1:0] s_data_in_x;
  output s_ready_x, m_valid_y;
  output signed [WIDTH-1:0] m_data_out_y;
  logic [WIDTH-1:0] w_to_multx, w_to_multf;
  logic w_wr_en_x, w_conv_done, w_read_done_x;
  logic [ADDRX-1:0] w_to_addrx, w_read_addr_x, w_write_addr_x;
  logic [ADDRF-1:0] w_to_addrf, w_read_addr_f;
  logic e_acc,c_acc;

  always_comb begin
    if (w_wr_en_x == 1)
      w_to_addrx = w_write_addr_x;
    else
      w_to_addrx = w_read_addr_x;
    if (w_wr_en_x == 1)
      w_to_addrf = 0;
    else
      w_to_addrf = w_read_addr_f;
  end
  memory1 #(WIDTH, LENX, ADDRX) mx (.clk(clk), .data_in(s_data_in_x), .data_out(w_to_multx), .addr(w_to_addrx), .wr_en(w_wr_en_x));

  $rommodname$ mf(.clk(clk), .addr(w_to_addrf), .z(w_to_multf));

  memory_control_xf1 #(ADDRX, LENX) cx (.clk(clk), .reset(reset), .s_valid_x(s_valid_x), .s_ready_x(s_ready_x), .m_addr_x(w_write_addr_x), .ready_write(w_wr_en_x), .conv_done(w_conv_done), .read_done(w_read_done_x), .valid_y(m_valid_y));

  conv_control1 #(ADDRX, ADDRF, LENX, LENF) cc(.reset(reset), .clk(clk), .m_addr_read_x(w_read_addr_x), .m_addr_read_f(w_read_addr_f), .conv_done(w_conv_done), .read_done_x(w_read_done_x), .m_valid_y(m_valid_y), .m_ready_y(m_ready_y), .en_acc(e_acc), .clr_acc(c_acc));

  convolutioner1 #(WIDTH, ADDRX, ADDRF) conv(.clk(clk), .reset(reset), .m_addr_read_x(w_to_addrx), .m_addr_read_f(w_to_addrf), .m_data_out_y(m_data_out_y), .en_acc(e_acc), .clr_acc(c_acc), .m_data_x(w_to_multx), .m_data_f(w_to_multf));
endmodule