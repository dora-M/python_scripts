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


def get_os_release(file_path, logger):
    try:
        with open(file_path, 'r') as file:
            # Read the first line from the file
            line = file.readline().strip()
            logger.debug('Read line: {}'.format(line))

            # Use regular expression to match the OS release format
            match = re.match(r'(CentOS|Rocky) Linux release (\d+\.\d+)', line)
            if match:
                distro = match.group(1)
                version = match.group(2)
                logger.debug('Distribution: {}, Version: {}'.format(distro, version))
                return distro, version
            else:
                error_message = 'Unknown OS release format'
                logger.error(error_message)
                print(error_message, file=sys.stderr)
                return error_message, None

    except FileNotFoundError:
        error_message = 'File not found: {}'.format(file_path)
        logger.error(error_message)
        print(error_message, file=sys.stderr)
        return error_message, None

    except Exception as e:
        error_message = 'An error occurred: {}'.format(e)
        logger.error(error_message)
        print(error_message, file=sys.stderr)
        return error_message, None


def main():
    # Call the function to configure logging and log messages
    configure_logging()
    # Create logger
    logger = logging.getLogger(__name__)

    # Log messages
    logger.error("This is my error message")
    logger.trace("This is my trace message")

    distro, version = get_os_release(os_release_file_path, logger)
    if version:
        result = '{} {}'.format(distro, version)
    else:
        result = distro
    logger.info('OS Release determined: {}'.format(result))
    print(result)


if __name__ == '__main__':
    main()
