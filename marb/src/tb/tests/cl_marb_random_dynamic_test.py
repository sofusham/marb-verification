import pyuvm
from pyuvm import *
from cocotb.triggers import ClockCycles, Combine

from random import randint

from cl_marb_tb_base_test import cl_marb_tb_base_test
from vseqs.cl_reg_simple_dynamic_seq import cl_reg_simple_dynamic_seq
from vseqs.cl_marb_basic_seq import cl_marb_basic_seq
from vseqs.cl_marb_random_prio_seq import cl_marb_random_prio_seq
from uvc.sdt.src import *




@pyuvm.test(timeout_time = 1000, timeout_unit = 'ns')
class cl_marb_random_dynamic_test(cl_marb_tb_base_test):
    """Random traffic test, with reverse(dynamic) priotization"""

    def __init__(self, name = "cl_marb_basic_test", parent = None):
        super().__init__(name, parent)

        # Create sequences (producers are created dynamically)
        self.cons_seq = cl_sdt_consumer_rsp_seq.create("cons_seq")

    async def run_phase(self):
        self.logger.info("Start run_phase() -> MARB random traffic test")
        self.raise_objection()

        await super().run_phase()

        # Register sequence for enabling and configuring the Memory Arbiter sequence
        conf_seq = cl_reg_simple_dynamic_seq.create("conf_seq")

        #cocotb.start_soon(conf_seq.start(self.marb_tb_env.virtual_sequencer))
        await conf_seq.start(self.marb_tb_env.virtual_sequencer)

        # Launch sequences
        prod0_task = cocotb.start_soon(self.prod_transaction(10, self.marb_tb_env.virtual_sequencer.sequencer_producer0_agent))
        prod1_task = cocotb.start_soon(self.prod_transaction(10, self.marb_tb_env.virtual_sequencer.sequencer_producer1_agent))
        prod2_task = cocotb.start_soon(self.prod_transaction(10, self.marb_tb_env.virtual_sequencer.sequencer_producer2_agent))
        cons_task = cocotb.start_soon(self.cons_transaction(1, self.marb_tb_env.virtual_sequencer.sequencer_consumer_agent))

        # Wait until all tasks are done
        await Combine(prod0_task, prod1_task, prod2_task)

        await ClockCycles(self.dut.clk, 10)

        # Change priotization dynamically during runtime
        prio_seq = cl_marb_random_prio_seq.create("prio_seq")
        prio_seq.dut = self.dut
        await prio_seq.start(self.marb_tb_env.virtual_sequencer)
        #await ClockCycles(self.dut.clk, 20)

        # Launch sequences again
        prod0_task = cocotb.start_soon(self.prod_transaction(10, self.marb_tb_env.virtual_sequencer.sequencer_producer0_agent))
        prod1_task = cocotb.start_soon(self.prod_transaction(10, self.marb_tb_env.virtual_sequencer.sequencer_producer1_agent))
        prod2_task = cocotb.start_soon(self.prod_transaction(10, self.marb_tb_env.virtual_sequencer.sequencer_producer2_agent))

        # Wait until all tasks are done
        await Combine(prod0_task, prod1_task, prod2_task)

        await ClockCycles(self.dut.clk, 10)

        self.drop_objection()

        self.logger.info("End run_phase() -> MARB random traffic test")
    
    async def prod_transaction(self, num, handle):
        for i in range(0, randint(1, num)):
            prod_seq = cl_sdt_single_zd_seq.create("prod_seq")
            prod_seq.randomize()
            await prod_seq.start(handle)
    
    async def cons_transaction(self, num, handle):
        for _ in range(0, num):
            await self.cons_seq.start(handle)
            self.logger.info("Consumer transaction done")
