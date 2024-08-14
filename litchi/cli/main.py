import click
import os
from . import init_command
from . import source_command
from . import index_command

from .utils import (
    initialize_project,
    update_source_files,
    create_index,
    show_index,
    update_index,
    search_index,
    generate_code,
)


@click.group()
def cli():
    """Litchi CLI tool."""
    pass


# Initialize project command
@click.command()
@click.argument("project_path")
@click.option("--language", default="", help="The language for indexing and LLM output.")
def init(project_path, language):
    """Initialize a new project with litchi files."""
    init_command.init_project(project_path, language)


# Source command group
@click.group()
def source():
    """Manager the source files to read or create index."""
    pass

@source.command("create")
def source_create():
    """Create the local file source_files.yaml."""
    source_command.create_source_file()

@source.command("update")
def source_update():
    """Update the source_files.yaml with current source files."""
    source_command.update_source_file()

@source.command("diff")
def source_diff():
    """Show the diff of current source files and source_files.yaml."""
    source_command.diff_from_source_file()

# Index command group
@click.group()
def index():
    """Manager the indexes of source files."""
    pass

@index.command("create")
@click.argument("file_path", required=False)
@click.option("--all", is_flag=True, help="Create index for all files")
def index_create(file_path, all):
    """Create index for a specified file or all files."""
    index_command.create_index(file_path, all)


@index.command("show")
@click.argument("file_path", required=False)
@click.option("--all", is_flag=True, help="Show index for all files")
def index_show(file_path, all):
    """Show index for a specified file or all files."""
    index_command.show_index(file_path, all)

@index.command("diff")
@click.argument("file_path", required=False)
@click.option("--all", is_flag=True, help="Update index for all files")
def index_diff(file_path, all):
    """Show diff of index for a specified file or all files."""
    index_command.show_index_diff(file_path, all)

@index.command("update")
@click.argument("file_path", required=False)
@click.option("--all", is_flag=True, help="Update index for all files")
def index_update(file_path, all):
    """Update index for a specified file or all files."""
    index_command.update_index(file_path, all)

@index.command("delete")
@click.argument("file_path", required=False)
@click.option("--all", is_flag=True, help="Update index for all files")
def index_delete(file_path, all):
    """Delete the index for a specified file or all files."""
    index_command.delete_index(file_path, all)

@index.command("query")
@click.argument("query")
def index_query(query):
    """Query to get the related indexes."""
    index_command.query_indexes(query)


@index.command("copytosource")
def index_copytosource():
    """Copy the index content to source file's directory."""
    search_index("")

@index.command("deletefromsource")
def index_deletefromsource():
    """Delete the index content from source file's directory."""
    search_index("")

@click.command("gen")
@click.argument("query")
@click.option("--diff", is_flag=True, help="Show diff with existing code")
@click.option("--without-index", is_flag=True, help="Generate code without updating index")
def gen(query, diff, without_index):
    """Generate the source code based on user's query and indexes."""
    generate_code(query, diff, without_index)


@click.command("chat")
@click.argument("query")
def chat(query):
    """Ask questions or chat to the source codes with indexes."""
    os.system(query)

@click.command("execute")
@click.argument("query")
@click.option("--dry-run", is_flag=True, help="Generate the code without executing")
def execute(query):
    """Generate and execute a script file from user's query."""
    os.system(query)

@click.command()
def console():
    """Use a user-friendly console interface for litchi."""
    print("The method is not supported yet")


@click.command("watch")
@click.argument("requirement_file")
def watch(requirement_file):
    """Watch the requirement file for changes and auto-generate code."""
    print("The method is not supported yet")


# Adding commands to the main CLI group
cli.add_command(init)
cli.add_command(console)
cli.add_command(source)
cli.add_command(index)
cli.add_command(gen)
cli.add_command(chat)
cli.add_command(execute)
cli.add_command(watch)

# Adding sub-commands to the respective command groups
source.add_command(source_update)

index.add_command(index_create)
index.add_command(index_show)
index.add_command(index_update)
index.add_command(index_diff)
index.add_command(index_delete)
index.add_command(index_query)

index.add_command(index_copytosource)
index.add_command(index_deletefromsource)


if __name__ == "__main__":
    cli()
