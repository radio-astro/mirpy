import subprocess
import warnings
from mirpy.commands import mir_commands

class MiriadError(Exception):
    def __init__(self, value):
	self.value = value
    def __str__(self):
	return str(self.value)

def to_args(kw):
    out = []
    for k,v in kw.items():
        if k.startswith("_"):
            k = k[1:]
        if isinstance(v, list):
            v = ",".join([str(i) for i in v])
        out.append("%s=%s" % (k,v))
    return out

def mir_func(f, filter, **kw):
    def func(**kw):
        args = to_args(kw)
        proc = subprocess.Popen([f]+args, shell=False, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()

    	lines = stderr.split('\n')
    	warns = []
    	errors = []
    	for l in lines:
	    wpfx = "### Warning: "
	    epfx = "### Fatal Error: "
	    if l.startswith(wpfx):
	        warns.append(l[len(wpfx):])
	    elif l.startswith(epfx):
	        errors.append(l[len(epfx)+1:])
	    else:
	        errors.append(l)
        if warns:
	    msg = "'%s': " % f
	    msg += "\n".join(warns)
	    warnings.warn(msg)

        if proc.returncode != 0:
            raise MiriadError("\n".join(errors))
        out = stdout.strip()
        if filter is not None:
            return filter(out)
        return out
    return func

class Miriad(object):
    def __init__(self):
        self._common = mir_commands()
        self._filters = {}

    def set_filter(self, funcname, ffunc):
        self._filters[funcname] = ffunc
        
    def __getattr__(self, k):
        if k in self._common:
            filter = self._filters.get(k, None)
            fn = mir_func(k, filter)
            fn.__doc__ = self._help(k)
            fn.func_name = k
            return fn 
        else:
            return object.__getattribute__(self, k)

    def _help(self, taskname):
        p = subprocess.Popen('miriad', shell=True, stdin=subprocess.PIPE, 
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print >>p.stdin, "help", taskname
        print >>p.stdin, "exit"
        stdout = p.communicate()[0]
        return str(stdout)
        #lines = stdout.split("\n")
        

if __name__ == "__main__":
    mir = Miriad()
    def uvindex_filt(output):
        lines = output.split()
        return lines
    mir.set_filter('uvindex', uvindex_filt)
    help(mir.uvindex)
    print mir.uvindex(vis="wshop.uv")
    
