import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os

GAMES_FILE = "games.json"  # games storage file

class GameVaultApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GameVault - Video Game Collection Manager")
        self.geometry("500x400")

        self.games = []  #list to hold game data
        self.loadGames()

        # main menu ui
        self.createMainMenu()

    def createMainMenu(self):
        tk.Label(self, text="Welcome to GameVault!", font=("Helvetica", 18)).pack(pady=20)

        tk.Button(self, text="View Games", width=20, command=self.viewGames).pack(pady=10)
        tk.Button(self, text="Add New Game", width=20, command=self.addNewGame).pack(pady=10)
        tk.Button(self, text="Exit", width=20, command=self.quit).pack(pady=10)

    def viewGames(self):
        ViewGamesWindow(self)

    def addNewGame(self):
        AddGameWindow(self)

    def loadGames(self):
        """Load games from a JSON file if it exists."""
        if os.path.exists(GAMES_FILE):
            with open(GAMES_FILE, "r") as file:
                self.games = json.load(file)

    def saveGames(self):
        """Save games to a JSON file."""
        with open(GAMES_FILE, "w") as file:
            json.dump(self.games, file, indent=4)

class ViewGamesWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("View Games")
        self.geometry("600x400")

        self.listbox = tk.Listbox(self, width=80)
        self.listbox.pack(padx=10, pady=10)

        for game in master.games:
            self.listbox.insert(tk.END, game["title"])

class AddGameWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title("Add New Game")
        self.geometry("400x400")

        tk.Label(self, text="Title:").pack()
        self.titleEntry = tk.Entry(self)
        self.titleEntry.pack()

        tk.Label(self, text="Genre:").pack()
        self.genreEntry = tk.Entry(self)
        self.genreEntry.pack()

        tk.Label(self, text="Platform:").pack()
        self.platformEntry = tk.Entry(self)
        self.platformEntry.pack()

        tk.Label(self, text="Progress:").pack()
        self.progressEntry = tk.Entry(self)
        self.progressEntry.pack()

        tk.Label(self, text="Notes:").pack()
        self.notesEntry = tk.Entry(self)
        self.notesEntry.pack()

        tk.Button(self, text="Upload Image", command=self.uploadImage).pack(pady=5)
        self.imagePath = ""

        tk.Button(self, text="Save Game", command=self.saveGame).pack(pady=10)

    def uploadImage(self):
        filepath = filedialog.askopenfilename(
            title="Select Game Artwork",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")]
        )
        if filepath:
            self.imagePath = filepath

    def saveGame(self):
        new_game = {
            "title": self.titleEntry.get(),
            "genre": self.genreEntry.get(),
            "platform": self.platformEntry.get(),
            "progress": self.progressEntry.get(),
            "notes": self.notesEntry.get(),
            "image_path": self.imagePath
        }
        self.master.games.append(new_game)
        self.master.saveGames()  # save the updated game list
        messagebox.showinfo("Saved", "Game added successfully!")
        self.destroy()

if __name__ == "__main__":
    app = GameVaultApp()
    app.mainloop()
