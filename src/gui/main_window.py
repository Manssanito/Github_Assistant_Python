import tkinter as tk
import services.github_api as gh
import services.Output_helper as oh
import os
from dotenv import load_dotenv

load_dotenv()

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GitHub API Assistant")

        self.root.geometry("800x500")
        
        # Row 1 - ApiKey Entry
        row1 = tk.Frame(self.root)
        row1.pack(pady=10)
        
        # Row 2 - Owner Entry
        row2 = tk.Frame(self.root)
        row2.pack(pady=10)
        
        # Row 3 - Credentials Functions
        row3 = tk.Frame(self.root)
        row3.pack(pady=10)
        
        # Row 4 - Collaborator Entry
        row4 = tk.Frame(self.root)
        row4.pack(pady=10)
        
        # Row 5 - Api Functions
        row5 = tk.Frame(self.root)
        row5.pack(pady=10)
        
        # Row 6 - Output
        row6 = tk.Frame(self.root)
        row6.pack(pady=10)
        
        # Row 1 - ApiKey Entry
        label_ApiKey = tk.Label(row1, text='Github ApiKey')
        label_ApiKey.pack(side=tk.LEFT, padx=5)
        
        self.entry_ApiKey = tk.Entry(row1 ,width=120)
        self.entry_ApiKey.pack(side=tk.LEFT,padx=5)
        
        # Row 2 - Owner Entry
        self.label_owner = tk.Label(row2, text='Owner/Organization Name')
        self.label_owner.pack(side=tk.LEFT,pady=10)

        self.entry_owner = tk.Entry(row2,width=40)
        self.entry_owner.pack(side=tk.LEFT,padx=5)
        
        # Row 3 - Credentials functions
        self.button_load = tk.Button(row3, text='Load Credentials', command=self.load_credentials)
        self.button_load.pack(side=tk.LEFT, padx=10)
        
        self.button_save = tk.Button(row3, text='Save Credentials', command=self.save_credentials)
        self.button_save.pack(side=tk.LEFT, padx=10)
        
        self.button_delete = tk.Button(row3, text='Delete Credentials', command=self.delete_credentials)
        self.button_delete.pack(side=tk.LEFT, padx=10)
        
        # Row 4 - Collaborator Entry
        self.label_collaborator = tk.Label(row4, text='Collaborator Name')
        self.label_collaborator.pack(side=tk.LEFT,pady=10)

        self.entry_collaborator = tk.Entry(row4,width=40)
        self.entry_collaborator.pack(side=tk.LEFT,padx=5)

        # Row 5 - Functions
        self.button_find_repos = tk.Button(row5, text='Find repos', command=self.find_repos)
        self.button_find_repos.pack(side=tk.LEFT, padx=10)
        
        self.button_collaborators_list = tk.Button(row5, text='Collaborator list', command=self.collaborators_list)
        self.button_collaborators_list.pack(side=tk.LEFT, padx=10)
        
        self.button_repos_with_this_collaborator = tk.Button(row5, text='Repos with this user', command=self.repos_with_this_collaborator)
        self.button_repos_with_this_collaborator.pack(side=tk.LEFT, padx=10)
        
        self.button_repos_invitations = tk.Button(row5, text='Repos invitations', command=self.repos_invitations)
        self.button_repos_invitations.pack(side=tk.LEFT, padx=10)
        
        # Row 6
        self.button_repos_excel = tk.Button(row6, text='Excel report', command=self.repos_excel_report)
        self.button_repos_excel.pack(side=tk.LEFT, padx=10)

        # Row 6
        self.text = tk.Text(self.root)
        self.text.pack(fill='both', expand='yes', pady=10, padx=10)

    # Credentials Funtions
    def load_credentials(self):
        load_dotenv(override=True)
        self.entry_ApiKey.delete(0, tk.END)
        self.entry_ApiKey.insert(0,os.getenv("GITHUB_TOKEN"))
        self.entry_owner.delete(0, tk.END)
        self.entry_owner.insert(0,os.getenv("GITHUB_OWNER"))
    
    def save_credentials(self):
        github_token = self.entry_ApiKey.get()
        self.save_value("GITHUB_TOKEN",github_token)       
        owner = self.entry_owner.get()
        self.save_value("GITHUB_OWNER",owner)
        load_dotenv(override=True)
        
    def delete_credentials(self):
        self.save_value("GITHUB_TOKEN",'')
        self.save_value("GITHUB_OWNER",'')
        load_dotenv(override=True)
        self.load_credentials()
        
    def save_value(self,key,key_value):
        rows = []
        key_exists = False
        try:
            with open(".env", "r") as f:
                for row in f:
                    if row.startswith(f"{key}="):
                        rows.append(f"{key}={key_value}\n")
                        key_exists = True
                    else:
                        rows.append(row)
                        
        except FileNotFoundError:
            pass
        
        if not key_exists:
            rows.append(f"{key}={key_value}\n")
            
        with open(".env", "w") as f:
            f.writelines(rows)

    # Api Functions
    def find_repos(self):
        apiKey = self.entry_ApiKey.get()
        repos = gh.get_repo_list(apiKey)
        self.text.delete(1.0, tk.END)
        if repos is not None:
            for repo in repos:
                self.text.insert(tk.END, f"- {repo['name']}\n")
        else:
            self.text.insert(tk.END, "Repos not found or API error")
    
    def collaborators_list(self):
        apiKey = self.entry_ApiKey.get()
        owner = self.entry_owner.get()
        self.text.delete(1.0, tk.END)
        collaborators = gh.get_all_unique_collaborators(owner,apiKey)
        if collaborators is not None:
            for collaborator in collaborators:
                self.text.insert(tk.END, f"- {collaborator}\n")
        else:
            self.text.insert(tk.END, "Collaborators not found or API error")
    
    def repos_with_this_collaborator(self):
        apiKey = self.entry_ApiKey.get()
        owner = self.entry_owner.get()
        collaborator = self.entry_collaborator.get()
        self.text.delete(1.0, tk.END)
        repos = gh.get_repos_with_this_collaborator(owner,apiKey,collaborator)
        if repos is not None:
            for repo, url in repos.items():
                self.text.insert(tk.END, f"{repo}: {url}\n")
        else:
            self.text.insert(tk.END, "this user its not a collaborator or API error")
    
    def repos_invitations(self):
        apiKey = self.entry_ApiKey.get()
        owner = self.entry_owner.get()
        collaborator = self.entry_collaborator.get()
        self.text.delete(1.0, tk.END)
        repos = gh.get_all_invitations(owner,apiKey)
        if repos is not None:
            for repo, user in repos.items():
                self.text.insert(tk.END, f"{repo}: {user}\n")
        else:
            self.text.insert(tk.END, "this user its not a collaborator or API error")
            
    def repos_excel_report(self):
        apiKey = self.entry_ApiKey.get()
        owner = self.entry_owner.get()
        self.text.delete(1.0, tk.END)
        report = oh.create_excel_report(owner,apiKey)
        if report is None:
            self.text.insert("Report file generated.")
        else:
            self.text.insert("An error ocurred")
        
    def init(self):
        self.root.mainloop()
