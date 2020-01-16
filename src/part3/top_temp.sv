parameter WIDTH = $WIDTH$;
input clk, reset, s_valid_x, m_ready_y;
input signed [WIDTH-1:0] s_data_in_x;
output s_ready_x, m_valid_y;
output signed [WIDTH-1:0] m_data_out_y;

logic l1_valid, l1_ready, l2_valid, l2_ready;
logic signed [WIDTH-1:0] l1_data;
logic signed [WIDTH-1:0] l2_data;

$modname1$ m1(.clk(clk), .reset(reset), .s_data_in_x(s_data_in_x), .s_valid_x(s_valid_x), .s_ready_x(s_ready_x), .m_data_out_y(l1_data), .m_valid_y(l1_valid), .m_ready_y(l1_ready)); 
$modname2$ m2(.clk(clk), .reset(reset), .s_data_in_x(l1_data), .s_valid_x(l1_valid), .s_ready_x(l1_ready), .m_data_out_y(l2_data), .m_valid_y(l2_valid), .m_ready_y(l2_ready));
$modname3$ m3(.clk(clk), .reset(reset), .s_data_in_x(l2_data), .s_valid_x(l2_valid), .s_ready_x(l2_ready), .m_data_out_y(m_data_out_y), .m_valid_y(m_valid_y), .m_ready_y(m_ready_y));

endmodule