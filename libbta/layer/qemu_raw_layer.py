from collections import deque

from . import BlkLayer


class QemuRawLayer(BlkLayer):
    """
    Layer for Qemu's Raw File Backend

    Doesn't have a finish event for itself, since it calls a callback function
    on finish. So it relies on the deducer to find a relationship, and mark it
    as finished. So finish_request is actually called by deducer.
    """
    TYPE = {'1': 'read', '2':'write'}

    SECTOR_SIZE = 512

    def __init__(self, name):
        super().__init__(name,
                         [('id', 'acb'), ('type', 'type'),
                          ('offset', 'sector_num'), ('length', 'nb_sectors')])
        self.added_reqs = deque()
        self.submitted_reqs = deque()
        self.finished_reqs = deque()

        self.issued_reqs = self.submitted_reqs

    def __repr__(self):
        string = '\n'.join([super().__repr__(),
                            'Added: ' + str(self.added_reqs),
                            'Submitted: ' + str(self.submitted_reqs),
                            'Finished: ' + str(self.finished_reqs)])
        return string

    def read_event(self, event):
        """
        Read a event, associate it with a request, then call deducer on add,
        rely on it for finishing request. It is possible that a request is
        actually finished but never marked so, if the deducer can't decide.
        """
        if event.name == 'paio_submit':
            self.add_request(event)
        elif event.name == 'handle_aiocb_rw':
            self.submit_request(event)

    def add_request(self, event):
        """
        Read a event, generate a request
        """
        req = self.gen_req('qemu_raw_rw', event)
        if req.type == 'read' or req.type == 'write':
            self._add_req(req, event.timestamp, self.added_reqs)

    def submit_request(self, event):
        """
        Read a event, submit a request
        """
        _id = event['aiocb']
        for req, idx in zip(self.added_reqs,
                            range(len(self.added_reqs))):
            if req['id'] == _id:
                del self.added_reqs[idx]
                self._submit_req(req, event.timestamp, self.submitted_reqs)
                return
        print("Throw event {0}".format(event))

    def finish_request(self, req, timestamp):
        self.submitted_reqs.remove(req)
        self._finish_req(req, timestamp, self.finished_reqs)

    def gen_req(self, name, event):
        req = super().gen_req(name, event)
        req.offset *= self.SECTOR_SIZE
        req.length *= self.SECTOR_SIZE
        req.type = self.TYPE.get(req.type, req.type)
        return req