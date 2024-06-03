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

    except Exception as e:
        # Handle any other exceptions and log the error
        logging.error(f"Exception: {str(e)}")


def remove_all_dnf_cache():
    """
    Removes all files in the /var/cache/dnf directory.
    Logs the operation.
    """
    try:
        subprocess.run(["rm", "-rf", "/var/cache/dnf/*"], check=True)
        logging.info("Successfully removed all files in /var/cache/dnf")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to remove files: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


def are_updates_available():
    try:
        # Run the dnf check-update command and capture the output
        result = subprocess.run(['dnf', 'check-update'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout_message = result.stdout.decode()
        stderr_message = result.stderr.decode()

        # Log the stdout and stderr messages
        if stdout_message:
            logging.info(stdout_message)
        if stderr_message:
            logging.error(stderr_message)

        # Return values taken from the man entry of the dnf command
        # 0   : Operation was successful, No updates available
        # 1   : An error occurred, which was handled by dnf
        # 3   : An unknown unhandled error occurred during operation
        # 100 : Updates are available and a list of the updates will be printed
        # 200 : There was a problem with acquiring or releasing of locks

        # Check the return code to determine if updates are available
        if result.returncode == 0:
            message = "Operation was successful, No updates available."
            logging.info(message)
        elif result.returncode == 1:
            message = "An error occurred, which was handled by dnf."
            logging.error(message)
            logging.error(stderr_message)  # Log stderr
        elif result.returncode == 3:
            message = "An unknown unhandled error occurred during operation."
            logging.critical(message)
            logging.critical(stderr_message)  # Log stderr
        elif result.returncode == 100:
            message = "Updates are available."
            logging.info(message)
            return True
        elif result.returncode == 200:
            message = "There was a problem with acquiring or releasing of locks."
            logging.warning(message)
            logging.warning(stderr_message)  # Log stderr
        else:
            # Handle other return codes by returning False and printing stderr
            logging.error(stderr_message)
    except subprocess.CalledProcessError as e:
        # Print any error that occurs during the subprocess call
        error_message = f"Error: {e.stderr.strip()}"
        logging.error(error_message)
    except Exception as e:
        # Handle any exceptions that occur during the subprocess run
        error_message = "An error occurred while checking for updates."
        logging.critical(error_message)
        logging.critical(str(e))
    finally:
        return False


def main():
    configure_logging()
    run_dnf_clean()
    remove_all_dnf_cache()
    updates_available = are_updates_available()
    logging.info(f"Updates available: {updates_available}")


if __name__ == "__main__":
    main()
