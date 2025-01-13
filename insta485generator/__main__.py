"""Build static HTML site from directory of HTML templates and plain files."""
import click
import pathlib
from pathlib import Path

@click.command()
@click.argument("input_dir", nargs=1, type=click.Path(exists=True))
def main(input_dir):
    input_dir = pathlib.Path(input_dir)
    print(f"DEBUG input_dir={input_dir}")


if __name__ == "__main__":
    main()