TheKratorProject
Cybersecurity Intelligence for the Next Era

The Krator Project is an advanced cybersecurity research lab focused on building high-impact tools, intelligent defenses, and experimental technologies for securing the digital world. From threat discovery to AI-powered countermeasures, our mission is to push the boundaries of what’s possible in cyber intelligence and defense.




⚔️ KRATOROPS (Offense Division)
Red teaming, exploitation, and lateral movement tools.

🧷 KRATORSHIELD (Defense Division)
Cyber awareness apps, honeypots, and real-time endpoint defense.

🧬 KRATORLABS (Innovation Lab)
R&D streams: AI-driven threat profiling, zero-day sim sandboxing, and quantum resilience.

💼 KRATORCONSOLE (Web UI / SaaS Portal)
Optional control panel with dashboards, team management, and integrated reporting

🔧 Tech Stack
Languages: Python · Rust · JavaScript

UI Framework: React + Tailwind CSS

Infra & DevOps: GitHub Actions · Docker (optional) · CLI-first design


## Krator GUI

The repository includes a minimal Tkinter-based GUI (`krator_gui.py`) as a placeholder interface for future tools. The GUI features a green-on-black style and buttons for planned components such as GeoLocation, IP/Port, Web Scraping, OSINT, Password Cracking (unimplemented) and Bug Bounty utilities.

## Remote Assistant

The project now includes `assistant.py`, a command-line helper for managing remote Linux hosts over SSH. It uses the open-source Paramiko library and supports running individual commands or entering an interactive shell. Additional helpers provide file transfer utilities, basic project task tracking, optional webcam capture via OpenCV, and an experimental voice-triggered shell activated by saying **"Krator"**.

### Usage

Install dependencies first:

```bash
pip install paramiko
pip install opencv-python speechrecognition pyaudio
```

Run a single command remotely:

```bash
python assistant.py <host> <user> "<command>"
```

Or start an interactive session:

```bash
python assistant.py <host> <user>
```

The assistant will prompt for your SSH password if it isn't provided with `--password`.

Additional subcommands:

- `upload <local> <remote>` – copy a file to the host
- `download <remote> <local>` – fetch a file from the host
- `project add <desc>` – append a task description to `tasks.txt`
- `project list` – show all recorded tasks
- `capture [--file path]` – save a webcam snapshot using OpenCV
- `wake` – listen for the wake word "Krator" before opening a shell

Pentesting capabilities are **not** included.

