# Krator Assistant Framework

Krator is a modular AI assistant framework. The project is
structured as a Python package with pluggable modules for presence detection,
voice control, project management and automation. The framework targets
Raspberry Pi and desktop systems.

## Quick start

```bash
pip install -r requirements.txt
python run.py
```

The assistant will listen for commands from the microphone or the terminal and
respond with simple status messages.

### Local task management

`ProjectManager` now stores tasks in a `tasks.json` file. Tasks can be added or
updated via the HTTP API and overdue tasks are reported based on their `due`
date.

### Device bridge

`DeviceBridge` offers a very small in-memory queue for sending commands between
devices. Commands are queued per device and can be fetched by the receiving
side.
