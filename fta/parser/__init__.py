def parse_traces(parsers):
    trace_queues = []
    for parser, files in parsers.items():
        if files:
            trace_queues.extend(parser.parse_files(files))
    return merge_sorted(trace_queues, lambda e: e['timestamp'])


def merge_sorted(lists, key):
    if len(lists) == 1:
        return lists[0]
    merged = []
    for l in lists:
        merged.extend(l)
    merged.sort(key=key)
    return merged