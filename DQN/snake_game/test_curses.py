import curses

curses.initscr()
win = curses.newwin(20, 20, 0, 0)
curses.curs_set(0)
win.nodelay(1)
win.timeout(100)
# win.keypad( 1 )
win.clear()
win.border(1)
win.addstr(0, 1, "Hello World!")
win.getch()


win2 = curses.newwin(20, 20, 30, 30)
curses.curs_set(0)
win2.nodelay(1)
win2.timeout(100)
# win.keypad( 1 )
win2.clear()
win2.border(1)
win2.addstr(0, 1, "Hello World!")
win2.getch()


