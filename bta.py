#!/usr/bin/env python3
import os
import time
import click

# Rewrite of blk_analyse

from libbta.traces import Traces
from libbta.config import Config
from libbta.sorter import Sorter


pass_traces = click.make_pass_decorator(Traces)


@click.group()
@click.option('-c', '--conf', default='config.py', show_default=True,
              help='Configuration file Location')
@click.option('--cwd', type=click.Path(file_okay=False, writable=True), help='Working Directory, all following path options, \
if is relative, will be relative to this path [default: the directory of \
conf file]')
@click.option('--cache_dir', default='cache', show_default=True,
              help='Directory for storing caches')
@click.option('-t', '--trace_dir', default='traces', show_default=True,
              help='Directory for storing traces')
@click.pass_context
def cli(ctx, conf, cwd, cache_dir, trace_dir):
    """
    Block trace analyser
    """
    if not cwd:
        cwd = os.path.dirname(os.path.realpath(conf))
    os.chdir(cwd)
    config = {'cache_dir': cache_dir, 'trace_dir': trace_dir}
    config = Config(conf).read(default=config)
    for path in ['cache_dir', 'trace_dir']:
        if not os.path.exists(config[path]):
            os.makedirs(config[path])
    ctx.obj = Traces(config)


@cli.command()
@pass_traces
def list(traces):
    for event in traces.load():
        click.echo(event)
    return