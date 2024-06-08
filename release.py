import logging
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


def get_distribution(file_path, logger):
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
                return distro
            else:
                logger.error('Unrecognized OS release format found in file: {}. Content: "{}"'.format(file_path, line))
                return 'Unknown'

    except FileNotFoundError:
        logger.error('File not found: {}'.format(file_path))
        return 'Unknown'

    except Exception as error_distribution:
        logger.error('An error occurred: {}'.format(error_distribution))
        return 'Unknown'


def next_func(distribution, logger):
    # Placeholder for the next function that uses the distribution variable
    logger.info('OS Release determined: {}'.format(distribution))


def main():
    # Call the function to configure logging and log messages
    configure_logging()
    # Create logger
    logger = logging.getLogger(__name__)

    distribution = get_distribution(os_release_file_path, logger)
    if distribution in ['CentOS', 'Rocky']:
        next_func(distribution, logger)
    else:
        logger.warning('Unsupported distribution: {}'.format(distribution))


if __name__ == '__main__':
    try:
        main()
        logging.error('This is an line to be deleted: xxxxxxxxxxxxxxxxxxxx')
    except Exception as unexpected_error:
        logging.error('An unexpected error occurred: {}'.format(unexpected_error))
