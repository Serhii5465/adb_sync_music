import os
import logging
import sys
from typing import Tuple, List
from src import constants, proc

def is_exist_rem_dir() -> Tuple[str, str]:
    """
    Checks, if exists and is empty remote directory on Android device.
    Returns:
        If exists returns 0, otherwise 1.
        If empty returns 1, otherwise 0.
    """
    cmd_is_exist_dir = ['adb', 'shell', '[ -d ' + constants.ROOT_DEST_DIR()
                        + constants.NAME_SYNC_DIR() + ' ] && echo 0 || echo 1']

    cmd_is_empty_dir = ['adb', 'shell',
                        'find ' + constants.ROOT_DEST_DIR() + constants.NAME_SYNC_DIR() +
                        ' -mindepth 1 -maxdepth 1 | '
                        'read && echo 0 || echo 1']  # 0 - not empty, 1 - empty

    is_exist = proc.get_bety_cmd_out(cmd_is_exist_dir)
    is_empty = proc.get_bety_cmd_out(cmd_is_empty_dir)

    return is_exist, is_empty

def get_loc_files() -> List[str]:
    """
    Finds recursively all files in folders on PC.
    Returns:
        List of relative paths to files.
    """

    dir = constants.ROOT_UNIX_SRC_DIR() + constants.NAME_SYNC_DIR()
    try:
        result = os.listdir(dir)
    except FileNotFoundError:
        sys.exit(dir + 'is missing')
    else:
        if len(result) == 0:
            raise IndexError(dir + 'is empty')

    os.chdir(constants.ROOT_UNIX_SRC_DIR())

    cmd_get_loc_files = ['find', constants.NAME_SYNC_DIR(), '-type', 'f']
    list_loc_files = proc.get_bety_cmd_out(cmd_get_loc_files).split('\n')

    return list_loc_files

def get_rem_files() -> List[str]:
    """
    Finds recursively all files in folders on Android device.
    Returns:
        List of relative paths to files.
    """
    cmd_adb_get_rem_files = ['adb', 'shell', 'cd '
                                + constants.ROOT_DEST_DIR()
                                + ' && find '
                                + constants.NAME_SYNC_DIR()
                                + ' -type f']

    list_rem_files = proc.get_bety_cmd_out(cmd_adb_get_rem_files).split('\n')
    return list_rem_files

def delete_remt_files(files: List[str], logger: logging.Logger) -> None:
    """
    Deletes files and folders on Android, which are missing on PC.
    Args:
        files: List of full paths to files.
    """
    if len(files) != 0:
        cmd_del_file = ['adb', 'shell', 'rm', '']
        logger.info('Removing files...')
        for i in files:
            logger.info('Deletable file: ' + i)
            cmd_del_file[len(cmd_del_file) - 1] = i
            out = proc.get_cmd_out(cmd_del_file)
            if out.returncode != 0:
                logger.error(out.stderr)

        #: Utility 'find' removing empty folders
        cmd_del_empt_dir = ['adb', 'shell',
                            'find ' + constants.ROOT_DEST_DIR()
                            + constants.NAME_SYNC_DIR() + ' -type d -delete']

        str_empty_dirs = proc.get_bety_cmd_out(cmd_del_empt_dir)
        if str_empty_dirs != '':
            logger.info('Removing empty directories...')
            list_empty_dirs = str_empty_dirs.split('\n')
            for i in list_empty_dirs:
                logger.info('Deletable directory: ' + i)