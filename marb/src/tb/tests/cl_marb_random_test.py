import pyuvm
from pyuvm import *
from cocotb.triggers import ClockCycles, Combine

from random import randint

from cl_marb_tb_base_test import cl_marb_tb_base_test
from vseqs.cl_reg_simple_seq import cl_reg_simple_seq
from vseqs.cl_marb_basic_seq import cl_marb_basic_seq
from uvc.sdt.src import *

@pyuvm.test(timeout_time = 1000, timeout_unit = 'ns')
class cl_marb_random_test(cl_marb_tb_base_test):
    """Random traffic test, default priotization"""

    def __init__(self, name = "cl_marb_basic_test", parent = None):
        super().__init__(name, parent)

        # Create sequences
        self.prod_seq = cl_sdt_single_seq.create("prod_seq")
        self.cons_seq = cl_sdt_consumer_rsp_seq.create("cons_seq")


    async def run_phase(self):
        self.logger.info("Start run_phase() -> MARB random traffic test")
        self.raise_objection()

        await super().run_phase()

        # Register sequence for enabling and configuring the Memory Arbiter sequence
        conf_seq = cl_reg_simple_seq.create("conf_seq")
        conf_seq.randomize()

        cocotb.start_soon(conf_seq.start(self.marb_tb_env.virtual_sequencer))

        # Launch sequences (as many consumer transactions as producer transactions)
        prod0_task = cocotb.start_soon(self.prod_transaction(10, self.marb_tb_env.virtual_sequencer.sequencer_producer0_agent))
        prod1_task = cocotb.start_soon(self.prod_transaction(10, self.marb_tb_env.virtual_sequencer.sequencer_producer1_agent))
        prod2_task = cocotb.start_soon(self.prod_transaction(10, self.marb_tb_env.virtual_sequencer.sequencer_producer2_agent))
        cons_task = cocotb.start_soon(self.cons_transaction(1, self.marb_tb_env.virtual_sequencer.sequencer_consumer_agent))

        # Wait until all tasks are done
        await Combine(prod0_task, prod1_task, prod2_task)

        await ClockCycles(self.dut.clk, 20)
        self.drop_objection()

        self.logger.info("End run_phase() -> MARB random traffic test")
    
    async def prod_transaction(self, num, handle):
        for _ in range(0, num):
            await self.prod_seq.start(handle)
            self.logger.info("Producer transaction done")
    
    async def cons_transaction(self, num, handle):
        for _ in range(0, num):
            await self.cons_seq.start(handle)
            self.logger.info("Consumer transaction done")
