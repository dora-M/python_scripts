import subprocess
import logging

log_file = "dnf_clean.log"


def configure_logging():
    """
    Configures the logging settings for the application.
    The format specifies how the log messages will be structured:
    %(asctime)s: Timestamp of the log entry.
    %(levelname)s: The log level (e.g., INFO, ERROR).
                                DEBUG: Detailed information, typically of interest only when diagnosing problems.
                                INFO: Confirmation that things are working as expected.
                                WARNING: An indication that something unexpected happened, or indicative of some
                                    problem in the near future (e.g., ‘disk space low’). The software is still working
                                    as expected.
                                ERROR: Due to a more serious problem, the software has not been able to perform some
                                    function.
                                CRITICAL: A very serious error, indicating that the program itself may be unable to
                                    continue running.
    %(message)s: The actual log message content.
    """
    logging.basicConfig(filename=log_file,
                        level=logging.INFO,
                        format='%(asctime)s %(levelname)s: %(message)s')


def run_dnf_clean():
    try:
        # Run the 'dnf clean all' command
        result = subprocess.run(
            ['dnf', 'clean', 'all'],
            check=False,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        # Return values taken from the man entry of the dnf command
        # 0   : Operation was successful.
        # 1   : An error occurred, which was handled by dnf.
        # 3   : An unknown unhandled error occurred during operation.
        # 200 : here was a problem with acquiring or releasing of locks.

        # Check the return code and log appropriate messages
        if result.returncode == 0:
            # Operation was successful
            logging.info("Operation was successful.")
        elif result.returncode == 1:
            # An error occurred, which was handled by dnf
            logging.error(f"An error occurred, which was handled by dnf: {result.stdout}")
        elif result.returncode == 3:
            # An unknown unhandled error occurred during operation
            logging.error(f"An unknown unhandled error occurred during operation: {result.stdout}")
        elif result.returncode == 200:
            # There was a problem with acquiring or releasing of locks
            logging.error(f"There was a problem with acquiring or releasing of locks: {result.stdout}")
        else:
            # Log any other unexpected return codes
            logging.error(f"Unexpected return code {result.returncode}: {result.stdout}")

