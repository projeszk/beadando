import os
import sys
import socket
import numpy as np
import logging
import errno
from server.properties import property as prop
from imgprocessing.processor import Processor
from threading import Thread
from random import randint

class ImageHandlerThread(Thread):
    """
    Image network handler thread.
    """

    __client = None
    __address = None

    def __init__(self, client, address):
        """
        Construct a new ImageModifierThread object.

        :param client:
        :param address:
        :return
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
        #option = self.__getOptionFromClient(client)
        #logging.info("Client option value: " + str(option))
        
        byte_array = self.__getImageOnByteArray(client)
        logging.info("Image arrived from client " + str(address[1]))
        client.send("IMG_OK")
        
        np_barray = np.fromstring(byte_array, np.uint8)
        img = cv2.imdecode(np_barray, cv2.IMREAD_COLOR)
        img = catInTheSack(randint(0,3), img)
        
        """ openCv method call at this point """

        self.__sendImageToClient(client, cv2.imencode('.jpg', proc)[1].tostring())
        logging.info("Sent modified picture to client " + str(address[1]))
        
        logging.debug("Client " + str(address[1]) + " closed")
        client.close()

    def  __getOptionFromClient(self, client):
        """
        Receive option integer from client side.

        :param client:
        :type client: Socket object
        :return: option value
        :rtype: number
        """
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
        """
        Receive image from client, and convert it to byte array.

        :param client:
        :type client: Socket object
        :return: image reprezenting byte array
        :rtype: byte array
        """
        total_data = b""
        while True:
            try: 
                data = client.recv(1024)
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
        """
        Send modified image to client.

        :param client:
        :type client: Socket object
        :param np_barray:
        :type np_barray: numpy byte array
        :return:
        """
        try:
            client.send(np_barray)
        except socket.error as error:
            logging.error("Image send error: " + str(error))
    
    def __catInTheSack(self, rndnumber, img):
        """
        Returns processed image based on random number.

        :param rndnumber: random number
        :type rndnumber: number
        :param img: image received from client
        :type img: numpy.array
        :return: processed image
        :rtype: numpy.array
        """
        if (rndnumber == 0):
            return Processor().detectCannyEdges(img)
        elif (rndnumber == 1):
            return Processor().detectLaplacianEdges(img)
        elif (rndnumber == 2):
            return Processor().haarCascadeDetection(img)
        elif (rndnumber == 3):
            return Processor().harrisCornerDetection(img)
