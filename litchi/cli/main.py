import click
import os
from . import init_command
from . import source_command
from . import index_command
from . import chat_command
from . import gen_command
from . import opt_command
from . import watch_command

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
@click.option("--all", is_flag=True, help="Create index for all files.")
def index_create(file_path, all):
    """Create index for a specified file or all files."""
    index_command.create_index(file_path, all)


@index.command("show")
@click.argument("file_path", required=False)
@click.option("--all", is_flag=True, help="Show index for all files.")
def index_show(file_path, all):
    """Show index for a specified file or all files."""
    index_command.show_index(file_path, all)

@index.command("diff")
@click.argument("file_path", required=False)
@click.option("--all", is_flag=True, help="Update index for all files.")
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
@click.option("--output-file", required=False, help="Output the related file list in file.")
def index_query(query, output_file):
    """Query to get the related indexes."""
    index_command.query_indexes(query, output_file)


@index.command("copy-to-source")
def index_copytosource():
    """Copy the index json file to source file's directory."""
    index_command.copy_indexes_to_source_code()

@index.command("delete-from-source")
def index_deletefromsource():
    """Delete the index content from source file's directory."""
    index_command.delete_indexes_from_source_code()

@click.command("gen")
@click.argument("query_or_file")
@click.option("--file", required=False, default="", help="Generate the code which is based on the file.")
@click.option("--run", is_flag=True, default=False, help="If run the generated code or not.")
@click.option("--language", required=False, default="", help="The programming language to generate.")
def gen(query_or_file, file, run, language):
    """Generate the source code based on user's query and indexes."""
    gen_command.generate_source_file(query_or_file, file, run, language)

@click.command("opt")
@click.argument("file")
@click.argument("query_or_file")
@click.option("--inplace", is_flag=True, default=False, help="If replace the origin source file or not.")
@click.option("--dry-run", is_flag=True, default=False, help="If only generate the code without writing.")
def opt(file, query_or_file, inplace, dry_run):
    """Generate the source code based on user's query and indexes."""
    opt_command.optimize_code(file, query_or_file, inplace, dry_run)

@click.command("chat")
@click.argument("query")
@click.option("--file", required=False, help="Use the file to chat with.")
@click.option("--files", required=False, help="Use the files in index file to chat.")
@click.option("--with-index", is_flag=True, help="Generate code with generated indexes.")
def chat(query, file, files, with_index):
    """Ask questions or chat to the source codes with indexes."""
    chat_command.chat(query, file, files, with_index)


@click.command("watch")
@click.argument("file", required=True)
def watch(file):
    """Watch the requirement file for changes and auto-generate code."""
    watch_command.watch_file(file)


# Adding commands to the main CLI group
cli.add_command(init)
cli.add_command(source)
cli.add_command(index)
cli.add_command(gen)
cli.add_command(opt)
cli.add_command(chat)
cli.add_command(watch)

# Adding sub-commands to the respective command groups
source.add_command(source_create)
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
