import curses
from curses import wrapper
from curses.textpad import rectangle
import calendar
import datetime


def main(screen):
    screen = curses.initscr()
    screen.keypad(True)

    # Set variables and create the calendar

    curTime = datetime.datetime.now()
    keyPress = ""
    cursorPosition = [-1, -1, -1]
    currentDay = 0
    cal = calendar.Calendar(0)
    calYear = curTime.year
    calMonth = ["January", "February", "March", "April", "May",
                "June", "July", "August", "September", "October",
                "November", "December"]
    daysOfWeek = "Mo Tu We Th Fr Sa Su"

    while keyPress != "q" and keyPress != "Q":
        if keyPress == "KEY_RIGHT" and cursorPosition[0] == -1:
            calYear += 1
        if keyPress == "KEY_RIGHT" and cursorPosition[0] >= 0 and cursorPosition[2] < 6:
            cursorPosition[2] += 1

        if keyPress == "KEY_LEFT" and cursorPosition[0] == -1:
            calYear -= 1
        if keyPress == "KEY_LEFT" and cursorPosition[0] >= 0 and cursorPosition[2] > 0:
            cursorPosition[2] -= 1

        if keyPress == "KEY_DOWN" and cursorPosition[0] >= 0 and cursorPosition[1] < 5:
            cursorPosition[1] += 1
        if keyPress == "KEY_DOWN" and cursorPosition[0] == -1:
            cursorPosition = [0, 0, 0]

        if keyPress == "KEY_UP" and cursorPosition[0] > -1 and cursorPosition[1] == 0:
            cursorPosition = [-1, -1, -1]
        if keyPress == "KEY_UP" and cursorPosition[0] > -1 and cursorPosition[1] > 0:
            cursorPosition[1] -= 1
        if keyPress == "]" and cursorPosition[0] > -1 and cursorPosition[0] == 11:
            calYear += 1
            cursorPosition = [0, 0, 0]
        if keyPress == "]" and cursorPosition[0] > -1 and cursorPosition[0] < 11:
            cursorPosition[0] += 1
            cursorPosition[2] = 0
        if keyPress == "[" and cursorPosition[0] > -1 and cursorPosition[0] == 0:
            calYear -= 1
            cursorPosition = [11, 0, 0]
        if keyPress == "[" and cursorPosition[0] > -1 and cursorPosition[0] > 0:
            cursorPosition[0] -= 1
            cursorPosition[2] = 0

        screen.clear()

        uY = 4
        uX = 1
        counter = 1

        year = cal.yeardayscalendar(calYear, 12)


        # Programatically print the month, days of week, and divider
        for i in range(0, len(calMonth)):
            weeks = cal.monthdayscalendar(calYear, i + 1)
            monthLength = len(calMonth[i])
            screen.insstr(uY, uX, "{:^21s}".format(calMonth[i]))
            screen.insstr(uY + 1, uX, "{:^21s}".format(daysOfWeek))
            screen.insstr(uY + 2, uX, "{:~>21s}".format(""))
            # We need to convert the week to a string
            for j in range(0, len(weeks)):
                for k in range(0, len(weeks[j])):
                    if weeks[j][k] != 0 and ( cursorPosition[0] == i and cursorPosition[1] == j and cursorPosition[2] == k):
                        screen.insstr(uY+3+j, uX + (k * 3), " {:0>2}".format(str(weeks[j][k])), curses.A_REVERSE)
                    elif weeks[j][k] != 0 and ( cursorPosition[0] != i or cursorPosition[1] != j or cursorPosition[2] != k ):
                        screen.insstr(uY+3+j, uX + (k * 3), " {:0>2}".format(str(weeks[j][k])))
                    else:
                        screen.insstr(uY+3+j, uX, " {:2}".format("  "))
            uX += 24
            if counter == 4:
                uX = 1
                uY += 11
                counter = 1
            else:
                counter += 1


        # Draw Rectangles with 2 lines for the header, 6 lines for the body, 20 spaces wide programaticallY
        ## Reset the positioning variables
        uY = 3
        uX = 0
        lY = 14
        lX = 23

        for i in range(0, 3):  # Rows
            for j in range(0, 4):  # Columns. 4 rows of 3
                rectangle(screen, uY, uX, lY, lX)
                # Increment x to draw the next column
                uX += 24
                lX += 24
            # Increment y to drow on the next row
            uY += 11
            uX = 0
            lY += 11
            lX = 23

        # Draw the Rectangle and Text for the Year Selector
        rectangle(screen, 0, 0, 2, 95)
        screen.addstr(1, 1, "{:^94s}".format("<    " + str(calYear) + "    >"))

        if cursorPosition[0] != -1:
            screen.addstr(39, 0, "  Calendar Date: {} {}, {}".format(calMonth[cursorPosition[0]], currentDay, calYear))
        screen.addstr(40, 0, "Curser Position: {} {} {}".format(cursorPosition[0], cursorPosition[1], cursorPosition[2]))

        # Calendar draw is done, refresh, get a key press, and get out
        screen.refresh()
        keyPress = screen.getkey()

wrapper(main)
