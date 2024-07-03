import sys
import os
import multiprocessing

# Ensure the current directory is in the sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app_rancho
from appviru import app_viru

def run_rancho():
    app_rancho.run(port=5000, debug=True)

def run_viru():
    app_viru.run(port=5001, debug=True)

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=run_rancho)
    p2 = multiprocessing.Process(target=run_viru)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
