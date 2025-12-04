import pyuvm
from pyuvm import *
from cocotb.triggers import RisingEdge, FallingEdge, ReadOnly

class cl_marb_ack_assert_check(uvm_subscriber):
    def __init__(self, clk_signal = None, rst_signal = None, ack0_signal = None, ack1_signal = None, ack2_signal = None, name = "cl_marb_ack_assert_check"):
        
        self.name = name

        self.clk = clk_signal
        self.rst = rst_signal
        
        self.ack0 = ack0_signal
        self.ack1 = ack1_signal
        self.ack2 = ack2_signal

        self.passed = True
    
    def check_assertions(self):
        cocotb.start_soon(self.ack_checker())

    # Only one ack signal is asserted at a time
    async def ack_checker(self):
        while True:
            await RisingEdge(self.clk)
            await ReadOnly()

            try:
                if (self.ack0.value == 1) + (self.ack1.value == 1) + (self.ack2.value == 1) > 1:
                    raise AssertionError(f"More than one ack signal asserted at the same time")

            except Exception as msg:
                self.passed = False
                print(msg)