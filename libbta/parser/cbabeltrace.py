import babeltrace

from .parser import Parser
from libbta import Event


class CBabeltrace(Parser): 
    def parse_dir(self, directory):
        self.col = babeltrace.TraceCollection()
        for _dir in self.iter_files(directory):
            if self.col.add_trace(traces_path, 'ctf') is None:
                raise RuntimeError('Cannot add trace')

    def parse(self):
        # a trace collection holds one to many traces
    
        # add the trace provided by the user
        # (LTTng traces always have the 'ctf' format)
        return col.events
