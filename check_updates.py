import subprocess
import logging
import sys
import re

# Path to the OS release file
os_release_file_path = '/etc/redhat-release'

# Define a custom log level TRACE
TRACE_LEVEL_NUM = 25
# Log file
LOG_FILE = 'file.log'


def trace(self, message, *args, **kws):
    if self.isEnabledFor(TRACE_LEVEL_NUM):
        self._log(TRACE_LEVEL_NUM, message, args, **kws)


# Extend the Logger class with the trace method
class CustomLogger(logging.getLoggerClass()):
    def trace(self, message, *args, **kws):
        if self.isEnabledFor(TRACE_LEVEL_NUM):
            self._log(TRACE_LEVEL_NUM, message, args, **kws)


# Set the custom logger class
logging.setLoggerClass(CustomLogger)

# Add TRACE level to the logging module
logging.addLevelName(TRACE_LEVEL_NUM, "TRACE")


def configure_logging():
    # Configure logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler(LOG_FILE),
                            logging.StreamHandler()
                        ])


def check_updates(logger):
    try:
        # Run the dnf check-update command and capture the output
        result = subprocess.run(['dnf', 'check-update'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Return values taken from the man entry of the dnf command
        # 0   : Operation was successful, No updates available
        # 1   : An error occurred, which was handled by dnf
        # 3   : An unknown unhandled error occurred during operation
        # 100 : Updates are available and a list of the updates will be printed
        # 200 : There was a problem with acquiring or releasing of locks

        # Check the return code to determine if updates are available
        if result.returncode == 0:
            print(f"Operation was successful, No updates available.")
            logger.info(f"Operation was successful, No updates available.")
            return False
        elif result.returncode == 1:
            print(f"An error occurred, which was handled by dnf.")
            logger.error(f"An error occurred, which was handled by dnf.")
            return False
        elif result.returncode == 3:
            print(f"An unknown unhandled error occurred during operation.")
            return False
        elif result.returncode == 100:
            print(f"Updates are available.")
            return True
        elif result.returncode == 200:
            print(f"There was a problem with acquiring or releasing of locks.")
            return False
        else:
            # Handle other return codes by returning False and printing stderr
            print(result.stderr.decode())
            return False
    except subprocess.CalledProcessError as e:
        # Print any error that occurs during the subprocess call
        print(f"Error: {e.stderr.strip()}")
        return False
    except Exception as e:
        # Handle any exceptions that occur during the subprocess run
        print("An error occurred while checking for updates.")
        print(str(e))
        return False


def main():
    # Call the function to configure logging and log messages
    configure_logging()
    # Create logger
    logger = logging.getLogger(__name__)

    # Log messages
    logger.error("This is my error message")
    logger.trace("This is my trace message")

    updates_available = check_updates(logger)
    print(updates_available)


# Entry point of the script
if __name__ == "__main__":
    main()
