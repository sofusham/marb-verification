from pyuvm import *

from uvc.sdt.src.cl_sdt_config import *
from uvc.apb.src.cl_apb_config import *

from uvc.sdt.src.cl_sdt_interface import cl_sdt_interface
from uvc.sdt.src.sdt_common import DriverType, SequenceItemOverride

class cl_marb_tb_config(uvm_object):
    def __init__(self, name = "cl_marb_tb_config"):
        super().__init__(name)

        self.dut = None

        self.apb_cfg = cl_apb_config.create("apb_cfg")

        self.data_width = None
        self.addr_width = None
        
        self.sdt_prod0_cfg = cl_sdt_config.create("sdt_prod0_cfg")
        self.sdt_prod1_cfg = cl_sdt_config.create("sdt_prod1_cfg")
        self.sdt_prod2_cfg = cl_sdt_config.create("sdt_prod2_cfg")
        self.sdt_cons_cfg = cl_sdt_config.create("sdt_cons_cfg")


        # sdt configuration
        #self.sdt_prod0_cfg.vif = cl_sdt_interface(clk_signal = None, rst_signal = None, name = "sdt_prod_vif") # fix clk and rst in base test
        self.sdt_prod0_cfg.is_active = uvm_active_passive_enum.UVM_ACTIVE
        self.sdt_prod0_cfg.driver = DriverType.PRODUCER
        self.sdt_prod0_cfg.num_consumer_seq = None
        self.sdt_prod0_cfg.enable_transaction_coverage = True
        self.sdt_prod0_cfg.enable_delay_coverage = True
        #self.sdt_prod0_cfg.seq_item_override = SequenceItemOverride.DEFAULT
        self.sdt_prod0_cfg.rd_data_no_ack_value = 'X'

        #self.sdt_prod1_cfg.vif = cl_sdt_interface(clk_signal = None, rst_signal = None, name = "sdt_prod_vif") # fix clk and rst in base test
        self.sdt_prod1_cfg.is_active = uvm_active_passive_enum.UVM_ACTIVE
        self.sdt_prod1_cfg.driver = DriverType.PRODUCER
        self.sdt_prod1_cfg.num_consumer_seq = None
        self.sdt_prod1_cfg.enable_transaction_coverage = True
        self.sdt_prod1_cfg.enable_delay_coverage = True
        #self.sdt_prod1_cfg.seq_item_override = SequenceItemOverride.DEFAULT
        self.sdt_prod1_cfg.rd_data_no_ack_value = 'X'    

        #self.sdt_prod2_cfg.vif = cl_sdt_interface(clk_signal = None, rst_signal = None, name = "sdt_prod_vif") # fix clk and rst in base test
        self.sdt_prod2_cfg.is_active = uvm_active_passive_enum.UVM_ACTIVE
        self.sdt_prod2_cfg.driver = DriverType.PRODUCER
        self.sdt_prod2_cfg.num_consumer_seq = None
        self.sdt_prod2_cfg.enable_transaction_coverage = True
        self.sdt_prod2_cfg.enable_delay_coverage = True
        #self.sdt_prod2_cfg.seq_item_override = SequenceItemOverride.DEFAULT
        self.sdt_prod2_cfg.rd_data_no_ack_value = 'X'            

        

        #self.sdt_cons_cfg.vif = cl_sdt_interface(clk_signal = None, rst_signal = None, name = "sdt_cons_vif") # fix clk and rst in base test
        self.sdt_cons_cfg.is_active = uvm_active_passive_enum.UVM_ACTIVE
        self.sdt_cons_cfg.driver = DriverType.CONSUMER
        self.sdt_cons_cfg.num_consumer_seq = None
        self.sdt_cons_cfg.enable_transaction_coverage = True
        self.sdt_cons_cfg.enable_delay_coverage = True
        #self.sdt_cons_cfg.seq_item_override = SequenceItemOverride.DEFAULT
        self.sdt_cons_cfg.rd_data_no_ack_value = 'X'


        