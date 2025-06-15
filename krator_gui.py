import tkinter as tk
from tkinter import messagebox

class KratorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("The Krator Project")
        self.configure(bg="black")
        self.geometry("600x400")

        header = tk.Label(self, text="The Krator Project", fg="#00FF00", bg="black", font=("Arial", 20, "bold"))
        header.pack(pady=10)

        button_frame = tk.Frame(self, bg="black")
        button_frame.pack(pady=20)

        tools = [
            ("GeoLocation Tools", self.geolocation_tools),
            ("IP and Port Tools", self.ip_port_tools),
            ("Web Scraping Tools", self.web_scraping_tools),
            ("OSINT Tools", self.osint_tools),
            ("Password Cracking Tools", self.password_cracking_tools),
            ("Bug Bounty Analyzer", self.bug_bounty_tools),
        ]

        for text, cmd in tools:
            btn = tk.Button(button_frame, text=text, command=cmd,
                            fg="#00FF00", bg="black", activebackground="#003300", activeforeground="#00FF00",
                            width=25, height=2)
            btn.pack(pady=5)

    def geolocation_tools(self):
        messagebox.showinfo("GeoLocation Tools", "Placeholder for geolocation functionality")

    def ip_port_tools(self):
        messagebox.showinfo("IP and Port Tools", "Placeholder for IP/Port functionality")

    def web_scraping_tools(self):
        messagebox.showinfo("Web Scraping Tools", "Placeholder for web scraping functionality")

    def osint_tools(self):
        messagebox.showinfo("OSINT Tools", "Placeholder for OSINT functionality")

    def password_cracking_tools(self):
        messagebox.showinfo("Password Cracking Tools", "This functionality is not implemented due to policy restrictions.")

    def bug_bounty_tools(self):
        messagebox.showinfo("Bug Bounty Analyzer", "Placeholder for bug bounty analysis functionality")

if __name__ == "__main__":
    app = KratorGUI()
    app.mainloop()
