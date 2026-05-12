#!/usr/bin/env python3
"""
monitor_res.py — semplice monitor CPU/RAM per terminale (Parrot/Debian)
Uso: ./monitor_res.py
Interrompi con q o Ctrl-C.
"""
import time
import psutil
import curses
from datetime import datetime

REFRESH = 1.0  # secondi

def format_bytes(n):
    for unit in ['B','KB','MB','GB','TB']:
        if n < 1024.0:
            return f"{n:5.1f}{unit}"
        n /= 1024.0
    return f"{n:.1f}PB"

def draw(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    maxy, maxx = stdscr.getmaxyx()

    while True:
        stdscr.erase()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cpu_perc = psutil.cpu_percent(interval=None)
        cpu_per_cpu = psutil.cpu_percent(interval=None, percpu=True)
        vm = psutil.virtual_memory()
        swap = psutil.swap_memory()
        procs = len(psutil.pids())

        # Header
        stdscr.addstr(0, 0, f"3PMonitor — {now}  (q to exit)")
        stdscr.hline(1, 0, '-', maxx)

        # CPU overall
        stdscr.addstr(2, 0, f"CPU: {cpu_perc:5.1f}%")
        bar_len = maxx - 20

        # Per-CPU
        stdscr.addstr(4, 0, "Per-core:")
        for i, p in enumerate(cpu_per_cpu):
            line = 5 + i
            if line >= maxy - 6:
                break
            used = int((p/100.0) * bar_len)
            stdscr.addstr(line, 0, f"CPU{i:02d}: {p:5.1f}% ")

        # Memoria
        mem_line = 5 + len(cpu_per_cpu) + 1
        if mem_line < maxy - 5:
            stdscr.addstr(mem_line, 0, f"RAM: {vm.percent:5.1f}%  {format_bytes(vm.used)}  /{format_bytes(vm.total)}")

        # Swap
        swap_line = mem_line + 2
        if swap_line < maxy - 4:
            stdscr.addstr(swap_line, 0, f"Swap: {swap.percent:5.1f}%  {format_bytes(swap.used)}  /{format_bytes(swap.total)}")

        # Processes
        proc_line = swap_line + 2
        if proc_line < maxy - 2:
            stdscr.addstr(proc_line, 0, f"Processi totali: {procs}")

        stdscr.refresh()

        # handle input
        try:
            ch = stdscr.getch()
            if ch in (ord('q'), ord('Q')):
                break
        except Exception:
            pass

        time.sleep(REFRESH)

def main():
    try:
        curses.wrapper(draw)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
