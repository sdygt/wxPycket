import datetime
import gettext
import os
import socket
import sys
import threading
from socketserver import ThreadingTCPServer, StreamRequestHandler, DatagramRequestHandler, ThreadingUDPServer

import wx

from layout.out.MyFrame import MyFrame


class MainFrame(MyFrame):
    def __init__(self, *args, **kwds):
        MyFrame.__init__(self, *args, **kwds)
        self.serverThread = None
        self.server = None
        self.clientSocket = None
        self.clientSocketProtocol = None

    def OnAbout(self, event):
        wx.MessageBox('About...', '关于', wx.OK)

    def OnServerToggle(self, event):
        log('debug', "OnServerToggle")
        if os.path.isfile('.enable'):
            self.OnServerStop()
        else:
            self.OnServerStart()

    def OnServerStart(self):
        txtServerPort = self.text_server_port.GetValue()
        if not txtServerPort.isdigit():
            wx.MessageBox('Invalid server port')
            return
        elif int(txtServerPort) <= 1024 or int(txtServerPort) >= 65536:
            wx.MessageBox('Port must in 1024 to 65535')
            return

        radP = self.radio_server_protocol
        txtProtocol = radP.GetItemLabel(radP.GetSelection())
        if txtProtocol == 'TCP':
            try:
                os.close(os.open('.enable', os.O_CREAT))
                self.server = ThreadingTCPServer(('', int(txtServerPort)), self.MainTCPHandler)
                self.serverThread = threading.Thread(target=self.server.serve_forever)
                self.serverThread.daemon = True
                self.serverThread.start()
                log('notice', 'TCP Server started')
            except (Exception) as e:
                wx.MessageBox('Failed Starting Server')
                log('error', e)
            except OSError as e:
                wx.MessageBox(e)
                log('error', e)
        elif txtProtocol == 'UDP':
            try:
                os.close(os.open('.enable', os.O_CREAT))
                self.server = ThreadingUDPServer(('', int(txtServerPort)), self.MainUDPHandler)
                self.serverThread = threading.Thread(target=self.server.serve_forever)
                self.serverThread.daemon = True
                self.serverThread.start()
                log('notice', 'UDP Server started')
            except OSError as e:
                wx.MessageBox(e)
                log('error', e)
            except Exception as e:
                wx.MessageBox('Failed Starting Server')
                log('error', e)

        self.btn_server_toggle.SetLabel('停止')

    def OnServerStop(self):
        log('debug', "OnServerStop")
        os.remove('.enable')
        self.server.shutdown()
        self.server.server_close()
        self.btn_server_toggle.SetLabel('启动')
        log('notice', 'Server stopped.')

    def OnClientToggle(self, event):
        log('debug', 'OnClientToggle')
        if self.clientSocket:
            self.OnClientStop()
        else:
            self.OnClientStart()

    def OnClientStart(self):
        log('debug', 'OnClientStart')
        txtAddress = self.text_client_address.GetValue()
        txtPort = self.text_client_port.GetValue()
        if not self.is_valid_ip(txtAddress):
            wx.MessageBox('Invalid IP Address！')
            return
        if not txtPort.isdigit() or int(txtPort) <= 1024 or int(txtPort) >= 65536:
            wx.MessageBox('Invalid port!')
            return

        PORT = (txtAddress, int(txtPort))

        radP = self.radio_client_protocol
        txtProtocol = radP.GetItemLabel(radP.GetSelection())

        if txtProtocol == 'TCP':
            try:
                self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.clientSocket.connect(PORT)
                log('notice', "TCP Connection " + str(self.clientSocket.getsockname()) + " established")

            except Exception as e:
                log('warning', str(e))
                self.clientSocket = None
                return

        else:  # UDP
            try:
                self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                log('notice', "UDP Socket " + str(self.clientSocket) + " established")
            except Exception as e:
                log('warning', str(e))
                self.clientSocket = None
                return

        self.clientSocketProtocol = txtProtocol
        self.btn_client_toggle.SetLabel('关闭Socket')

    def OnClientStop(self):
        log('debug', 'OnClientStop')
        log('notice', "Closing Connection " + str(self.clientSocket))
        self.clientSocket.close()
        self.clientSocket = None
        self.clientSocketProtocol = None
        self.btn_client_toggle.SetLabel('建立Socket')

    def OnClientSend(self, event):
        msg = self.text_client_input.GetValue().encode()
        print(msg)
        try:
            if self.clientSocketProtocol == 'TCP':
                self.clientSocket.send(msg)
            else:  # UDP
                txtAddress = self.text_client_address.GetValue()
                txtPort = self.text_client_port.GetValue()
                PORT = (txtAddress, int(txtPort))
                self.clientSocket.sendto(msg, PORT)

            self.text_client_input.Clear()
        except Exception as e:
            log('warning', str(e))
            self.OnClientStop()

    def is_valid_ip(self, addr):
        try:
            socket.inet_aton(addr)
            return True
        except socket.error:
            return False

    class MainTCPHandler(StreamRequestHandler):
        def __init__(self, request, client_address, server):
            StreamRequestHandler.__init__(self, request, client_address, server)

        def handle(self):
            log('notice', "New connection from " + str(self.client_address))

            while os.path.isfile('.enable'):
                msg = self.request.recv(8192)
                if not msg:
                    log('notice', ("Disconnected from " + str(self.client_address)))
                    break
                log('info', (str(self.client_address) + " " + str(msg)))

    class MainUDPHandler(DatagramRequestHandler):

        def __init__(self, request, client_address, server):
            DatagramRequestHandler.__init__(self, request, client_address, server)

        def handle(self):
            msg, sock = self.request
            log('info', (str(self.client_address) + " " + str(msg)))


if __name__ == "__main__":
    if os.path.isfile('.enable'):
        os.remove('.enable')
    gettext.install("wxPycket")  # replace with the appropriate catalog name

    wxPycket = wx.App()
    frame = MainFrame(None, wx.ID_ANY, "")


    def log(type, msg, frame=frame):
        label = {'error': '[ERR!]', 'warning': '[WARN]', 'notice': '[NOTI]', 'info': '[INFO]', 'debug': '[DBG ]'}
        print(datetime.datetime.now(), label[type], msg, sep=' ', file=sys.stderr)
        if not type == 'debug':
            frame.text_log.AppendText(str(datetime.datetime.now()) + ' ' + label[type] + ' ' + msg + '\n')
        if type in ['err', 'warning', 'notice']:
            frame.frame_statusbar.SetStatusText(str(msg))


    wxPycket.SetTopWindow(frame)
    frame.Show()
    wxPycket.MainLoop()
