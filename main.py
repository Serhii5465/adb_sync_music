import sys
from py_exec_cmd import exec_cmd
from src import log, upl, fs_ops

def is_dev_attach() -> None:
    """
    Verifies connection of USB device by his serial number.
    """
    serial_no = '293290c6'
    cmd_state = ['adb', 'devices']
    out = exec_cmd.get_bety_cmd_out(cmd_state)

    if out.find(serial_no) == -1:
        sys.exit('Device not connected')

def main() -> None:
    is_dev_attach()

    log_inst = log.crt_logger()
    is_exist, is_empty = fs_ops.is_exist_rem_dir()

    upl.prep_transf(is_exist, is_empty, log_inst)

main()