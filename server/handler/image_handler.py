import os
import sys
import socket
import logging
import errno
from properties import property as prop

def run(client, address):
    """
    Callable method.
    Handle image receive from client and return the modified image to client.
        
    :return:
    """
    client.send("Connected to the server with name " + str(address[1]) + ". Send an image of the analysis." + os.linesep)
    
    raw_img_filename = str(address[1]) + "_img.jpg"
    with open(prop.TMP_DIR + raw_img_filename, "wb") as raw_img:
        while True:
            try: 
                data = client.recv(prop.BUFF_SIZE)
                if not data:
                    break
                raw_img.write(data)
            except socket.error as error:
                if error.args[0] == errno.EAGAIN or error.args[0] == errno.EWOULDBLOCK:
                    continue
                else:
                    logging.error("Thread error: " +  str(error))
                    sys.exit(1)                    
    logging.debug("Image arrived from client " + str(address[1]))
    client.send("IMG_OK" + os.linesep)

    """ openCv method call at this point """

    ret_img_filename = str(address[1]) + "_ret_img.jpg"
    try:
        with open(prop.TMP_DIR + ret_img_filename, "rb") as ret_img:
            try:
               data = ret_img.read()
               client.send(data)
               logging.debug("Image sent to client")
            except socket.error as error:
                logging.error("Image send error: " + str(error))
    except IOError as error:
        logging.error("IOError: " + str(error))
    
    logging.debug("Client " + str(address[1]) + " closed")
    client.close()
