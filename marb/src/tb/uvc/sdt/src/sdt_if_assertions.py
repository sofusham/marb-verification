import pyuvm
from pyuvm import *
from cocotb.triggers import RisingEdge, FallingEdge, ReadOnly

class sdt_if_assert_check(uvm_subscriber):
    def __init__(self, clk_signal, rst_signal = None, rd_signal = None, wr_signal = None, addr_signal = None, wr_data = None, name = "sdt_if_assert_check"):
        
        self.name = name

        self.clk = clk_signal
        self.rst = rst_signal
        
        self.rd = rd_signal
        self.wr = wr_signal
        self.addr = addr_signal
        self.wr_data = wr_data

        self.passed = True
    
    def check_assertions(self):
        cocotb.start_soon(self.rd_wr_checker())
        cocotb.start_soon(self.addr_checker())
        cocotb.start_soon(self.wr_data_checker())

    # 1. rd and wr are not asserted at the same timeq
    async def rd_wr_checker(self):
        while True:
            await RisingEdge(self.clk)
            await ReadOnly()

            try:
                if (self.rd.value == 1) and (self.wr.value == 1):
                    raise AssertionError(f"rd and wr asserted at the same time")
                
            except Exception as msg:
                self.passed = False
                print(msg)
        
    # 2. addr must not be 'X' when rd or wr is asserted
    async def addr_checker(self):
        while True:
            await RisingEdge(self.clk)
            await ReadOnly()

            if (self.rd.value == 1) or (self.wr.value == 1):
                try:
                    if "X" in self.addr.value.binstr:
                        raise AssertionError(f"addr is 'X' when rd or wr is asserted")
                except Exception as msg:
                    self.passed = False
                    print(msg)
    
    # 3. wr_data must not be 'X' when wr is asserted
    async def wr_data_checker(self):
        while True:
            await RisingEdge(self.clk)
            await ReadOnly()

            if self.wr.value == 1:
                try:
                    if "X" in self.wr_data.value.binstr:
                        raise AssertionError(f"wr_data is 'X' when wr is asserted")
                except Exception as msg:
                    self.passed = False
                    print(msg)