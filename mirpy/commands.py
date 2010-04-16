import os

def mir_commands():
    """Get a filter list of miriad commands in the miriad bin directory"""
    mir = which('miriad')
    if mir is None:
        raise OSError('miriad is not available. Check your PATH.')
    mirpath = os.path.split(mir)[0]
    return [ cmd for cmd in os.listdir(mirpath) \
                 if (not cmd.startswith('mir') or not cmd.startswith('doc')
                     or not cmd.startswith('pg')) ]



def which(program='miriad'):
    """Equivalent of unix 'which' command"""
    def is_exe(fpath):
        return os.path.exists(fpath) and os.access(fpath, os.X_OK)
    if program:
        fpath, fname = os.path.split(program)
    else:
        return None
    if fpath and is_exe(program):
        return program
    else:
        if os.environ.has_key("PATH"):
           for path in os.environ["PATH"].split(os.pathsep):
               exe_file = os.path.join(path, program)
               if is_exe(exe_file):
                   return exe_file
    return None
