import os
import sys
import socket
import thread
import time
import logging
import errno
from properties import property as prop

# Simple multithreading socket server class
class SocketServer:
    __SERVER_SOCKET = None
    __HOST = prop.HOST
    __PORT = prop.PORT
    __TIMEOUT = 10

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")
        try:
            self.__SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__SERVER_SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.__SERVER_SOCKET.settimeout(self.__TIMEOUT)
        except socket.error as error:
            logging.error("Error while create the server socket " + str(error))
            sys.exit(1)

    def __del__(self):
        self.__SERVER_SOCKET.close()

    def run(self):
        server = self.__SERVER_SOCKET
        try:
            server.bind((self.host(), self.port()))
            server.listen(5)
        except socket.error as error:
            logging.error("Server error: " +  str(error))
            sys.exit(1)
        try:
            logging.debug("Server running at port " + str(self.port()))
            print("Server running at port " + str(self.port()))
            while True:
                client, address =  server.accept()
                logging.debug("Client connected: " + str(address))
                try:
                    thread.start_new_thread(self.client_handler, (client, address))
                except socket.error as error:
                    logging.error("Server thread error: " +  str(error))
                    sys.exit()
        except socket.timeout as error:
            logging.debug("Server stop because " + str(error))
            print("Server stop because " + str(error))
            server.close()
            sys.exit(1)

    def host(self):
        return self.__HOST

    def port(self):
        return self.__PORT

    def client_handler(self, client, address):
        client.send("Connected to the server. Send a picture of the analysis." + os.linesep)
        with open(prop.IMG_DIR_PATH + str(address[1]) + "_img.jpg", "wb") as img:
            while True:
                try: 
                    data = client.recv(prop.BUFF_SIZE)
                    reply = data
                    if not data: break
                    img.write(data)
                    client.send(reply)
                    print "sent: " + reply
                except socket.error as error:
                    if error.args[0] == errno.EAGAIN or error.args[0] == errno.EWOULDBLOCK:
                        time.sleep(0.1)
                        continue
                    else:
                        logging.error("Thread error: " +  str(error))
                        sys.exit(1)
        img.close()
        logging.debug("Client close")    
        client.close()
