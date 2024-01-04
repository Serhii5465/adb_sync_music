from py_exec_cmd import exec_cmd

def NAME_SYNC_DIR() -> str:
    return 'Music/'

# # Test
# def ROOT_UNIX_SRC_DIR() -> str:
#     return '/cygdrive/f/media/'

# # Test
# def ROOT_DEST_DIR() -> str:
#     return '/storage/self/primary/'

def ROOT_UNIX_SRC_DIR() -> str:
    return '/cygdrive/e/media/'

def ROOT_DEST_DIR() -> str:
    return '/storage/F32E-95B4/'

def FULL_PATH_UNIX_SRC_ROOT() -> str:
    return ROOT_UNIX_SRC_DIR() + NAME_SYNC_DIR()

def WIN_SRC_DIR() -> str:
    return exec_cmd.get_bety_cmd_out(['cygpath.exe', '--windows', FULL_PATH_UNIX_SRC_ROOT()])