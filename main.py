import curses
from curses import wrapper
import time
import random


menu = ['Start', 'Quit']

# text
text1 = "╭━━━╮╱╱╱╱╱╱╱╱╱╱╭┳━━━━╮"
text2 = "┃╭━╮┃╱╱╱╱╱╱╱╱╱╱┃┃╭╮╭╮┃"
text3 = "┃╰━━┳━━┳━━┳━━┳━╯┣╯┃┃┣┫╱╭┳━━┳━━╮"
text4 = "╰━━╮┃╭╮┃┃━┫┃━┫╭╮┃╱┃┃┃┃╱┃┃╭╮┃╭╮┃"
text5 = "┃╰━╯┃╰╯┃┃━┫┃━┫╰╯┃╱┃┃┃╰━╯┃╰╯┃╰╯┃"
text6 = "╰━━━┫╭━┻━━┻━━┻━━╯╱╰╯╰━╮╭┫╭━┻━━╯"
text7 = "╱╱╱╱┃┃╱╱╱╱╱╱╱╱╱╱╱╱╱╱╭━╯┃┃┃"
text8 = "╱╱╱╱╰╯╱╱╱╱╱╱╱╱╱╱╱╱╱╱╰━━╯╰╯"







def print_menu(stdscr, selected_row_idx):
    stdscr.clear()
    credit = "Made by plugg.#7168. GitHub: plugg1N"

    offset = 6
    h, w = stdscr.getmaxyx()
    stdscr.addstr(1,w//3+offset, text1)
    stdscr.addstr(2,w//3+offset, text2)
    stdscr.addstr(3,w//3+offset, text3)
    stdscr.addstr(4,w//3+offset, text4)
    stdscr.addstr(5,w//3+offset, text5)
    stdscr.addstr(6,w//3+offset, text6)
    stdscr.addstr(7,w//3+offset, text7)
    stdscr.addstr(8,w//3+offset, text8)
    stdscr.addstr(h-1, w-len(credit)-offset+4, credit)

    for idx, row in enumerate(menu):
        x = w//2 - len(row)//2
        y = h//2 - len(menu)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(4))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(4))
        else:
            stdscr.addstr(y, x, row)

    stdscr.refresh()



def show_statistics(stdscr):
    stdscr.clear()


def start_scr(stdscr):
    curses.curs_set(0)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)
    current_row_idx = 0

    print_menu(stdscr, current_row_idx)
    while True:
        key = stdscr.getch()

        stdscr.clear()

        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(menu) - 1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13] and current_row_idx == 0:
            wpm_test(stdscr)
        elif key == curses.KEY_ENTER or key in [10, 13] and current_row_idx == 1:
            quit()
        print_menu(stdscr, current_row_idx)
        stdscr.refresh()




def display_text(stdscr, target, current, wpm=0, cpm=0):
    stdscr.addstr(target)
    stdscr.addstr(2, 0, f"WPM: {wpm}")
    stdscr.addstr(3, 0, f"CPM: {cpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)

        stdscr.addstr(1, i, char, color)
    

def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()



def wpm_test(stdscr):
    target_text = load_text() 
    current_text = []
    wpm = 0
    cpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60) / 5))
        cpm = round(len(current_text) / (time_elapsed / 60))

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm, cpm)
        stdscr.refresh()


        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            time.sleep(2)
            break
            

        try:
            key = stdscr.getkey() 
        except:
            continue

        if ord(key) == 27:
            break
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    start_scr(stdscr)
    
    while True:
        wpm_test(stdscr)
        stdscr.addstr(5, 0, "Press [ENTER] key to continue or [ESC] to go back!")
        key = stdscr.getkey()
        if ord(key) == 27:
            break


wrapper(main)
