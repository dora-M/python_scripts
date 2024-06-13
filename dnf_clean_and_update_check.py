import subprocess
import logging

log_file = "dnf_clean.log"


def configure_logging():
    """
Configures the logging settings for the application.
The format specifies how the log messages will be structured:
    %(asctime)s: Timestamp of the log entry.
    %(levelname)s: The log level (e.g., INFO, ERROR).
    %(message)s: The actual log message content

Logging Levels:
logging.NOTSET    0 When set on a logger, indicates that ancestor loggers are to be consulted to determine the
                    effective level. If that still resolves to NOTSET, then all events are logged. When set on a
                    handler, all events are handled.
logging.DEBUG    10 Detailed information, typically only of interest to a developer trying to diagnose a problem.
logging.INFO     20 Confirmation that things are working as expected.
logging.WARNING  30 An indication that something unexpected happened, or that a problem might occur in the near
                    future (e.g. ‘disk space low’). The software is still working as expected.
logging.ERROR    40 Due to a more serious problem, the software has not been able to perform some function.
logging.CRITICAL 50 A serious error, indicating that the program itself may be unable to continue running.
    """
    logging.basicConfig(filename=log_file,
                        level=logging.INFO,
                        format="%(asctime)s %(levelname)s: %(message)s")


def run_dnf_clean():
    try:
        # Run the dnf clean all command and capture the output
        result = subprocess.run(["dnf", "clean", "all"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout_message = result.stdout.decode()
        stderr_message = result.stderr.decode()

        # Return values taken from the man entry of the dnf command
        # 0   : Operation was successful
        # 1   : An error occurred, which was handled by dnf
        # 3   : An unknown unhandled error occurred during operation
        # 200 : There was a problem with acquiring or releasing of locks

        # Check the return code to determine if updates are available
        if result.returncode == 0:
            message = f"dnf clean all: Operation was successful."
            logging.info(message)
        elif result.returncode == 1:
            message = (f"dnf clean all: An error occurred, which was handled by dnf."
                       f"\nSTDOUT: {stdout_message}"
                       f"\nSTDERR: {stderr_message}")
            logging.error(message)
        elif result.returncode == 3:
            message = (f"dnf clean all: An unknown unhandled error occurred during operation."
                       f"\nSTDOUT: {stdout_message}"
                       f"\nSTDERR: {stderr_message}")
            logging.critical(message)
        elif result.returncode == 200:
            message = f"dnf clean all: There was a problem with acquiring or releasing of locks."
            logging.warning(message)
        else:
            message = (f"dnf clean all: Unexpected return code: {result.returncode}"
                       f"\nSTDOUT: {stdout_message}"
                       f"\nSTDERR: {stderr_message}")
            logging.error(message)
    except subprocess.CalledProcessError as e:
        # Print any error that occurs during the subprocess call
        message = f"dnf clean all: An error occurred while dnf clean call: {e.stderr.strip()}"
        logging.error(message)
    except subprocess.TimeoutExpired as e:
        # Handle timeout exception
        message = f"dnf clean all: The command timed out: {e.stderr.strip() if e.stderr else 'No stderr'}"
        logging.error(message)
    except subprocess.SubprocessError as e:
        # Handle other subprocess errors
        message = f"dnf clean all: A subprocess error occurred: {str(e)}"
        logging.error(message)
    except Exception as e:
        # Handle any other exceptions that occur during the subprocess run
        message = f"dnf clean all: An error occurred while running dnf clean: {str(e)}"
        logging.critical(message)


def remove_all_dnf_cache():
    """
    Removes all files in the /var/cache/dnf directory.
    Logs the operation.
    """
    try:
        subprocess.run(["rm", "-rf", "/var/cache/dnf/*"], check=True)
        message = f"dnf clear cache: Successfully removed all files in /var/cache/dnf"
        logging.info(message)
    except subprocess.CalledProcessError as e:
        message = f"dnf clear cache: Failed to remove files: {e.stderr.strip() if e.stderr else str(e)}"
        logging.error(message)
    except subprocess.TimeoutExpired as e:
        message = f"dnf clear cache: Command timed out: {e.stderr.strip() if e.stderr else 'No stderr'}"
        logging.error(message)
    except subprocess.SubprocessError as e:
        message = f"dnf clear cache: A subprocess error occurred: {str(e)}"
        logging.error(message)
    except Exception as e:
        message = f"dnf clear cache: An unexpected error occurred: {str(e)}"
        logging.critical(message)


def are_updates_available():
    try:
        # Run the dnf check-update command and capture the output
        result = subprocess.run(["dnf", "check-update"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout_message = result.stdout.decode()
        stderr_message = result.stderr.decode()

        # Return values taken from the man entry of the dnf command
        # 0   : Operation was successful, No updates available
        # 1   : An error occurred, which was handled by dnf
        # 3   : An unknown unhandled error occurred during operation
        # 100 : Updates are available and a list of the updates will be printed
        # 200 : There was a problem with acquiring or releasing of locks

        # Check the return code to determine if updates are available
        if result.returncode == 0:
            message = f"dnf check-update: Operation was successful, No updates available."
            logging.info(message)
        elif result.returncode == 1:
            message = (f"dnf check-update: An error occurred, which was handled by dnf."
                       f"\nSTDOUT: {stdout_message}"
                       f"\nSTDERR: {stderr_message}")
            logging.error(message)
        elif result.returncode == 3:
            message = (f"dnf check-update: An unknown unhandled error occurred during operation."
                       f"\nSTDOUT: {stdout_message}"
                       f"\nSTDERR: {stderr_message}")
            logging.critical(message)
        elif result.returncode == 100:
            message = f"dnf check-update: Updates are available."
            logging.info(message)
            return True
        elif result.returncode == 200:
            message = f"dnf check-update: There was a problem with acquiring or releasing of locks."
            logging.warning(message)
        else:
            message = (f"dnf check-update: Unexpected return code: {result.returncode}"
                       f"\nSTDOUT: {stdout_message}"
                       f"\nSTDERR: {stderr_message}")
            logging.error(message)
    except subprocess.CalledProcessError as e:
        # Print any error that occurs during the subprocess call
        message = f"dnf check-update: An error occurred while checking for updates call: {e.stderr.strip()}"
        logging.error(message)
    except subprocess.TimeoutExpired as e:
        # Handle timeout exception
        message = f"dnf check-update: The command timed out: {e.stderr.strip() if e.stderr else 'No stderr'}"
        logging.error(message)
    except subprocess.SubprocessError as e:
        # Handle other subprocess errors
        message = f"dnf check-update: A subprocess error occurred: {str(e)}"
        logging.error(message)
    except Exception as e:
        # Handle any other exceptions that occur during the subprocess run
        message = f"dnf check-update: An error occurred while checking for updates: {str(e)}"
        logging.critical(message)
    finally:
        return False


def main():
    configure_logging()
    run_dnf_clean()
    remove_all_dnf_cache()
    are_updates_available()


if __name__ == "__main__":
    main()
