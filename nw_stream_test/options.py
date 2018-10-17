import getopt
import socket
import sys



class Options:
    verbose = False
    refresh = 1
    port = 8192
    protocol = socket.SOCK_STREAM
    hosts = []
    minimum_size = 128
    maximum_size = 8192
    rate = 1
    display_rate = 3

    def __init__(self):
        try:
            opts, self.hosts = getopt.getopt(
                sys.argv[1:],
                "h?vur:p:m:x:n:",
                [
                    "help", "verbose",
                    "udp", "refresh=", "port=",
                    "minimum-size=", "maximum-size=", "messages-per-second="
                ]
            )
        except getopt.GetoptError:
            self.usage()
            sys.exit(2)

        for opt, arg in opts:
            if opt in ('-?', '-h', '--help'):
                self.usage()
                sys.exit(0)
            elif opt in ('-v', '--verbose'):
                self.verbose = True
            elif opt in ('-r', '--refresh'):
                self.refresh = int(arg)
            elif opt in ('-p', '--port'):
                self.port = int(arg)
                if self.port < 1 or self.port > 65535:
                    self.usage("invalid port: %d" % self.port)
                    sys.exit(2)
            elif opt in ('-u', '--udp'):
                self.protocol = socket.SOCK_DGRAM
            elif opt in ('-m', '--minimum-size'):
                self.minimum_size = int(arg)
            elif opt in ('-x', '--maximum-size'):
                self.maximum_size = int(arg)
            elif opt in ('-n', '--messages-per-second'):
                self.rate = int(arg)

    def usage(self, message=None):
        if message:
            print message
        print """Usage:
    %s [options] [hosts_to_send_data]
Where:
    --help - display this message
    --verbose - display more noisey information
    --refresh %d - how many seconds to delay before refreshing the screen
    --port %d - the port to connect to
    --udp - connect using UDP (instead of TCP)
    --minimum-size %d - the smallest message size to transmit
    --maximum-size %d - the largest message size to transmit
    --messages-per-second %d - the rate at which to send messages""" % \
            (
                sys.argv[0], self.refresh, self.port
            )
