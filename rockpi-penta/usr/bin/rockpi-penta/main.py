#!/usr/bin/env python3
import queue
import sys
import threading

import fan
import misc
try:
    import oled
    top_board = True
except Exception as ex:
    top_board = False


q = queue.Queue()
lock = threading.Lock()

action = {
    'none': lambda: 'nothing',
    'slider': lambda: oled.slider(lock),
    'switch': lambda: misc.fan_switch(),
    'reboot': lambda: misc.check_call('reboot'),
    'poweroff': lambda: misc.check_call('poweroff'),
}


def receive_key(q):
    while True:
        func = misc.get_func(q.get())
        action[func]()


def main():
    if sys.argv[-1] == 'on':
        if top_board:
            oled.welcome()
    elif sys.argv[-1] == 'off':
        if top_board:
            oled.goodbye()
        exit(0)


if __name__ == '__main__':
    main()

    if top_board:
        p0 = threading.Thread(target=receive_key, args=(q,))
        p1 = threading.Thread(target=misc.watch_key, args=(q,))
        p2 = threading.Thread(target=oled.auto_slider, args=(lock,))
        p3 = threading.Thread(target=fan.running)

        p0.start()
        p1.start()
        p2.start()
        p3.start()
        p3.join()
    else:
        p3 = threading.Thread(target=fan.running)
        p3.start()
        p3.join()
