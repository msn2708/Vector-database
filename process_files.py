from list_files import list_files
from process_file import process_file

def process_files():
  # Get the config file and set up a pool of workers to do all processing in parallel
  files = list_files()
  #list_files_to_queue()
  for file in files:
    print(f"Now processing: {file}")
    process_file(filename=file)
    
#main program
if __name__ == "__main__":
  process_files()
