
# 蓄電池IPアドレス
BT_ADDR = '192.168.0.xx'

# 蓄電池プロファイル
CNV_DEF = {
    '80,30':'ON',  #動作状態,ON
    '80,31':'OFF', #動作状態,OFF
    '88,41':'異常発生有', #異常発生状態,異常
    '88,42':'異常発生無', #異常発生状態,正常
    'da,40':'その他', #運転モード 
    'da,41':'急速充電', #運転モード 
    'da,42':'充電', #運転モード 
    'da,43':'放電', #運転モード 
    'da,44':'待機', #運転モード 
    'da,45':'テスト', #運転モード 
    'da,46':'自動', #運転モード 
    'da,48':'再起動', #運転モード 
    'da,49':'実効容量再計算処理', #運転モード 
    'cf,40':'その他', #運転動作状態 
    'cf,41':'急速充電', #運転動作状態 
    'cf,42':'充電', #運転動作状態 
    'cf,43':'放電', #運転動作状態 
    'cf,44':'待機', #運転動作状態 
    'cf,45':'テスト', #運転動作状態 
    'cf,46':'自動', #運転動作状態 
    'cf,48':'再起動', #運転動作状態 
    'cf,49':'実効容量再計算処理', #運転動作状態 
    'db,00':'系統連系（逆潮流可）', #系統連系状態
    'db,01':'独立', #系統連系状態
    'db,02':'系統連系（逆潮流不可）', #系統連系状態
}

CMD_DEF = {
    '80':('cnv', '', '動作状態'),
    '81':('hex', '', '設置場所'),
    '82':('hex', '', '規格Version情報'),
    '83':('hex', '', '識別番号'),
    '88':('cnv', '', '異常発生状態'),
    '8a':('hex', '', 'メーカーコード'),
    'a0':('dec', ' Wh', 'AC実効容量(充電)'),
    'a1':('dec', ' Wh', 'AC実効容量(放電)'),
    'a2':('dec', ' Wh', 'AC充電可能容量'),
    'a3':('dec', ' Wh', 'AC放電可能容量'),
    'a4':('dec', ' Wh', 'AC充電可能量'),
    'a5':('dec', ' Wh', 'AC放電可能量'),
    'a8':('dec', ' Wh', 'AC積算充電電力量計測値'),
    'a9':('dec', ' Wh', 'AC積算放電電力量計測値'),
    'aa':('hex', '', 'AC充電量'),
    'ab':('hex', '', 'AC放電量'),
    'cf':('cnv', '', '運転動作状態'),
    'd1':('hex', '', '定格容量'),
    'd2':('hex', '', '定格電圧'),
    'da':('cnv', '', '運転モード'),
    'db':('cnv', '', '系統連系状態'),
    'e2':('dec', ' Wh', '蓄電残量'),
    'e3':('hex', '', '蓄電残量'),
    'e4':('dec', '%', '蓄電残量'),
    'e6':('hex', '', '蓄電池タイプ'),
}

CMD_MODE = {
    '42':'充電', #運転モード
    '43':'放電', #運転モード
    '44':'待機', #運転モード
}

STDSEL = (
    'cf',  #運転動作状態
    'da',  #運転モード
    'a4',  #AC充電可能量
    'e2',  #蓄電残量
    'e4',  #蓄電残量
)

def getusage():
    usage = str(CMD_DEF).replace('), ', ')\n')
    return usage.replace('{', '').replace('}', '')

