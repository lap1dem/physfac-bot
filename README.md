# physfac-bot

An official Telegram chat bot of Faculty of Physics of Taras Shevchenko National
University of Kyiv. This was created to gather and provide different kinds of
information about study, such as schedule, teachers' emails, books, etc.
Bot is avaiable [here](http://t.me/physfac_bot).

## Overview

1. Bot is written in Python using [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) library.
2. For storing data PSQL server and [psycopg2](http://initd.org/psycopg/) package are using.
3. For navigating the functions standard package `shelve` is used.
4. All `/library` files are stored in the developer's dialogue and are accessed by file ID
since the bot is not able to send files larger than 50 MB by default.

## Features

### Schedule
`/schedule` command provides access to lessons timetable in .jpg format provided by deanery.

### Textschedule
`/textschedule` command provides additional features to classic `/schedule` command.
The special algorithm was written to read the Excel document prepared by deanery, and
with such, all data about schedule were stored in PSQL database. This allows implement
such features as search for empty auditorium, sending daily schedule, getting work
schedule of specific teacher, etc. This feature is under development but it has already
been partially implemented.


### Emails
`/emails` provides access to the database of most teachers' emails.

### Library
`/library` is an electronic archive of textbooks, handbooks and other materials recommended
by teachers.

### Exams
`/exams` command provides access to exams timetable in .pdf format provided by deanery.

### Nord
`/nord` command provides information about alternating lessons.

### Minka
`/qmminka` and `/edminka` commands are tests for knowledge of formulas on a chosen
object (Quantum Mechanics and Electrodynamics respectively). For now the test on
AGVA is under development.

### Sport and clinic schedules
`/ttsport` and `/ttclinic` commands provide access to schedule of sports complex and
student's clinic respectively.

### Bonus features (hidden from public)
`/civ` command was developed to improve playing experience in computer game Civilization V.
It allows to shuffle the list of available civilizations in chosen number for chosen players.
Works in 2 regimes: random and balanced.
`Balanced` shuffle is based on a "tier list" with point grades for each civ.
