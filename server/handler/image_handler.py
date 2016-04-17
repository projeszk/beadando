import os
import sys
import socket
import time
import logging
import errno
from properties import property as prop

def run(client, address):
    """
    Callable method.
    Handle image receive from client.
        
    :return:
    """
    client.send("Connected to the server. Send a picture of the analysis." + os.linesep)
    filename = str(address[1]) + "_img.jpg"
    with open(prop.TMP_DIR + filename, "wb") as img:
        logging.debug(filename + " created")
        while True:
            try: 
                data = client.recv(prop.BUFF_SIZE)
                if not data: break
                img.write(data)
                client.send("Package arrived from client " + str(address[1]) + os.linesep)
            except socket.error as error:
                if error.args[0] == errno.EAGAIN or error.args[0] == errno.EWOULDBLOCK:
                    time.sleep(0.1)
                    continue
                else:
                    logging.error("Thread error: " +  str(error))
                    sys.exit(1)
    img.close()
    logging.debug("Client " + str(address[1]) + " close")    
    client.close()
