# Import necessary modules
import re  # This module provides support for regular expressions, which are used to search, match, and manipulate strings based on patterns

def get_session_ids():
    try:
        # Run the command to list sessions without headers
        result = subprocess.run(['loginctl', 'list-sessions', '--no-legend'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
        # Capture and strip the stdout output
        output = result.stdout.strip()

        # Use regex to extract session IDs from the output
        session_ids = re.findall(r'^\S+', output, re.MULTILINE)

        # Return the list of session IDs
        return session_ids

    except subprocess.CalledProcessError as e:
        # Print any error that occurs during the subprocess call
        print(f"Error: {e.stderr.strip()}")
        return None
    except Exception as e:
        # Print any unexpected errors
        print(f"An unexpected error occurred: {e}")
        return None

def get_session_details(session_id):
    try:
        # Run the command to get the status of a specific session
        result = subprocess.run(['loginctl', 'session-status', session_id, '-o', 'short'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
        # Capture and strip the stdout output
        output = result.stdout.strip()

        # Extract relevant session details using regex
        details = {
            'Session ID': session_id,
            'Since': re.search(r'Since:\s+(.+)', output).group(1),
            'Leader': re.search(r'Leader:\s+(\d+)', output).group(1),
            'Seat': re.search(r'Seat:\s+(.+)', output).group(1),
            'Display': re.search(r'Display:\s+(.+)', output).group(1),
            'Service': re.search(r'Service:\s+(.+)', output).group(1),
            'Desktop': re.search(r'Desktop:\s+(.+)', output).group(1),
            'State': re.search(r'State:\s+(.+)', output).group(1),
            'Idle': re.search(r'Idle:\s+(.+)', output).group(1),
            'Unit': re.search(r'Unit:\s+(\S+)', output).group(1),
        }

        # Return the extracted session details
        return details

    except subprocess.CalledProcessError as e:
        # Print any error that occurs during the subprocess call
        print(f"Error: {e.stderr.strip()}")
        return None
    except Exception as e:
        # Print any unexpected errors
        print(f"An unexpected error occurred while processing session {session_id}: {e}")
        return None

def print_session_details(details):
    if details:
        # Print the session details
        print(f"Session {details['Session ID']} details:")
        for key, value in details.items():
            if key != 'Session ID':
                print(f"  {key}: {value}")

def main():
    # Call the function to get the list of session IDs
    session_ids = get_session_ids()

    # Check if session IDs were successfully retrieved
    if session_ids:
        print("SESSION IDs:", session_ids)

        # Loop through each session ID, get its details and print them
        for session_id in session_ids:
            details = get_session_details(session_id)
            print_session_details(details)
    else:
        # Print a message if no session IDs were found or an error occurred
        print("No session IDs found or an error occurred.")

# Entry point of the script
if __name__ == "__main__":
    main()
