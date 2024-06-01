# Import necessary modules
import subprocess  # This module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes.

def check_updates():
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
            return False
        elif result.returncode == 1:
            print(f"An error occurred, which was handled by dnf.")
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
    updates_available = check_updates()
    print(updates_available)


# Entry point of the script
if __name__ == "__main__":
    main()
