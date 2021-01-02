import sys
import socket
from datetime import datetime
import threading
socket.setdefaulttimeout(1)


def worker(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print("scanning port: " + str(port))
        connection = s.connect_ex((target_ip, port))
        if connection == 0:
            print("Port " + str(port) + " is Open")
        s.close()
    except KeyboardInterrupt:
        print("closing the program.")
        sys.exit()
    except socket.gaierror:
        print("Hostname Couldn't be Resolved, Please Check Your Dns.")
        sys.exit()
    except socket.error:
        print("couldn't do the connection at all, check your internet connection.")
        sys.exit()


# Define our target
if len(sys.argv) == 5:
    target_ip = socket.gethostbyname(sys.argv[1])  # Get ip from hostname
    start_port = sys.argv[2]
    end_port = sys.argv[3]
    workers = sys.argv[4]
    print("-_" * 25)
    print("Scanning Target: " + target_ip + " from Port " + start_port + " to Port " + end_port + " Using " +
          str(workers) + " Workers")
    print("Time Started: " + str(datetime.now()))
    threads = []

    # Loop to Create thread for every port
    for port in range(int(start_port), int(end_port)):
        t = threading.Thread(target=worker, args=(port, ))
        threads.append(t)
    start = 0

    # Loop to divide the threads by the needed workers to create patches for every group of workers
    for i in range(int(len(threads)) // int(workers)):
        for t in threads[start: start+int(workers)]:
            t.start()
        for t in threads[start: start+int(workers)]:
            t.join()
        start = start + int(workers)
else:  # if wrong arguments
    print("Invalid Syntax")
    print("Syntax is: python3 PortScanner.py <hostname or ip> <start port> <end port> <Number of Threads (Workers)>")


