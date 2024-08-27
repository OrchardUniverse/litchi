import time
import os



class FileWatcher:
    def __init__(self, file) -> None:
        self.monitor_file = file

        if not os.path.exists(self.monitor_file):
            print(f"Create the empty wath file since it doesn't exist: {self.monitor_file}")
            self.create_initial_file()

        
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

                    print(f"Triggered and extract the user requirement: {requirement_content}")


                    # TODO: Call function to generate code



                    # Move back to the beginning of the file and change the first line
                    file.seek(0)
                    file.write('Ready to generate? NOT READY!\n\n\n\n')

                    file.write("==================== GENERATED ====================\n")

                    file.flush()
                    os.fsync(file.fileno())
                    # Keep the rest of the file the same
                    file.write(file_contents)
        except IOError as e:
            print(f'Error reading file: {e}')


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
                print(f'File {self.monitor_file} not found. Please check the path.')
                break
