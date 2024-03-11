#!/usr/bin/python3
import sys
import time
import traceback
import BTCom
import BTDef

def request_response(epc):
    try:
        th1 = BTCom.BTCom(BTDef.BT_ADDR, BTDef.CMD_DEF, BTDef.CNV_DEF);
        th1.start()
        th1.confirm_request(epc)
        th1.join(timeout=th1.ECHONET_TIMEOUT)
    except Exception as e:
        print(list(traceback.TracebackException.from_exception(e).format())[-1], file=sys.stderr)
    #print('join wait')

if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        for key in BTDef.STDSEL:
            request_response(key)
        exit(0)

    cmd = args[1]
    if cmd == 'all':
        for key, val in BTDef.CMD_DEF.items():
            request_response(key)
    elif cmd in BTDef.CMD_DEF.keys():
        request_response(cmd)
    else:
        print(BTDef.getusage())

