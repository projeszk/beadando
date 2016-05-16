import logging
import socket
import sys

from properties import property as prop
from threads.ImageHandlerThread import ImageHandlerThread

class SocketServer:
    """
    Multithreaded socket server.
    """
    __SERVER_SOCKET = None
    __HOST = None
    __PORT = None
    __TIMEOUT = None
    __RUNNING = True

    def __init__(self, host=prop.HOST, port=prop.PORT, timeout = prop.TIMEOUT):
        """
        Construct new SocketServer object.

        :param host: Host name
        :type host: str
        :param port: Port number
        :type port: number
        :param timeout: Timeout second value
        :type port: number

        :return:
        """
        self.__HOST = host
        self.__PORT = port
        self.__TIMEOUT = timeout
        logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")
        try:
            self.__SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__SERVER_SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.__SERVER_SOCKET.settimeout(self.__TIMEOUT)
        except socket.error as error:
            logging.error("Error while create the server socket " + str(error))
            sys.exit(1)

    def __del__(self):
        """
        Free ServerSocket object.
        
        :return:
        """
        self.__SERVER_SOCKET.close()

    def run(self):
        """
        Server run method.
        Infinite multithreaded server loop.
        
        :return:
        """
        server = self.__SERVER_SOCKET
        try:
            server.bind((self.getHost(), self.getPort()))
            server.listen(5)
        except socket.error as error:
            logging.error("Server error: " +  str(error))
            return
        try:
            logging.info("Server running at port " + str(self.getPort()) + " and host " + str(self.getHost()))
            while self.isRunning():
                client, address =  server.accept()
                logging.debug("Client connected: " + str(address))
                try:
                    ImageHandlerThread(client, address).start()
                except socket.error as error:
                    logging.error("Server thread error: " +  str(error))
                    client.close()
                    return
        except socket.timeout or KeyboardInterrupt as error:
            logging.debug("Server stop because " + str(error))
            self.stop()
            server.close()
            return
        logging.info("Server stop")

    def start(self):
        self.__setRunning(True)

    def stop(self):
        self.__setRunning(False)

    def isRunning(self):
        return self.__RUNNING

    def __setRunning(self, running):
        self.__RUNNING = running

    def getHost(self):
        """
        Return server host name.
        
        :return: host name
        :rtype: str
        """
        return self.__HOST

    def getPort(self):
        """
        Return server port number.
        
        :return: port number
        :rtype: number
        """
        return self.__PORT
