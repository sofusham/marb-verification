from pyuvm import *
from .cl_reg_base_seq import *

class cl_reg_disable_seq(cl_reg_base_seq):
    """Disable sequence for control registers"""

    def __init__(self, name = "cl_reg_disable_seq"):
        super().__init__(name)

    async def body(self):
        await super().body()

        #######################
        # Start disable sequence
        #######################
        # Read ctrl_reg register
        status, read_val = await self.sequencer.reg_model.ctrl_reg.read(self.bus_map, path_t.FRONTDOOR, check_t.NO_CHECK)
        # Check the status received
        if status == status_t.IS_OK:
            self.sequencer.logger.info(
                f"Setup SEQ: read {read_val} "
                f"from ctrl_reg, status = {status}")
        else:
            self.sequencer.logger.error("STATUS is NOT_OK")

        # Write ctrl_reg
        write_val = read_val & (~self.start_mask)
        status = await self.sequencer.reg_model.ctrl_reg.write(write_val, self.bus_map, path_t.FRONTDOOR, check_t.NO_CHECK)
        # Check the status received
        if status == status_t.IS_OK:
            self.sequencer.logger.info(
                f"Setup SEQ: written {write_val} "
                f"to ctrl_reg, status = {status}")
        else:
            self.sequencer.logger.error("STATUS is NOT_OK")
