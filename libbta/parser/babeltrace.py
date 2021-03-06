import regex
import re

from .parser import Parser
from libbta import Event


meta_pattern = re.compile(r"""
        \[(?P<timestamp>\d+(\.\d*)?|\.\d+)\]
        \ +\(.*\)    # Ignore delta
        \ +(?P<host>\S+)
        \ +(?P<fullname>\S+)
""", re.VERBOSE)
attrs_group = re.compile(r"(?<={).*?(?=})")
# key_val_pattern = regex.compile(r"(?:[^,[]|\[.*\])+")
key_val_pattern = regex.compile(r"([^,([]+(?:[([](?:[^()[\]]*|(?1))*[)\]])*)")
key_val_split = re.compile(r" *(\S+) *= *(.*) *")


class Babeltrace(Parser): 
    @classmethod
    def parse(cls, infile):
        """
        Read lines from infile, where each line is an event
        """
        events = []
        with open(infile, encoding='utf-8') as tracefile:
            for line in tracefile:
                e = cls.parseline(line)
                events.append(e)
        return events
    

    @classmethod
    def parseline(cls, line):
        """
        Generate event from line
        """
        meta, attrs = re.split(r': (?={)', line, 1)
    
        m = meta_pattern.match(meta)
        timestamp = float(m.group('timestamp'))
        fullname = m.group('fullname')
        name_fields = fullname.split(':')
        if len(name_fields) == 1:
            scope = 'kernel'
            name = fullname
        else:
            scope = name_fields[0]
            name = name_fields[1]
    
        event = Event(name, timestamp)
    
        event['host'] = m.group('host')
        event['domain'] = m.group('host') + '.' + scope
    
        # print(attrs)
        cls.parse_attrs(attrs, event)
        return event
    

    @classmethod
    def parse_attrs(cls, attrs, event):
        for key_vals in attrs_group.findall(attrs.strip()):
    
            for key_val in key_val_pattern.findall(key_vals.strip()):
                m = key_val_split.match(key_val)
                event[m.group(1)] = m.group(2)
        return event
