import sys
import os

# Add the parent directory to the sys.path to allow imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from file_organizer.main import main

if __name__ == "__main__":
    main()