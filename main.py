from imgprocessing import processor
from server.Server import SocketServer
import cv2
import numpy as np
"""
Instantiate socket server
Start server
"""
server = SocketServer()
server.run()
