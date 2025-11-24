from uvc.sdt.src import *
from cl_marb_tb_base_seq import cl_marb_tb_base_seq
from uvc.sdt.src.cl_sdt_seq_lib import cl_sdt_base_seq

class cl_marb_basic_seq(cl_marb_tb_base_seq):
    """Start virutal sequence of rd and wr in parallel for each producer"""

    def __init__(self, name = "cl_marb_basic_seq"):
        super().__init__(name)

        self.sequencer = None

    async def body(self):
        self.sequencer.logger.info("STARTING SUPER:BODY")
        await super().body()

        producer_seq0 = cl_sdt_base_seq.create("marb_tb_sdt_producer0_seq")
        prod_task0 = cocotb.start_soon(producer_seq0.start(self.sequencer.sequencer_producer0_agent))

        producer_seq1 = cl_sdt_base_seq.create("marb_tb_sdt_producer1_seq")
        prod_task1 = cocotb.start_soon(producer_seq1.start(self.sequencer.sequencer_producer1_agent))

        producer_seq2 = cl_sdt_base_seq.create("marb_tb_sdt_producer2_seq")
        prod_task2 = cocotb.start_soon(producer_seq2.start(self.sequencer.sequencer_producer2_agent))

        consumer_seq = cl_sdt_base_seq.create("marb_tb_sdt_consumer_seq")
        cons_task = cocotb.start_soon(consumer_seq.start(self.sequencer.sequencer_consumer_agent))

        self.sequencer.logger.info("STARTING STARTING SEQUENCES")
