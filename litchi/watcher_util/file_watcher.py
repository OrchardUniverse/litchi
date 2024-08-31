import time
import os
import logging

from ..index_util.llm_util import LlmUtil
from ..cli.gen_command import generate_source_file

class FileWatcher:
    def __init__(self, file, project_path: str = "./") -> None:
        self.monitor_file = file

        if not os.path.exists(self.monitor_file):
            logging.info(f"Create the empty wath file since it doesn't exist: {self.monitor_file}")
            self.create_initial_file()

        self.llm_util = LlmUtil(project_path)

        
    def create_initial_file(self):
        with open(self.monitor_file, 'w') as file:
            file.write('Ready to generate? NOT READY!\n\n')
            file.write('Do something like checking if the port 8080 is occupied.\n')

        
    def check_file_ready(self, file_path):
        try:
            with open(file_path, 'r+') as file:
                file_contents = file.read()
                lines = file_contents.splitlines()

                if lines[0] == 'Ready to generate? READY!':
                    
                    # Remove the system hint 
                    requirement_content = ""
                    lines = file_contents.splitlines()[2:]
                    for i, line in enumerate(lines):
                        if line.startswith("===================="):
                            lines = lines[:i]
                            break
                    requirement_content = '\n'.join(lines)

                    logging.info(f"Triggered and extract the user requirement: {requirement_content}")


                    # TODO: Reuse generate function to generate code
                    output_string = self.generate_code(requirement_content)
                    # generate_source_file(requirement_content, file_path, False, "")

                    # Move back to the beginning of the file and change the first line
                    file.seek(0)
                    file.write('Ready to generate? NOT READY!\n\n\n\n')

                    file.write("==================== GENERATED ====================\n\n")

                    file.write(output_string)
                    file.write("\n\n")

                    file.flush()
                    os.fsync(file.fileno())
                    # Keep the rest of the file the same
                    file.write(file_contents)
        except IOError as e:
            logging.error(f'Error reading file: {e}')


    def start_watching(self):
        last_modified = None

        while True:
            try:
                current_modified = os.path.getmtime(self.monitor_file)
                if last_modified is None:
                    last_modified = current_modified

                if current_modified != last_modified:
                    self.check_file_ready(self.monitor_file)
                    last_modified = current_modified

                time.sleep(1)
            except KeyboardInterrupt:
                break
            except FileNotFoundError:
                logging.error(f'File {self.monitor_file} not found. Please check the path.')
                break

    def generate_code(self, requirement_content) -> str:
        gencode_output = self.llm_util.call_llm_to_gencode(requirement_content, "", "")

        if gencode_output.output_file == "":
            logging.error("Error: output file path is empty.")
            return ""
        else:
            logging.info(f"Generate file path: {gencode_output.output_file}")

        try:
            with open(gencode_output.output_file, 'w') as file:
                file.write(gencode_output.code)
                output_message = f"Generate code and write to `{gencode_output.output_file}`:\n\n```\n{gencode_output.code}\n```"
                logging.info(output_message)
                return output_message
        except Exception as e:
            logging.error(f"An error occurred while writing to the file: {e}")