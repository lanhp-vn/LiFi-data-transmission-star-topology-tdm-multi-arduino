import os

def get_file_size(file_path):
    """Returns the size of the file in bytes."""
    try:
        # Get the size of the file in bytes
        size = os.path.getsize(file_path)
        return size
    except OSError as e:
        # Handle the error if file does not exist or is inaccessible
        return f"Error: {e}"

# Example usage
file_path = './Input_Output_files./user1.txt'
print(f"The size of the file is {get_file_size(file_path)} bytes.")
