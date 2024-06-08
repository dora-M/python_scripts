import subprocess
import re
import logging

log_file = "sessions.log"


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
                        level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s: %(message)s')


def get_session_ids():
    try:
        message = f'Running loginctl command: loginctl list-session --no-legend'
        logging.debug(message)
        result = subprocess.run(['loginctl', 'list-sessions', '--no-legend'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
        message = f'Command output:\n{result.stdout}'
        logging.debug(message)
        output = result.stdout.strip()
        session_ids = re.findall(r'^\S+', output, re.MULTILINE)
        message = f'Extracted session IDs: {session_ids}'
        logging.info(message)
        return session_ids
    except subprocess.CalledProcessError as e:
        # Print any error that occurs during the subprocess call
        error_message = (f'loginctl list-session: '
                         f'An error occurred while checking the state of the login manager call: {e.stderr.strip()}')
        logging.error(error_message)
    except Exception as e:
        # Handle any exceptions that occur during the subprocess run
        error_message = (f'loginctl list-session: '
                         f'An error occurred while checking the state of the login manager: {e.stderr.strip()}')
        logging.critical(error_message)


def get_session_details(session_id):
    try:
        message = f'Getting details for session ID: {session_id}'
        logging.debug(message)
        result = subprocess.run(['loginctl', 'session-status', session_id, '-o', 'short'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
        message = f'Session details output:\n{result.stdout}'
        logging.debug(message)
        output = result.stdout.strip()
        details = {
            'Session ID': session_id,
            'Since': re.search(r'Since:\s+(.+)', output).group(1),
            'Leader': re.search(r'Leader:\s+(\d+)', output).group(1),
            'Seat': re.search(r'Seat:\s+(.+)', output).group(1),
            'Display': re.search(r'Display:\s+(.+)', output).group(1),
            'Service': re.search(r'Service:\s+(.+)', output).group(1),
            #'Desktop': re.search(r'Desktop:\s+(.+)', output).group(1),
            'State': re.search(r'State:\s+(.+)', output).group(1),
            #'Idle': re.search(r'Idle:\s+(.+)', output).group(1),
            'Unit': re.search(r'Unit:\s+(\S+)', output).group(1),
        }
        message = f'xtracted details: {details}'
        logging.debug(message)
        return details
    except subprocess.CalledProcessError as e:
        # Print any error that occurs during the subprocess call
        error_message = (f'loginctl session-status: '
                         f'An unexpected error occurred while processing session call: {e.stderr.strip()}')
        logging.error(error_message)
        return None
    except Exception as e:
        # Handle any exceptions that occur during the subprocess run
        error_message = (f'loginctl session-status: '
                         f'An unexpected error occurred while processing session: {e.stderr.strip()}')
        logging.critical(error_message)
        return None


def print_session_details(details):
    if details:
        print(f"Session {details['Session ID']} details:")
        for key, value in details.items():
            if key != 'Session ID':
                print(f"  {key}: {value}")


def main():
    configure_logging()
    print("Starting main function...")
    session_ids = get_session_ids()
    if session_ids:
        print("SESSION IDs:", session_ids)
        for session_id in session_ids:
            details = get_session_details(session_id)
            print_session_details(details)
    else:
        print("No session IDs found or an error occurred.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        error_message = f'An unexpected error occurred: {e.stderr.strip()}'
        logging.error(error_message)
