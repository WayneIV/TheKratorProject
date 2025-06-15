import argparse
import getpass
import paramiko


def run_command(host, username, password, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode()
    error = stderr.read().decode()
    ssh.close()
    return output, error


def interactive_shell(host, username, password):
    print(f"Connected to {host} as {username}. Type 'exit' to quit.")
    while True:
        cmd = input("$ ")
        if cmd.strip().lower() == "exit":
            break
        out, err = run_command(host, username, password, cmd)
        if out:
            print(out)
        if err:
            print(err)


def main():
    parser = argparse.ArgumentParser(description="Remote Assistant over SSH")
    parser.add_argument("host", help="Target host")
    parser.add_argument("username", help="SSH username")
    parser.add_argument("command", nargs="?", help="Command to run remotely")
    parser.add_argument("--password", help="SSH password")
    args = parser.parse_args()

    password = args.password or getpass.getpass(prompt="SSH password: ")

    if args.command:
        out, err = run_command(args.host, args.username, password, args.command)
        if out:
            print(out)
        if err:
            print(err)
    else:
        interactive_shell(args.host, args.username, password)


if __name__ == "__main__":
    main()
