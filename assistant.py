import argparse
import getpass
import os

import paramiko

# Optional dependencies. Import lazily where used.


def connect(host, username, password):
    """Establish an SSH connection and return the client."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, username=username, password=password)
    return ssh


def run_command(ssh, command):
    """Execute a command over an existing SSH connection."""
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode()
    error = stderr.read().decode()
    return output, error


def interactive_shell(ssh):
    """Interactive shell that prefixes the prompt with the wake word."""
    print("Type 'exit' to quit.")
    while True:
        cmd = input("Krator$ ")
        if cmd.strip().lower() == "exit":
            break
        out, err = run_command(ssh, cmd)
        if out:
            print(out)
        if err:
            print(err)


def upload_file(ssh, local_path, remote_path):
    sftp = ssh.open_sftp()
    sftp.put(local_path, remote_path)
    sftp.close()


def download_file(ssh, remote_path, local_path):
    sftp = ssh.open_sftp()
    sftp.get(remote_path, local_path)
    sftp.close()


def capture_image(filename="capture.jpg"):
    """Capture an image using OpenCV."""
    import cv2  # lazy import

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(filename, frame)
        print(f"Saved image to {filename}")
    else:
        print("Failed to capture image")
    cap.release()


def wait_for_wake_word(word="krator"):
    """Listen for the given wake word using the microphone."""
    try:
        import speech_recognition as sr  # lazy import
    except ImportError:
        print("speech_recognition module not installed")
        return False
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    print(f"Say '{word}' to begin")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        phrase = recognizer.recognize_google(audio).lower()
        return word.lower() in phrase
    except sr.UnknownValueError:
        return False


def add_task(description, tasks_file="tasks.txt"):
    with open(tasks_file, "a", encoding="utf-8") as f:
        f.write(f"- {description}\n")


def list_tasks(tasks_file="tasks.txt"):
    if not os.path.exists(tasks_file):
        print("No tasks found")
        return
    with open(tasks_file, encoding="utf-8") as f:
        print(f.read())


def main():
    parser = argparse.ArgumentParser(description="Remote Assistant over SSH")
    parser.add_argument("host", help="Target host")
    parser.add_argument("username", help="SSH username")
    parser.add_argument("--password", help="SSH password")

    sub = parser.add_subparsers(dest="action", required=True)
    run_p = sub.add_parser("run", help="Run a single command")
    run_p.add_argument("cmd")

    sub.add_parser("shell", help="Interactive shell")

    up_p = sub.add_parser("upload", help="Upload local file")
    up_p.add_argument("local")
    up_p.add_argument("remote")

    down_p = sub.add_parser("download", help="Download remote file")
    down_p.add_argument("remote")
    down_p.add_argument("local")

    project_p = sub.add_parser("project", help="Manage project tasks")
    project_p.add_argument("op", choices=["add", "list"])
    project_p.add_argument("description", nargs="?")

    capture_p = sub.add_parser("capture", help="Capture an image using OpenCV")
    capture_p.add_argument("--file", default="capture.jpg")

    sub.add_parser("wake", help="Wait for wake word before opening shell")

    args = parser.parse_args()

    password = args.password or getpass.getpass(prompt="SSH password: ")

    ssh = connect(args.host, args.username, password)

    if args.action == "run":
        out, err = run_command(ssh, args.cmd)
        if out:
            print(out)
        if err:
            print(err)
    elif args.action == "shell":
        interactive_shell(ssh)
    elif args.action == "upload":
        upload_file(ssh, args.local, args.remote)
    elif args.action == "download":
        download_file(ssh, args.remote, args.local)
    elif args.action == "project":
        if args.op == "add" and args.description:
            add_task(args.description)
        elif args.op == "list":
            list_tasks()
    elif args.action == "capture":
        capture_image(args.file)
    elif args.action == "wake":
        if wait_for_wake_word("krator"):
            interactive_shell(ssh)
        else:
            print("Wake word not detected")

    ssh.close()


if __name__ == "__main__":
    main()
