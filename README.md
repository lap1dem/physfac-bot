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
since the bot is not able to send files larger than 50 MB at the default.

## Features

### Schedule
`/schedule` command provides access to lessons timetable in .jpg format provided by deanery.
For now, a new feature is under developing - `/schedule+`, which data will be stored in SQL table
which in turn will allow new possibilities, such as search for a free auditorium, subscription
for daily schedule, etc.

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
`/qmminka` and `/edminka` commands are tests for nowledge of formulas on choosed
object (Quantum Mechanics and Electrodynamics respectively). For now the test on
AGVA is under development.

### Sport and clinic schedules
`/ttsport` and `/ttclinic` commands provide access to schedule of sports complex and
student's clinic respectively.
