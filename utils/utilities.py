import os

def is_directory_exists(path):
    """
    Check if a directory exists at the given path.
    """
    return os.path.exists(path) and os.path.isdir(path)

def is_directory_readable(path):
    """
    Check if a directory is readable at the given path.
    """
    return os.access(path, os.R_OK)

def is_directory_writable(path):
    """
    Check if a directory is writable at the given path.
    """
    return os.access(path, os.W_OK)

def is_directory_empty(path):
    """
    Check if a directory is empty at the given path.
    """
    try:
        return not bool(os.listdir(path))
    except FileNotFoundError:
        return False

def is_file_exists(path):
    """
    Check if a file exists at the given path.
    """
    return os.path.exists(path) and os.path.isfile(path)

def is_file_readable(path):
    """
    Check if a file is readable at the given path.
    """
    return os.access(path, os.R_OK)

def is_file_writable(path):
    """
    Check if a file is writable at the given path.
    """
    return os.access(path, os.W_OK)

def replace_newlines(sentence):
    # This method replaces all instances of a newline except the last one.
    # Replace newlines with spaces
    sentence_with_spaces = sentence.replace('\n', ' ')
    
    # Find the index of the last newline character
    last_newline_index = sentence.rfind('\n')
    
    # Preserve the last newline character
    modified_sentence = sentence_with_spaces[:last_newline_index] + '\n' + sentence_with_spaces[last_newline_index+1:]
    
    return modified_sentence

# Example usage:
if __name__ == "__main__":
    directory_path = "/path/to/your/directory"
    file_path = "/path/to/your/file.txt"

    if is_directory_exists(directory_path):
        print(f"Directory '{directory_path}' exists.")
        if is_directory_readable(directory_path):
            print(f"Directory '{directory_path}' is readable.")
        if is_directory_writable(directory_path):
            print(f"Directory '{directory_path}' is writable.")
        if is_directory_empty(directory_path):
            print(f"Directory '{directory_path}' is empty.")

    if is_file_exists(file_path):
        print(f"File '{file_path}' exists.")
        if is_file_readable(file_path):
            print(f"File '{file_path}' is readable.")
        if is_file_writable(file_path):
            print(f"File '{file_path}' is writable.")
