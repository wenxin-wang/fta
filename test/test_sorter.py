import unittest, os

from libbta.sorter import Sorter
from libbta.parser import parser_babeltrace as traceparser
from libbta.layer.qemu_virtio_layer import QemuVirtioLayer
from libbta.layer.qemu_raw_layer import QemuRawLayer
from libbta.layer.deducers import VirtioRawDeducer


class SorterTestCase(unittest.TestCase):
    def setUp(self):
        self.infile = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   'babeltrace_example.txt')
        self.events = traceparser.parse(self.infile)
        self.upper = QemuVirtioLayer('QemuVirtioLayer')
        self.lower = QemuRawLayer('QemuRawLayer')
        self.deducer = VirtioRawDeducer(self.upper, self.lower)
        self.sorter = Sorter([(self.upper, ['debc.qemu']),
                              (self.lower, ['debc.qemu'])])
        self.sorter.read_events(self.events)

    def test_print(self):
        print()
        print(self.sorter)
