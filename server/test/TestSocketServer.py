import unittest
import socket
from Server import SocketServer
from properties import property as prop

class TestSocketServer(unittest.TestCase):
    """
    SocketServer unittest class.
    """

    def __init__(self, *args, **kwargs):
        """
        Crating a server object whit default host and port and set timeout 0.1 second.

        :param args:
        :param kwargs:
        """
        super(TestSocketServer, self).__init__(*args, **kwargs)
        self.server = SocketServer(timeout=0.1)

    def testHost(self):
        """
        Test host string.

        :return:
        """
        self.assertEqual(self.server.getHost(), prop.HOST)

    def testPort(self):
        """
        Test port number.

        :return:
        """
        self.assertEqual(self.server.getPort(), prop.PORT)

    def testRunServer(self):
        """
        Test server run method and timeout.

        :return:
        """
        try:
            self.server.run()
        except socket.error as error:
            self.assertTrue(False, str(error))
        self.assertFalse(self.server.isRunning())


if __name__ == "__main__":
    unittest.main()