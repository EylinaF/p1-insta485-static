"""Build static HTML site from directory of HTML templates and plain files."""
import pathlib
import json
import shutil
import sys
import click
import jinja2
from jinja2 import TemplateSyntaxError, TemplateNotFound

@click.command(help="Templated static website generator.")
@click.argument("input_dir", nargs=1, type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(), help='Output directory.')
@click.option("-v", "--verbose", is_flag=True, help='Print more output.')
def main(input_dir, output, verbose):
    """Generate a HTML site."""
    input_dir = pathlib.Path(input_dir)
    output_dir = pathlib.Path(output) if output else input_dir/"html"
    if output_dir.exists():
        print(f"insta485generator error: '{output_dir}' already exists")
        sys.exit(1)
    config_filename = pathlib.Path(input_dir/"config.json")

    if not config_filename.exists():
        print(f"insta485generator error: '{config_filename}' not found")
        sys.exit(1)

    try:
        with config_filename.open(encoding="utf-8") as config_file:
            # config_filename is open within this code block
            config_list = json.load(config_file)
        # config_filename is automatically closed
    except json.JSONDecodeError as e1:
        print(f"insta485generator error: '{config_filename}'")
        print(e1)
        sys.exit(1)

    template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(input_dir/"templates")),
        autoescape=jinja2.select_autoescape(['html', 'xml']),
    )

    
    for entry in config_list:
        render_template(entry, output_dir, template_env, verbose)

    copy_static_file(input_dir, output_dir, verbose)


if __name__ == "__main__":
    main()


def render_template(entry, output_dir, template_env, verbose):
    """Render."""
    url = entry["url"]
    url = url.lstrip("/")
    template_name = entry["template"]
    try:
        template = template_env.get_template(template_name)
    except TemplateSyntaxError as e2:
        print(f"insta485generator error: '{template_name}'")
        print(f"{e2.message}")
        sys.exit(1)
    except TemplateNotFound:
        print(f"insta485generator error: '{template_name}' not found")
        sys.exit(1)
        
    context = entry["context"]
    output = output_dir/url
    output.mkdir(parents=True, exist_ok=True)
    output_path = output/"index.html"
    output_path.touch()

    rendered_context = template.render(context)

    with output_path.open("w") as output_file:
        output_file.write(rendered_context)
        if verbose:
            print(f"Rendered {template_name} -> {output_path}")


def copy_static_file(input_dir, output_dir, verbose):
    """Copy Static File."""
    static_dir = input_dir / "static"
    if static_dir.exists():
        shutil.copytree(static_dir, output_dir, dirs_exist_ok=True)
        if verbose:
            print(f"Copied {static_dir} -> {output_dir}")
