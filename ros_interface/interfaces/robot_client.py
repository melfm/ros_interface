import socket
import time
from IPython import embed

class RobotCommunicator():
    def __init__(self, robot_ip="127.0.0.1", port=9101):
        self.robot_ip = robot_ip
        self.port = port
        self.connected = False
        self.connect()

    def connect(self):
        while not self.connected:
            print("attempting to connect with robot at {}".format(self.robot_ip))
            self.tcp_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            # connect to computer
            self.tcp_socket.connect((self.robot_ip, self.port))
            print('connected')
            self.connected = True
            if not self.connected:
                time.sleep(1)

    def send(self, fn, cmd):
        data = '<|{}**{}|>'.format(fn,cmd)
        print('sending', data)
        self.tcp_socket.send(data.encode())
        ret_msg = self.tcp_socket.recv(1024).decode()
        print('rx', ret_msg)
        return ret_msg

    def disconnect(self):
        self.send('END', '')
        print('disconnected from {}'.format(self.robot_ip))
        self.tcp_socket.close()
        self.connected = False

def send_step(rc,n=3,step_cmd=[0,0,5,0,0,0,0]):
    for i in range(n):
        rc.send("STEP", step_cmd)
        time.sleep(1/100.)
 
if __name__ == '__main__':

    # works when client/server are both on local machine (capilano) 127.0.0.1
    # success test case is:
    # >> python robot_server.py # on capilano
    # >> python robot_client.py 127.0.0.1 # on capilano
    # fails when client/server are on different machines on lab subnet
    # failure test case is:
    # >> python robot_server.py # on capilano
    # >> python robot_client.py 132.206.73.29 # on rhys
    import sys
    #server_ip = sys.argv[1]
    #print('attempting to message server on %s - ensure it is running'%server_ip)
    #rc = RobotCommunicator(robot_ip=server_ip)
    #rc.send('RESET', 'True')
    try:
        rc = RobotCommunicator()
    except KeyboardInterrupt:
        pass
    embed()
    rc.disconnect()
