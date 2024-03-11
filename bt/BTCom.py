import sys
import time
import socket
import binascii
import traceback
import threading
from contextlib import closing

class BTCom(threading.Thread):
    #port
    ECHONET_PORT = 3610
    #timeout
    ECHONET_TIMEOUT = 10

    def __init__(self, host, cmdcfg, cnvdef):
        super(BTCom, self).__init__()
        self.host = host
        self.cmdcfg = cmdcfg
        self.cnvdef = cnvdef

    def run(self):
        res = self.receive_state()
        if res:
            self.printres(res)
        else:
            print('Timeout')

    def printres(self, res):
        print(self.getstrval(res))

    def getstrval(self, res):
        epc, lng, val = res[:2], res[2:4], res[4:]
        if epc in self.cmdcfg.keys():
            cfg = self.cmdcfg[epc]
            return self.tostring(cfg, epc, lng, val)
            #print(epc + '\t' + lng + '\t' + val + '\t' + str(cfg))
        else:
            return 'Unknown EPC:' + epc

    def tostring(self, cfg, epc, lng, val):
        if lng == '00':
            return f'{epc}\tNone'
        elif cfg[0] == 'hex':
            return f'{epc}\t{val}{cfg[1]}\t{cfg[2]}'
        elif cfg[0] == 'dec':
            return f'{epc}\t{int(val, 16)}{cfg[1]}\t{cfg[2]}'
        elif cfg[0] == 'cnv':
            return f'{epc}\t{self.getcnv(epc, val)}{cfg[1]}\t{cfg[2]}'
        else:
            return f'{epc}\t{val}{cfg[1]}\t{cfg[2]}'

    def getcnv(self, epc, val):
        key = epc + ',' + val
        if key in self.cnvdef:
            return f'{val}:{self.cnvdef[key]}'
        else:
            return val

    def receive_state(self):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
            sock.bind(('', self.ECHONET_PORT))
            sock.settimeout(self.ECHONET_TIMEOUT)
            try:
                row, addr = sock.recvfrom(4096)
                hex = str(binascii.hexlify(row), 'utf-8')
                res = hex[24:]
                return res
            except Exception as e:
                print(list(traceback.TracebackException.from_exception(e).format())[-1], file=sys.stderr)
        return None

    def confirm_request(self, epc):
        #                     #   2      2       3       3      1      1      1      1
        format_echonet_lite = ['EHD', 'TID', 'SEOJ', 'DEOJ', 'ESV', 'OPC', 'EPC', 'PDC', 'EDT']
        data_format = {
            format_echonet_lite[0]: '1081', #EHD 固定
            format_echonet_lite[1]: '0000', #TID
            format_echonet_lite[2]: '05FF01', #SEOJ 送信元PC
            format_echonet_lite[3]: '027D01', #DEOJ 送信先蓄電池
            format_echonet_lite[4]: '62', #ESV 60:要求,61:要求応答,62:取得
            format_echonet_lite[5]: '01', #OPC 取得コマンド数
            format_echonet_lite[6]: epc, #EPC コマンド
            format_echonet_lite[7]: '00', #PDC 制御コマンド数
            format_echonet_lite[8]: '' #EDT none
        }
        self.send_request(data_format, format_echonet_lite)

    def set_btmode(self, cmd):
        #                     #   2      2       3       3      1      1      1      1
        format_echonet_lite = ['EHD', 'TID', 'SEOJ', 'DEOJ', 'ESV', 'OPC', 'EPC', 'PDC', 'EDT']
        data_format = {
            format_echonet_lite[0]: '1081', #EHD 固定
            format_echonet_lite[1]: '0000', #TID
            format_echonet_lite[2]: '05FF01', #SEOJ 送信元PC
            format_echonet_lite[3]: '027D01', #DEOJ 送信先蓄電池
            format_echonet_lite[4]: '61', #ESV 60:要求,61:要求応答,62:取得
            format_echonet_lite[5]: '01', #OPC 取得コマンド数
            format_echonet_lite[6]: 'DA', #EPC コマンド 運転モード設定
            format_echonet_lite[7]: '01', #PDC 制御コマンド数
            format_echonet_lite[8]: cmd #EDT 42:充電,43:放電,44:待機
        }
        return self.send_request(data_format, format_echonet_lite)

    def send_request(self, data, format):
        frame = ''
        for key in format:
            frame += data[key]
        msg = binascii.unhexlify(frame)
        with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
            sock.sendto(msg, (self.host, self.ECHONET_PORT))
        return frame

