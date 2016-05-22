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
import cv2
import time
import struct

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
        #option = self.__getOptionFromClient(client)
        #logging.info("Client option value: " + str(option))
        
        byte_array = self.__getImageOnByteArray(client)
        logging.info("Image arrived from client " + str(address[1]))
        
        np_barray = np.fromstring(byte_array, np.uint8)
        img = cv2.imdecode(np_barray, cv2.IMREAD_COLOR)
        img = self.__catInTheSack(randint(0,3), img)
        """ openCv method call at this point """
        time.sleep(1)
        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),100]
        result, imgencode = cv2.imencode('.jpg', img, encode_param)
        self.__sendImageToClient(client, np.array(imgencode).tostring())
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
        print "Receiving image"
        total_data = b""
        while True:
            try: 
                data = client.recv(1024)    
                if data[0:2] == 'ok':
                    break
                total_data += data
                client.send('0')
            except socket.error as error:
                if error.args[0] == errno.EAGAIN or error.args[0] == errno.EWOULDBLOCK:
                    continue
                else:
                    logging.error("Get image from client error: " +  str(error))
                    sys.exit(1)
        return total_data

    def __sendImageToClient(self, client, image_array):
        """
        Send modified image to client.

        :param client:
        :type client: Socket object
        :param image_array:
        :type image_array: numpy byte array
        :return:
        """
        try:
            int_in_bytes = struct.pack('!i',len(image_array))
            print len(image_array)
            client.send(int_in_bytes)
            print client.recv(1024)
            chunks = len(image_array)/1024
            i = 0
            while(i<chunks):
                print "Sending {}. chunk".format(i)
                client.send(image_array[i*1024:i*1024+1024])
                print i*1024+1024
                print client.recv(1024)
                i += 1
            client.send(image_array[i*1024:len(image_array) - i*1024])
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
