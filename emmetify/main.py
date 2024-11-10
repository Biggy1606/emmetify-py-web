import click

from emmetify.cli.html2emmet import cli_html2emmet

@click.group()
def main():
    """Emmetify - Tree structured data to Emmet converter"""
    pass

main.add_command(cli_html2emmet)

if __name__ == "__main__":
    main()

