from .cl_reg_base_seq import *

class cl_reg_dynamic_seq(cl_reg_base_seq):
    """Setup sequence for registers"""

    def __init__(self, name = "cl_reg_dynamic_seq"):
        super().__init__(name)

    async def body(self):
        await super().body()

        #######################
        # Set dynamic priority
        #######################

        # set dynamic priority
        # cif2 > cif1 > cif0
        write_val = 0 | 2 << 16 | 1 << 8 | 0
        print(write_val)
        status = await self.sequencer.reg_model.dprio_reg.write(write_val, self.bus_map, path_t.FRONTDOOR, check_t.NO_CHECK)
        # Check the status received
        if status == status_t.IS_OK:
            self.sequencer.logger.info(
                f"Static SEQ: read {write_val} "
                f"from ctrl_reg, status = {status}")
        else:
            self.sequencer.logger.error("STATUS is NOT_OK")
        

        # Read current control register value
        status, read_val = await self.sequencer.reg_model.ctrl_reg.read(self.bus_map, path_t.FRONTDOOR, check_t.NO_CHECK)
        # Check the status received
        if status == status_t.IS_OK:
            self.sequencer.logger.info(
                f"Static SEQ: read {read_val} "
                f"from ctrl_reg, status = {status}")
        else:
            self.sequencer.logger.error("STATUS is NOT_OK")
        
        # Write control register to enable dynamic priority
        write_val = self.dynamic_prio_mask | self.start_mask
        status = await self.sequencer.reg_model.ctrl_reg.write(write_val, self.bus_map, path_t.FRONTDOOR, check_t.NO_CHECK)
        # Check the status received
        if status == status_t.IS_OK:
            self.sequencer.logger.info(
                f"Static SEQ: written {write_val} "
                f"to ctrl_reg, status = {status}")
        else:
            self.sequencer.logger.error("STATUS is NOT_OK")
