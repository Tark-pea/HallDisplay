# HallDisplay

HallDisplay is a lightweight Python application that displays the current class block based on the time of day, lists important annoucements, displays weather and cafeteria menu. It is designed for use on hallway displays, TVs, Raspberry Pis, or any monitor where students and staff need a quick view of the current schedule or other important notes.

## Features

- 🕒 Automatically detects the current class block
- 📅 Supports different schedules for each weekday
- ⏱ Displays passing periods and time remaining
- 🖥 Full-screen friendly display
- ⚡ Lightweight and easy to run
- 🔧 Easily customizable schedule

## Requirements

- Python 3.10+
- Any required Python packages (see `requirements.txt` if included)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Tark-pea/HallDisplay.git
cd HallDisplay
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running

Start the application by running:

```bash
start_display.sh
```

## Customizing the Schedule

The schedule is stored in the project source and can easily be modified to match your school's timetable.

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

## Typical Uses

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
