import os

# Reading the text file by joining path and file name
def read_file_txt(file_path, file_name):
    """
    Reads the content of a text file and returns it as a string.

    This function constructs the full file path by combining the provided 
    directory path and file name, then opens the file in read mode with UTF-8 
    encoding and reads its content.

    Args:
        file_path (str): The directory path where the file is located.
        file_name (str): The name of the file to be read, including its extension.

    Returns:
        str: The content of the file as a string.

    Raises:
        FileNotFoundError: If the file does not exist at the specified path.
        PermissionError: If the file cannot be accessed due to insufficient permissions.
        UnicodeDecodeError: If the file contains characters that cannot be decoded using UTF-8.
        OSError: For other issues related to file handling, such as invalid paths.

    Example:
        >>> content = read_file_txt('/Users/vahid/Documents', 'example.txt')
        >>> print(content)
        This is the content of the example.txt file.
    """
    full_path = os.path.join(file_path, file_name)
    with open(full_path, 'r', encoding='utf-8') as file:
        return file.read()
    

