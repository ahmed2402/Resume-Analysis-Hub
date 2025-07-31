import sys
import os

# Add your project directory to the sys.path
path = '/home/ahmvd/Resume-Analysis-Hub'
if path not in sys.path:
    sys.path.append(path)

from home import app as application 