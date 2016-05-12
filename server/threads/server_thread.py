import os
import sys
import socket
import numpy as np
#import cv2
import logging
import errno
from threading import Thread

from properties import property as prop

class ImageHandlerThread(Thread):

    __client = None
    __address = None

    def __init__(self, client, address):
        """
        Construct a new ImageModifierThread object.
        """
        Thread.__init__(self)
        self.__client = client
        self.__address = address

    def __del__(self):
        del self.__client
        del self.__address

    def run(self):
        """
        Callable method.
        Handle image receive from client and return the modified image to client.
            
        :return:
        """
        client = self.__client
        address = self.__address
        client.send("Connected to the server with name " + str(address[1]) + ". Send an image of the analysis." + os.linesep)
        option = self.__getOptionFromClient(client)
        logging.info("Client option value: " + str(option))
        
        byte_array = self.__getImageOnByteArray(client)
        logging.info("Image arrived from client " + str(address[1]))
        client.send("IMG_OK")
        
        np_barray = np.fromstring(byte_array, np.uint8)
        #img = cv2.imdecode(np_barray, cv2.IMREAD_COLOR)
        #cv2.imshow("image", img)
        #cv2.waitKey(0)

        """ openCv method call at this point """

        self.__sendImageToClient(client, np_barray)
        logging.info("Sent modified picture to client " + str(address[1]))
        
        logging.debug("Client " + str(address[1]) + " closed")
        client.close()

    def  __getOptionFromClient(self, client):
        option = None
        while option == None:
            try: 
                data = client.recv(sys.getsizeof(int()))
                if not data:
                    break
                option = data
            except socket.error as error:
                if error.args[0] == errno.EAGAIN or error.args[0] == errno.EWOULDBLOCK:
                    continue
                else:
                    logging.error("Get option value from client error: " +  str(error))
                    sys.exit(1)
        return option

    def __getImageOnByteArray(self, client):
        total_data = b""
        while True:
            try: 
                data = client.recv(prop.BUFF_SIZE)
                if not data:
                    break
                total_data += data
            except socket.error as error:
                if error.args[0] == errno.EAGAIN or error.args[0] == errno.EWOULDBLOCK:
                    continue
                else:
                    logging.error("Get image from client error: " +  str(error))
                    sys.exit(1)
        return total_data

    def __sendImageToClient(self, client, np_barray):
        try:
            client.send(np_barray)
        except socket.error as error:
            logging.error("Image send error: " + str(error))
