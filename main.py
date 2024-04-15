import sys
from src import log, upl, fs_ops, proc

def is_dev_attach() -> None:
    """
    Verifies connection of USB device by his serial number.
    """
    serial_no = '293290c6'
    out = proc.get_cmd_out(['adb', 'devices']).stdout.strip('\n')

    if out.find(serial_no) == -1:
        sys.exit('Device not connected')

def main() -> None:
    is_dev_attach()

    log_inst = log.crt_logger()
    is_exist, is_empty = fs_ops.is_exist_rem_dir()

    upl.prep_transf(is_exist, is_empty, log_inst)

main()