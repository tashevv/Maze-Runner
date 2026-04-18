import sys
import os

# Add the local 'lib' folder to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))

import time
import curses

from maze_generator import maze, WIDTH, HEIGHT, WALL, SEED

def format_time(elapsed):
    hours = elapsed // 3600
    minutes = (elapsed % 3600) // 60
    seconds = elapsed % 60

    if hours > 0:
        return f"{hours}h {minutes:02d}m {seconds:02d}s"
    elif minutes > 0:
        return f"{minutes}m {seconds:02d}s"
    else:
        return f"{seconds}s"

def input_f(key):
    if key == ord('q'): # Quit
        curses.endwin()  # cleanly close curses first
        exit()
    elif key == ord('r'): # Restart
        curses.endwin()  # cleanly close curses first
        os.execv(sys.executable, [sys.executable] + sys.argv)
    

def main(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # player color

    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.nodelay(True)
    stdscr.timeout(100)  # refresh every 100ms

    # Start player at a valid empty spot
    player_x, player_y = 1, 1

    start_time = time.time()

    while True:
        stdscr.clear()

        # HEADER
        elapsed = int(time.time() - start_time)
        time_str = format_time(elapsed)

        stdscr.addstr(0, 0, "MAZE RUNNER v1.0", curses.A_BOLD)
        stdscr.addstr(1, 0, f"Time: {time_str} ")
        stdscr.addstr(1, 24, f"Position: ({player_x}, {player_y})")
        
        stdscr.addstr(2, 0, f"Seed: {SEED} ")
        stdscr.addstr(2, 24, f"Size: ({WIDTH}, {HEIGHT})")

        # MAZE
        maze_offset_y = 4

        # Draw the maze
        for y in range(HEIGHT):
            for x in range(WIDTH):
                stdscr.addstr(y + maze_offset_y, x, maze[(x, y)])

        # Draw player
        stdscr.addstr(player_y + maze_offset_y, player_x, chr(9608), curses.color_pair(1))
        # Draw Exit
        stdscr.addstr(HEIGHT - 2 + maze_offset_y, WIDTH - 2, "Exit")

        stdscr.addstr(HEIGHT + 1 + maze_offset_y, 0, "Arrow keys to move, q to quit")

        # FOOTER
        footer_y = HEIGHT + maze_offset_y + 1

        stdscr.addstr(footer_y, 0, "CONTROLS: Arrow Keys = Move | Q = Quit | R = Restart")
        
        stdscr.refresh()
        
        # Calculate new position
        new_x, new_y = player_x, player_y

        # Input logic
        key = stdscr.getch()
        input_f(key)
        if key == curses.KEY_UP:
            new_y -= 1
        elif key == curses.KEY_DOWN:
            new_y += 1
        elif key == curses.KEY_LEFT:
            new_x -= 1
        elif key == curses.KEY_RIGHT:
            new_x += 1

        # Collision check (THIS is the important part)
        if maze.get((new_x, new_y)) != WALL:
            
            # Check if Exit is reached
            if player_x == WIDTH - 2 and player_y == HEIGHT - 2:
                stdscr.addstr(footer_y + 2, 0, "YOU ESCAPED THE MAZE!", curses.A_BOLD)
                
                curses.wrapper(main) # End game logic needs fixing
            # Assign new player position   
            player_x, player_y = new_x, new_y    
        
curses.wrapper(main)
