import time
import SafetyJournal
import os
import traceback

os.chdir(os.path.dirname(os.path.abspath(__file__)))

today = time.strftime("%Y-%m-%d", time.localtime())
is_update = True
is_success = False
with open('auto.dat', 'r', encoding='utf-8') as f:
    lastday = f.readline()
    if lastday == today:
        is_update = False

if is_update:
    try:
        is_success = SafetyJournal.main()
    except Exception as e:
        with open('log.txt','w',encoding='utf8') as f:
            f.write(traceback.format_exc())

if is_success:
    with open('auto.dat', 'w', encoding='utf8') as f:
        f.write(today)