# Teams-Meeting-Auto-Join
This Python application, built with Tkinter and Selenium, provides a graphical user interface (GUI) to automate joining Microsoft Teams meetings at scheduled times. Users can specify a Teams meeting link, select a date and time for the meeting, and the application will automatically join the meeting on their behalf.

## Features

- **GUI Interface**: User-friendly interface to input Teams link, date, and time.
- **Automatic Meeting Join**: Automatically opens Chrome, joins the Teams meeting, and manages microphone settings.
- **Background Scheduling**: Continuous background thread to monitor and join scheduled meetings without manual intervention.

## Requirements

- Chromium Driver
- Chrome version must be compatible with chrome Driver
- Python 3.x
- Install dependencies:
  ```bash
  pip install tkcalendar schedule selenium

## How does it work?
- It launches the Teams link that the user will input and will click the necessary buttons to join the meeting.
- It also automatically mutes your mic before joining.
