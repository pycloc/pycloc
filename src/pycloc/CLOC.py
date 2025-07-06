from pycloc.utils import CLOCException
import subprocess
import os

class CLOC:
    def __init__(self):
        self.base_command = "cloc"
        self.options = []
        self.flags = []
        self.arguments = []
        self.working_directory = os.getcwd()

    def add_option(self, option, value):
        """Adds an option with a value (e.g., --output file.txt)."""
        self.options.append(f"{option} {value}")
        return self

    def add_flag(self, flag):
        """Adds a flag (e.g., --verbose, -v)."""
        self.flags.append(flag)
        return self

    def add_argument(self, argument):
        """Adds a positional argument (e.g., filename)."""
        self.arguments.append(argument)
        return self
    
    def set_working_directory(self, path):
        """Sets the working directory for the command."""
        self.working_directory = path
        return self

    def build(self):
        """Constructs the full CLI command string."""
        parts = [self.base_command] + self.flags + self.options + self.arguments
        return " ".join(parts)
    
    def execute(self):
        """Executes the CLI command, returns raw process result or Exception."""
        command = self.build()
        try:
            process = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, cwd=self.working_directory)
            return process.stdout.decode("utf-8")
        except subprocess.CalledProcessError as error:
            match error.returncode:
                case 25:
                    message = 'Failed to create tarfile of files from git or not a git repository.'
                case 126:
                    message = 'Permission denied. Please check the permissions of the working directory.'
                case 127:
                    message = 'CLOC command not found. Please install CLOC.'
                case _: 
                    message = 'Unknown CLOC error: ' + str(error)

            if error.returncode < 0 or error.returncode > 128:
                message = 'CLOC command was terminated by signal ' + str(-error.returncode)
        
            raise CLOCException(message, error.returncode)
