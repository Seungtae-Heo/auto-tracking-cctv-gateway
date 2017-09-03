import logging
import struct
import threading

from tornado import gen
from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer

logger = logging.getLogger(__name__)


class MobileTCPServer(TCPServer):

    __instance_lock = threading.Lock()
    __instance = None

    @staticmethod
    def instance():
        if not MobileTCPServer.__instance:
            with MobileTCPServer.__instance_lock:
                if not MobileTCPServer.__instance:
                    MobileTCPServer.__instance = MobileTCPServer()
        return MobileTCPServer.__instance

    def __init__(self):
        super(MobileTCPServer, self).__init__()

    @gen.coroutine
    def handle_stream(self, stream, address):
        logger.info('New mobile stream from {}'.format(address))

        camera_id = -1
        while True:
            try:
                packet_size = struct.calcsize('!L')
                packet = yield stream.read_bytes(packet_size)
                packet = struct.unpack('!L', packet)[0]

                # TODO: Subscribe Camera
            except StreamClosedError:
                logger.info('Mobile stream is closed.')
                break

        if not camera_id == -1:
            # TODO: Unsubscribe Camera
            pass
