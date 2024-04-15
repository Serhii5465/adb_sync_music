from src import constants, fs_ops, proc
from typing import List
import logging

def prep_transf(is_exist: str, is_empty: str, logger: logging.Logger) -> None:
    """
    Depending on the status of the remote folder on Android, prepares synchronization commands.
    Args:
        is_exist: Is exists root folder?
        is_empty: Is empty root folder?
    """
    cmd_adb_push = ['adb', 'push', '', '']

    list_loc_files = fs_ops.get_loc_files()

    if is_exist == '1' and is_empty == '1':
        print('Music folder not exist.\nCreating...')
        cmd_adb_mkdir = ['adb', 'shell', 'mkdir', constants.ROOT_DEST_DIR() + constants.NAME_SYNC_DIR()]
        proc.run_cmd(cmd_adb_mkdir)

        upload(cmd_adb_push, list_loc_files, logger)

    if is_exist == '0' and is_empty == '1':
        print('Music folder exist,but empty')
        upload(cmd_adb_push, list_loc_files, logger)

    if is_exist == '0' and is_empty == '0':
        print('Music folder exist and not empty')
        list_rem_files = fs_ops.get_rem_files()


        list_del_files = ['"' + constants.ROOT_DEST_DIR() + i +
                            '"' for i in list(set(list_rem_files) -
                                            set(list_loc_files))]

        if len(list_del_files) > 0:
            fs_ops.delete_remt_files(list_del_files, logger)

        list_upl_files = list(set(list_loc_files) - set(list_rem_files))

        if len(list_upl_files) > 0:
            upload(cmd_adb_push, list_upl_files, logger)
        else:
            print('Nothing to uploading')

def upload(command: List[str], loc_files: List[str], logger: logging.Logger) -> None:
    """
    Сonverts paths of uploadable files to Windows style and starts
    of sync with Android.
    Args:
        command: Contains arguments command of sync for ABD.
        loc_files: List of relative paths to files, which will be uploaded.
    """

    logger.info('Uploading files...')
    cmd_conv_path = ['cygpath.exe', '--windows', '']

    for idx, val in enumerate(loc_files):
        #: Inserting path to file on destination side.
        command[len(command) - 1] = constants.ROOT_DEST_DIR() + val

        #: Converting path to WIN-style
        val = constants.ROOT_UNIX_SRC_DIR() + val
        cmd_conv_path[len(cmd_conv_path) - 1] = val

        #: Inserting path to file on transmit side.
        val = proc.get_bety_cmd_out(cmd_conv_path)
        command[len(command) - 2] = val

        #: Beginning of upload
        out = proc.get_cmd_out(command)

        if out.returncode == 0:
            form_out = out.stdout.strip('\n')
            logger.info(form_out)
        else:
            form_err = out.stderr.strip('\n')
            logger.error(form_err)
            raise RuntimeError(form_err)