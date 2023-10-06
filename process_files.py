from list_files import list_files
from process_file import process_file
from text_processor_exception import TextProcessingError

def process_files():
  
  #Get the list of files to process
  try:
    files = list_files()
    for file in files:
      process_file(file)
  except Exception as e:
    raise TextProcessingError(f"process_files: Encountered an error when processing file: {file}", original_exception=e)
  
    
      
    
    
#main program
if __name__ == "__main__":
  process_files()
