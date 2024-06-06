import os
import subprocess
import sys
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog, StringVar


class ProjectCreator(ttk.Window):
    def __init__(self):
        super().__init__(themename="superhero")
        self.title("Project Creator")
        self.geometry("600x240")
        self.resizable(False, False)

        # Variables
        self.project_name_var = StringVar()
        self.local_repo_var = StringVar()
        self.remote_repo_var = StringVar()

        # Trace variables
        self.project_name_var.trace_add("write", self.update_create_button_state)
        self.remote_repo_var.trace_add("write", self.update_create_button_state)

        # Labels and Entry widgets
        self.lbl_name = ttk.Label(self, text="Project Name:")
        self.lbl_name.grid(row=0, column=0, padx=10, pady=10)
        self.ent_project_name = ttk.Entry(self, textvariable=self.project_name_var, width=50)
        self.ent_project_name.grid(row=0, column=1, padx=10, pady=10)
        self.btn_name = ttk.Button(self, text="Clear", width=15, command=lambda: self.clear_entry(self.ent_project_name), bootstyle=SECONDARY)
        self.btn_name.grid(row=0, column=2, padx=10, pady=10)

        self.lbl_local_rep = ttk.Label(self, text="Local Repo Path:")
        self.lbl_local_rep.grid(row=1, column=0, padx=10, pady=10)
        self.ent_local_rep = ttk.Entry(self, textvariable=self.local_repo_var, width=50)
        self.ent_local_rep.grid(row=1, column=1, padx=10, pady=10)
        self.btn_local_rep = ttk.Button(self, text="Choose Folder", width=15, command=self.choose_folder, bootstyle=SECONDARY)
        self.btn_local_rep.grid(row=1, column=2, padx=10, pady=10)

        self.lbl_remote_rep = ttk.Label(self, text="Remote Repo URL:")
        self.lbl_remote_rep.grid(row=2, column=0, padx=10, pady=10)
        self.ent_remote_rep = ttk.Entry(self, textvariable=self.remote_repo_var, width=50)
        self.ent_remote_rep.grid(row=2, column=1, padx=10, pady=10)
        self.ent_remote_rep.bind("<KeyRelease>", self.fill_project_name)
        self.btn_remote_rep = ttk.Button(self, text="Clear", width=15, command=lambda: self.clear_entry(self.ent_remote_rep), bootstyle=SECONDARY)
        self.btn_remote_rep.grid(row=2, column=2, padx=10, pady=10)

        # Checkbox for first commit
        self.first_commit_var = ttk.IntVar(value=1)
        self.chk_first_commit = ttk.Checkbutton(self, text="Perform first commit", variable=self.first_commit_var, bootstyle=SUCCESS)
        self.chk_first_commit.grid(row=3, column=0, columnspan=3, pady=10)

        # Create Project Button
        self.create_button = ttk.Button(self, text="Create Project", command=self.create_project, bootstyle=SUCCESS)
        self.create_button.grid(row=4, column=0, columnspan=3, pady=20)
        self.create_button["state"] = "disabled"

    def clear_entry(self, entry):
        """
        Clears the text in the given entry widget.

        Args:
            entry (ttk.Entry): The entry widget to clear.
        """
        entry.delete(0, ttk.END)

    def choose_folder(self):
        """
        Opens a dialog to choose a folder and sets the chosen path to the local repo entry.
        """
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.local_repo_var.set(folder_path)

    def fill_project_name(self, event):
        """
        Fills the project name based on the remote repo URL.
        """
        repo_url = self.ent_remote_rep.get()
        if repo_url:
            project_name = repo_url.split('/')[-1].replace('.git', '')
            self.project_name_var.set(project_name)

    def create_venv(self, project_path):
        """
        Creates a virtual environment in the given project path.

        Args:
            project_path (str): Path to the project directory.
        """
        subprocess.run([sys.executable, '-m', 'venv', os.path.join(project_path, 'venv')])

    def create_file(self, file_path, content):
        """
        Creates a file with the given content.

        Args:
            file_path (str): Path to the file.
            content (str): Content to write to the file.
        """
        with open(file_path, 'w') as file:
            file.write(content)

    def run_git_command(self, args, cwd):
        """
        Runs a git command in the specified directory.

        Args:
            args (list): List of git command arguments.
            cwd (str): Directory to run the command in.

        Returns:
            int: Return code of the git command.
        """
        result = subprocess.run(['git'] + args, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running {' '.join(args)}: {result.stderr}")
        return result.returncode

    def create_project(self):
        """
        Creates a new project with a local and remote git repository.
        Initializes a virtual environment, creates .gitignore and requirements.txt files,
        and performs the initial commit and push if the flag is set.
        """
        repo_url = self.ent_remote_rep.get()
        project_name = self.ent_project_name.get()
        project_path = os.path.join(self.ent_local_rep.get(), project_name)

        try:
            # Creating the project folder
            if not os.path.exists(project_path):
                os.makedirs(project_path)

            # Initializing the git repository
            if self.run_git_command(['init'], project_path) != 0:
                return

            # Adding the remote repository
            if self.run_git_command(['remote', 'add', 'origin', repo_url], project_path) != 0:
                return

            # Creating the virtual environment
            self.create_venv(project_path)

            # Adding .gitignore and requirements.txt files
            gitignore_content = """
            # Python
            __pycache__/
            *.py[cod]
            *.pyo
            .env
            venv/
            """
            self.create_file(os.path.join(project_path, '.gitignore'), gitignore_content)
            self.create_file(os.path.join(project_path, 'requirements.txt'), "")

            # Adding, committing, and pushing the files if first_commit is checked
            if self.first_commit_var.get() == 1:
                if self.run_git_command(['add', '.'], project_path) != 0:
                    return
                if self.run_git_command(['commit', '-m',
                                         f'Initial commit for {project_name} with venv, .gitignore, and requirements.txt'],
                                        project_path) != 0:
                    return
                if self.run_git_command(['push', '-u', 'origin', 'master'], project_path) != 0:
                    return

            messagebox.showinfo("Success",
                                f"Project '{project_name}' has been created and pushed to the remote repository.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_create_button_state(self, *args):
        """
        Updates the state of the create button based on the project name and remote repo URL entries.
        """
        if self.project_name_var.get() and self.remote_repo_var.get():
            self.create_button["state"] = "normal"
        else:
            self.create_button["state"] = "disabled"


if __name__ == "__main__":
    app = ProjectCreator()
    app.mainloop()
