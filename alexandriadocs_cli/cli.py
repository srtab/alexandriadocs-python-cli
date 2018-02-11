# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import io
import os
import sys
import click
import tarfile
import requests

SITE = 'http://localhost:8000/api/v1/projects/upload/'


class Context(object):

    def __init__(self):
        self.verbose = False
        self.path = os.getcwd()

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)


pass_context = click.make_pass_decorator(Context, ensure=True)


@click.command()
@click.option('-p', '--path', required=True,
              type=click.Path(exists=True, file_okay=False, resolve_path=True),
              help='Changes the folder to operate on.')
@click.option('-v', '--verbose', is_flag=True,
              help='Enables verbose mode.')
@click.option('-t', '--token', nargs=1, type=str, required=True,
              help='The project token.')
@pass_context
def cli(ctx, verbose, path, token):
    """A complex command line interface."""
    ctx.verbose = verbose

    tar = tarfile.open("sample.tar.gz", mode="w:gz")
    tar = tar.add(path)
    f = open("sample.tar.gz", "rb")
    # archive = tarfile.open(mode='w:gz')
    # archive.add(path)
    # archive.close()
    # f = io.BytesIO()
    # with tarfile.open(mode='w:gz', fileobj=f) as archive:
    #     archive.add(path)
    # print(token)
    response = requests.post(SITE, headers={
        'Api-Key': token},
        files={'archive': f})
    f.close()
    print(response)

if __name__ == '__main__':
    cli()
