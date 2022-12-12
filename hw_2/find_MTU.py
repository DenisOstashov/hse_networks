import http.client as httplib
import socket
import subprocess
import sys

def main():
    if len(sys.argv) != 2:
        raise TypeError('1 argument required ({} given)'.format(len(sys.argv) - 1))
    host = sys.argv[1]
    try:
        socket.getaddrinfo(host, None)
    except socket.gaierror:
        raise TypeError('Unknown host {}'.format(host))
    
    try:
        conn = httplib.HTTPConnection(host)
        conn.request("HEAD", "/")
    except Exception:
        print("Host {} is not reachable".format(host))

    left = 1
    right = 10000
    while left + 1 < right:
        median = (left + right) // 2
        print("Try MTU = {}".format(median))
        try:
            result = subprocess.run(['ping', host, '-c', '1', '-s', str(median), '-M', 'do'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            raise Exception("Host {} is not reachable")
        if result.returncode == 0:
            left = median
        else:
            right = median
    print("Found MTU = {}(or {} if we include IP(20 bytes) and ICMP(8 bytes) headers)".format(left, left + 28))


if __name__ == "__main__":
    main()