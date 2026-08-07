# HallDisplay

HallDisplay is a lightweight Python application that displays the current class block based on the time of day, lists important annoucements, displays weather and cafeteria menu. It is designed for use on hallway displays, TVs, Raspberry Pis, or any monitor where students and staff need a quick view of the current schedule or other important notes.

## Features

### 📚 Schedule Display

- Automatically detects the current class block
- Displays the current period or passing period
- Shows the remaining time in each block
- Supports unique schedules for every weekday
- Easily customizable for different schools

### 📢 Announcements

Display custom announcements directly on the screen.

Examples include:

- Welcome messages
- Upcoming events
- School reminders
- Emergency notices
- Club information

Announcements are easily editable in the source code.

### 🌦 Live Weather

Weather information is retrieved directly from the National Weather Service API.

Displays:

- Current temperature
- Current forecast
- Automatically updates throughout the day

No API key is required.

### 🍽 Cafeteria Menu

Displays the current cafeteria menu.

The menu system is separated into its own module, making it easy to adapt to different schools or food providers.

### 🖥 Full Screen Interface

The interface is designed specifically for TVs and hallway displays.

Features include:

- Automatic fullscreen mode
- Large, easy-to-read fonts
- High contrast color scheme
- Decorative panel styling inspired by classical architecture
- Updates automatically every second

---

## Requirements

- Python 3.10+
- tkinter
- beautifulsoup4
- requests

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Tark-pea/HallDisplay.git
cd HallDisplay
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running

Start the display with

```bash
./start_display.sh
```

or

```bash
bash start_display.sh
```

or from ssh
```bash
export DISPLAY=:0
./HallDisplay/start_display.sh &
xtrlock & disown
```

The application launches in fullscreen.

Press **Esc** to exit.

---

## Customizing

### Schedule

The schedule is stored in `block_display_bot.py` and can easily be modified to match your school's timetable.

Example:

```python
SCHEDULE = {
    0: [("8:30", "9:20", "A")],
    1: [("8:30", "9:20", "B")],
    ...
}
```

You can edit:

- Block names
- Start and end times
- Different schedules for each weekday

---

### Announcements

Announcements are located near the top of `hall_display_ui.py`.

Example:

```python
self.add_bullet(
    self.important_frame.body,
    "Welcome Juniors!",
    CREAM
)
```

Simply add or remove announcement lines to update the display.

---

### Weather

Weather data comes from the National Weather Service API.

The location is controlled by the latitude and longitude values:

```python
LAT = 35.727
LON = -81.686
```

Change these coordinates to match your school.

No API key is necessary.

---

### Cafeteria Menu

The menu is managed separately by `menu_board.py`.

Because it is isolated from the UI, you can replace it with another data source without changing the rest of the application.

---

## Typical Uses

- Mini PCs
- School hallway displays
- Classroom smart boards
- Raspberry Pi information screens
- Digital signage
- Administrative displays

## Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest new features
- Submit pull requests

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

Made with ❤️ for schools.
