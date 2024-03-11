#!/usr/bin/python3
import sys
import datetime
import traceback
import BTCom
import BTDef
from zoneinfo import ZoneInfo

def getnow():
    now = datetime.datetime.now(ZoneInfo('Asia/Tokyo'))
    return f'{now:%Y/%m/%d %H:%M}'

def send_request(cmd):
    try:
        if cmd in BTDef.CMD_MODE.keys():
            btc = BTCom.BTCom(BTDef.BT_ADDR, BTDef.CMD_DEF, BTDef.CNV_DEF)
            msg = btc.set_btmode(cmd)
            print(msg)
        else:
            print(cmd + ' is nodef')
    except Exception as e:
        print(list(traceback.TracebackException.from_exception(e).format())[-1], file=sys.stderr)
    #print('join wait')

if __name__ == '__main__':
    args = sys.argv
    print(getnow() + ' ' + str(args))
    if len(args) < 2:
        print('usage: BTSet.py cmd')
        print(BTDef.CMD_MODE)
        sys.exit(1)
    send_request(args[1])

