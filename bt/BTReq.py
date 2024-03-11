#!/usr/bin/python3
import sys
import time
import traceback
import BTCom
import BTDef

def send_request(epc):
    try:
        if epc in BTDef.CMD_DEF.keys():
            btc = BTCom.BTCom(BTDef.BT_ADDR, BTDef.CMD_DEF, BTDef.CNV_DEF)
            btc.confirm_request(epc)
        else:
            print(epc + ' is nodef')
    except Exception as e:
        print(list(traceback.TracebackException.from_exception(e).format())[-1], file=sys.stderr)
    #print('join wait')

if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        print('usage: BTReq.py epc')
        print(BTDef.getusage())
        sys.exit(1)
    send_request(args[1])

