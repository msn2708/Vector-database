from multiprocessing import Pool 
from process_file import process_file
from list_files import list_files
from get_config import Config
import concurrent.futures
import os
import sys

def process_files(data_dir):
  # Get the config file and set up a pool of workers to do all processing in parallel
  config = Config().get_config()
  files = list_files()
  print(files)
  #p = Pool(processes=None)
  #chunks = p.map(process_file, files)
  #chunks = p.map(process_file, [(os.path.join(data_dir, f),config) for f in files])

  executor = concurrent.futures.ThreadPoolExecutor()
  chunks = executor.map(process_file, [(os.path.join(data_dir, f),config) for f in files])
  return chunks

"""
  for file in files:
    args = [(os.path.join(data_dir, file),config)]
    
  chunks = p.map(process_file, args)
  p.close()
  p.join()
"""
#main program to invoke
if __name__ == "__main__":
  process_files("/Users/smohammed/Downloads/documents")