from list_files_to_queue import list_files_to_queue
from process_files_from_queue import process_files_from_queue

    
def start_text_processing ():
  list_files_to_queue ()
  
  process_files_from_queue()


if __name__ == '__main__':
  start_text_processing ()
  