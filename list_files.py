import os
from get_config import Config

def list_files():
    try:
        config = Config().get_config()
        data_dir = config.get('data_dir') 
        file_list = []  # Initialize an empty list to store file paths
        for root, dirs, files in os.walk(data_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_list.append(file_path)  # Append the file path to the list
        return file_list   
    except Exception as e: 
        print(f"Error in listing the directory: {e}")
        
if __name__ == '__main__':
    files = list_files()
    for file in files:
        print(file)