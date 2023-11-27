import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from profile_manager import ProfileManager
import subprocess

class GitCredentialsManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Git Credentials Manager")
        self.root.geometry("400x250")
        self.root.minsize(400, 250)
        
        self.profile_manager = ProfileManager()
        self.profiles = self.profile_manager.load_profiles()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        self.credentials_frame = ttk.Frame(self.notebook)
        self.profiles_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.credentials_frame, text='Credentials')
        self.notebook.add(self.profiles_frame, text='Profiles')

        self.create_credentials_widgets()
        self.create_profiles_widgets()
        self.refresh_display()

    def create_credentials_widgets(self):
        style = ttk.Style()
        style.configure('TLabel', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10))
        style.configure('TEntry', font=('Arial', 10))

        ttk.Label(self.credentials_frame, text="Username:").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.name_entry = ttk.Entry(self.credentials_frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        ttk.Label(self.credentials_frame, text="Email:").grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.email_entry = ttk.Entry(self.credentials_frame)
        self.email_entry.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

        save_button = ttk.Button(self.credentials_frame, text="Save Credentials", command=self.save_credentials)
        save_button.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

        refresh_button = ttk.Button(self.credentials_frame, text="Refresh", command=self.refresh_display)
        refresh_button.grid(row=2, column=1, padx=10, pady=10, sticky='ew')

        self.status_bar = ttk.Label(self.credentials_frame, text="", relief='sunken', anchor='w')
        self.status_bar.grid(row=3, column=0, columnspan=2, sticky='ew', padx=10, pady=5)

        self.credentials_frame.grid_columnconfigure(1, weight=1)

    def create_profiles_widgets(self):
        self.profile_combobox = ttk.Combobox(self.profiles_frame, values=list(self.profiles.keys()), state='readonly')
        self.profile_combobox.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        self.profile_combobox.bind("<<ComboboxSelected>>", self.on_profile_selected)

        load_profile_button = ttk.Button(self.profiles_frame, text="Load Profile", command=self.load_profile)
        load_profile_button.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

        save_profile_button = ttk.Button(self.profiles_frame, text="Save Profile", command=self.save_profile)
        save_profile_button.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

        delete_profile_button = ttk.Button(self.profiles_frame, text="Delete Profile", command=self.delete_profile)
        delete_profile_button.grid(row=3, column=0, padx=10, pady=10, sticky='ew')

        self.profiles_frame.grid_columnconfigure(0, weight=1)

    def display_status(self, message, error=False):
        self.status_bar['text'] = message
        self.status_bar['foreground'] = 'red' if error else 'green'

    def get_git_credentials(self):
        try:
            name = subprocess.check_output(["git", "config", "user.name"], text=True).strip()
            email = subprocess.check_output(["git", "config", "user.email"], text=True).strip()
            return name, email
        except subprocess.CalledProcessError:
            self.display_status("Git not configured", error=True)
            return "", ""

    def set_git_credentials(self, name, email):
        try:
            subprocess.run(["git", "config", "--global", "user.name", name], check=True)
            subprocess.run(["git", "config", "--global", "user.email", email], check=True)
            self.display_status("Credentials updated successfully")
        except subprocess.CalledProcessError:
            self.display_status("Failed to update credentials", error=True)

    def save_credentials(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        self.set_git_credentials(name, email)

    def refresh_display(self):
        name, email = self.get_git_credentials()
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, name)
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, email)
        self.display_status("Display refreshed")

    def load_profile(self):
        selected_profile = self.profile_combobox.get()
        if selected_profile in self.profiles:
            profile_data = self.profiles[selected_profile]
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, profile_data['name'])
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, profile_data['email'])

    def save_profile(self):
        profile_name = simpledialog.askstring("Profile Name", "Enter profile name:")
        if profile_name:
            self.profiles[profile_name] = {
                'name': self.name_entry.get(),
                'email': self.email_entry.get()
            }
            self.save_profiles()
            self.profile_combobox['values'] = list(self.profiles.keys())

    def delete_profile(self):
        current_profile = self.profile_combobox.get()
        if current_profile and messagebox.askyesno("Delete Profile", f"Are you sure you want to delete the profile '{current_profile}'?"):
            del self.profiles[current_profile]
            self.save_profiles()
            self.profile_combobox['values'] = list(self.profiles.keys())
            self.profile_combobox.set('')

    def on_profile_selected(self, event=None):
        selected_profile = self.profile_combobox.get()
        if selected_profile in self.profiles:
            profile_data = self.profiles[selected_profile]
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, profile_data['name'])
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, profile_data['email'])
