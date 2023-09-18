#Cabrillorator v0.1
#by KC1RVK September 2023
#Cabrillorator is a simple program to allow a user to enter Amatuer Radio QSO information and store it in Cabrillo format.  The application is optimized to make it easy to quickly capture QSOs during a contest or other rapid fire contact formats.
#Requires the tkinter library

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import datetime

class QSOApp(tk.Tk):
    def popup():
        # Create a new window
        popup = tk.Toplevel()
        popup.title("Popup Window")

        # Create a Text widget to display the text
        text = tk.Text(popup, wrap="word")
        text.insert("1.0", "Some text that the user can select and copy")
        text.pack(fill="both", expand=True)

        # Create a Button widget to close the window
        button = tk.Button(popup, text="Close", command=popup.destroy)
        button.pack()

        # Allow the user to select the text
        text.tag_configure("sel", background="yellow")
        text.bind("<ButtonRelease-1>", lambda event: text.tag_add("sel", "sel.first", "sel.last"))

        # Run the window
        popup.mainloop()

    def __init__(self):
        super().__init__()
        self.title("Cabrillorator v0.1beta 05032023 KC1RVK")
        self.geometry("800x400")
        self.qso_log = []
        self.create_widgets()

    def create_widgets(self):
        self.entries_frame = ttk.Frame(self)
        self.entries_frame.grid(row=0, column=0, padx=10, pady=10)

        self.log_frame = ttk.Frame(self)
        self.log_frame.grid(row=0, column=1, padx=10, pady=10)

        self.save_button = ttk.Button(self, text="Save Log", command=self.save_log)
        self.save_button.grid(row=1, column=1, padx=10, pady=10)

        self.clear_log_button = ttk.Button(self, text="Clear Log", command=self.clear_log)
        self.clear_log_button.grid(row=1, column=1, padx=(5, 10), pady=10, sticky="w")

        self.create_entries()
        self.create_log()

        self.create_help_menu()

    def create_entries(self):
        labels = ["Frequency", "Mode", "Date", "Time", "Sent Call", "Sent RST", "Sent QTH", "Received Call", "Received RST", "Received QTH"]
        self.entries = {}
        self.keep_values = {}

        for i, label in enumerate(labels):
            ttk.Label(self.entries_frame, text=label).grid(row=i, column=0, padx=5, pady=5)

            text_var = tk.StringVar()
            text_var.trace("w", lambda *args, var=text_var: var.set(var.get().upper()))
     
            entry = ttk.Entry(self.entries_frame, textvariable=text_var)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[label] = entry

            if label in ["Frequency", "Mode", "Sent Call", "Sent QTH"]:
                keep_value = tk.BooleanVar()
                keep_value.set(False)
                check_button = ttk.Checkbutton(self.entries_frame, text="Keep", variable=keep_value, takefocus=False)
                check_button.grid(row=i, column=2, padx=5, pady=5)
                self.keep_values[label] = keep_value

        # Set default values for Date and Time entries
        now = datetime.datetime.utcnow()
        self.entries["Date"].insert(0, now.strftime("%y%m%d"))
        self.entries["Time"].insert(0, now.strftime("%H%M"))

        add_button = ttk.Button(self.entries_frame, text="Add QSO", command=self.add_qso)
        add_button.grid(row=len(labels), column=1, padx=5, pady=5)

        clear_button = ttk.Button(self.entries_frame, text="Clear", command=self.clear_entries)
        clear_button.grid(row=len(labels), column=0, padx=5, pady=5)

        # Make the Add QSO button the default when the user hits Enter
        self.bind('<Return>', lambda event: self.add_qso())

    def create_log(self):
        self.log_text = tk.Text(self.log_frame, wrap=tk.WORD, width=59, height=20)
        self.log_text.pack()

    def add_qso(self):
        qso_data = [entry.get() for entry in self.entries.values()]
        qso_line = "QSO: " + " ".join(qso_data)
        self.qso_log.append(qso_line)
        self.log_text.insert(tk.END, qso_line + "\n")
        self.clear_entries()
        self.entries["Frequency"].focus_set()

    def save_log(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as file:
                file.write("\n".join(self.qso_log))

    def clear_entries(self):
        for label, entry in self.entries.items():
            if label not in ["Frequency", "Mode", "Sent Call", "Sent QTH"] or not self.keep_values[label].get():
                entry.delete(0, tk.END)
        self.entries["Frequency"].focus_set()
       
        # Set default values for Date and Time entries
        now = datetime.datetime.utcnow()
        self.entries["Date"].insert(0, now.strftime("%y%m%d"))
        self.entries["Time"].insert(0, now.strftime("%H%M"))

    def clear_log(self):
        self.qso_log.clear()
        self.log_text.delete(1.0, tk.END)

    def create_help_menu(self):
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        help_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_help)

    def show_help(self):
        help_window = tk.Toplevel(self)
        help_window.title("Help")
        help_text = tk.Text(help_window, wrap=tk.WORD)
        help_text.insert(tk.END, "Creator: KC1RVK\nWhat: A simple Cabrillo format QSO logger\nVer: v0.1beta 050323\nFeedback and Ideas:  Find my contact info on QRZ.COM\n\nSome Tips\n1. The Keep button will retain those values when the Clear or Add QSO button is used\n2. Add QSO also evokes clear\n3. Date and Time are in UTC\n4. MAKE SURE YOU SAVE THE LOG")
        help_text.config(state=tk.DISABLED)
        help_text.pack(expand=True, fill=tk.BOTH)
        help_window.geometry("450x200")

if __name__ == "__main__":
    app = QSOApp()
    app.mainloop()
