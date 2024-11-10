import asyncio
from pathlib import Path
import json

import click
from emmetify.cmd import html2emmet


@click.command(name='html2emmet')
@click.option(
    '--text',
    required=True,
    help="HTML text to convert to Emmet"
)
def cli_html2emmet(text: str):
    print(asyncio.run(html2emmet(text)))
