from uvc.sdt.src import *
from cl_marb_tb_base_seq import cl_marb_tb_base_seq
from reg_model.seq_lib.cl_reg_enable_seq import cl_reg_enable_seq
from reg_model.seq_lib.cl_reg_disable_seq import cl_reg_disable_seq 
from uvc.sdt.src.cl_sdt_seq_lib import cl_sdt_base_seq
from uvc.apb.src.cl_apb_seq_lib import cl_apb_single_zd_seq
from uvc.apb.src.apb_common import OpType
from cocotb.triggers import ClockCycles


class cl_marb_random_prio_seq(cl_marb_tb_base_seq):
    """Start virutal sequence of writing new priority configuration to APB bus"""

    def __init__(self, name = "cl_marb_random_prio_seq"):
        super().__init__(name)

        # Hack for being able to clock in the sequence
        self.dut = None

        self.sequencer = None

    async def body(self):
        self.sequencer.logger.info("STARTING SUPER:BODY")
        await super().body()

        # Disable memory arbiter before changing priority
        self.sequencer.logger.info("Disabling Memory Arbiter before changing priority")
        disable_seq = cl_reg_disable_seq.create("disable_seq")
        await disable_seq.start(self.sequencer)
        # Write random priority configuration to APB bus
        prio_seq = cl_apb_single_zd_seq.create("marb_tb_apb_prio_seq")
        with prio_seq.randomize_with() as it:
            it.s_item.addr in vsc.rangelist([0x0, 0x4])
            #it.op == OpType.WRITE
            it.s_item.op == 1  # WRITE
            it.s_item.strb == 0xF
            with vsc.implies(it.s_item.addr == 0x0):
                it.s_item.data in vsc.rangelist([0x0, 0x2])
            #vsc.implies(it.s_item.addr == 0x0, it.s_item.data.inside(vsc.rangelist([0x1, 0x3])))
        self.sequencer.logger.info(f"Changing priority configuration: ADDR=0x{prio_seq.s_item.addr:08X}, DATA=0x{prio_seq.s_item.data:08X}")
        prio_task = cocotb.start_soon(prio_seq.start(self.sequencer.sequencer_apb_agent))

        await ClockCycles(self.dut.clk, 10)

        # Enable memory arbiter after changing priority
        self.sequencer.logger.info("Enabling Memory Arbiter after changing priority")
        enable_seq = cl_reg_enable_seq.create("enable_seq")
        await enable_seq.start(self.sequencer)

        self.sequencer.logger.info("STARTING STARTING SEQUENCES")
