import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import json
import os

GAMES_FILE = "games.json"  # games storage file

class GameVaultApp(tk.Tk):
    """Main window for GameVault Program.
    
        This class handles UI setup, showing main menu, buttons for navigation to other windows
        such as viewing games, adding games, and editing existing games."""
    def __init__(self):
        super().__init__()
        self.title("GameVault - Video Game Collection Manager")
        self.geometry("500x400")

        self.games = []  #list to hold game data
        self.loadGames()

        # main menu ui
        self.createMainMenu()

    def createMainMenu(self):
        """Create the main menu UI."""
        tk.Label(self, text="Welcome to GameVault!", font=("Helvetica", 18)).pack(pady=10)

        try:
            image_path = os.path.join(os.path.dirname(__file__), "GameVault.png")
            image = Image.open(image_path)
            image = image.resize((200, 200), Image.Resampling.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(image)
            tk.Label(self, image=self.logo_image).pack(pady=10)
        except Exception as e:
            tk.Label(self, text=f"Image load error: {str(e)}").pack(pady=10)

        tk.Button(self, text="View Games", width=20, command=self.viewGames).pack(pady=5)
        tk.Button(self, text="Add New Game", width=20, command=self.addNewGame).pack(pady=5)
        tk.Button(self, text="Exit", width=20, command=self.quit).pack(pady=5)

    def viewGames(self):
        """Open view games window."""
        ViewGamesWindow(self)

    def addNewGame(self):
        """Open add new game window."""
        AddGameWindow(self)

    def loadGames(self):
        """Load games from a JSON file."""
        if os.path.exists(GAMES_FILE):
            with open(GAMES_FILE, "r") as file:
                self.games = json.load(file)

    def saveGames(self):
        """Save games to a JSON file."""
        with open(GAMES_FILE, "w") as file:
            json.dump(self.games, file, indent=4)

class ViewGamesWindow(tk.Toplevel):
    """Window to view all games in the collection."""
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title("View Games")
        self.geometry("400x200")

        self.listbox = tk.Listbox(self, width=80)
        self.listbox.pack(padx=10, pady=10)
        self.listbox.bind("<<ListboxSelect>>", self.showDetails)

        for game in master.games:
            self.listbox.insert(tk.END, game["title"])

    def showDetails(self, event):
        """Show details of the selected game."""
        if not self.listbox.curselection():
            return
        index = self.listbox.curselection()[0]
        selected_game = self.master.games[index]
        GameDetailWindow(self.master, selected_game)

class AddGameWindow(tk.Toplevel):
    """Window to add a new game to the collection."""
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
        """Open file dialog to select an image for the game."""
        filepath = filedialog.askopenfilename(
            title="Select Game Artwork",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")]
        )
        if filepath:
            self.imagePath = filepath

    def saveGame(self):
        """Validate input and save the new game to the collection."""
        title = self.titleEntry.get().strip()
        genre = self.genreEntry.get().strip()
        platform = self.platformEntry.get().strip()

        if not title or not genre or not platform:
            messagebox.showerror("Validation Error", "Title, Genre, and Platform are required.")
            return

        new_game = {
            "title": title,
            "genre": genre,
            "platform": platform,
            "progress": self.progressEntry.get().strip(),
            "notes": self.notesEntry.get().strip(),
            "image_path": self.imagePath
        }
        self.master.games.append(new_game)
        self.master.saveGames()
        messagebox.showinfo("Saved", "Game added successfully!")
        self.destroy()
        
class GameDetailWindow(tk.Toplevel):
    """Window to show details of a selected game."""
    def __init__(self, master, game):
        super().__init__(master)
        self.master = master
        self.game = game
        self.title(f"Details - {game['title']}")
        self.geometry("500x600")

        # Container frame for icon and title
        top_frame = tk.Frame(self)
        top_frame.pack(fill="x", pady=10)

        # Load and show controller icon in the top-right
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "controllericon.png")
            icon_image = Image.open(icon_path)
            icon_image = icon_image.resize((48, 48), Image.Resampling.LANCZOS)
            self.icon_photo = ImageTk.PhotoImage(icon_image)
            tk.Label(top_frame, image=self.icon_photo).pack(side="right", padx=10)
        except Exception as e:
            tk.Label(top_frame, text="🎮").pack(side="right", padx=10)

        # Title label aligned left in same row
        tk.Label(top_frame, text=game["title"], font=("Helvetica", 16, "bold")).pack(side="left", padx=10)

        # Game info labels
        tk.Label(self, text=f"Genre: {game['genre']}").pack()
        tk.Label(self, text=f"Platform: {game['platform']}").pack()
        tk.Label(self, text=f"Progress: {game['progress']}").pack()
        tk.Label(self, text=f"Notes: {game['notes']}").pack()

        # Display main game image if present
        if game["image_path"] and os.path.exists(game["image_path"]):
            try:
                img = Image.open(game["image_path"])
                img.thumbnail((300, 300))
                self.photo = ImageTk.PhotoImage(img)
                tk.Label(self, image=self.photo).pack(pady=10)
            except Exception:
                tk.Label(self, text="Error loading game image").pack()
        else:
            tk.Label(self, text="No game image available").pack(pady=10)

        tk.Button(self, text="Edit Game", command=self.editGame).pack(pady=10)
        
    def editGame(self):
        EditGameWindow(self.master, self.game)
        self.destroy()
        
class EditGameWindow(tk.Toplevel):
    """Window to edit an existing game."""
    def __init__(self, master, game):
        super().__init__(master)
        self.master = master
        self.game = game
        self.title("Edit Game")
        self.geometry("400x400")

        tk.Label(self, text="Title:").pack()
        self.titleEntry = tk.Entry(self)
        self.titleEntry.insert(0, game["title"])
        self.titleEntry.pack()

        tk.Label(self, text="Genre:").pack()
        self.genreEntry = tk.Entry(self)
        self.genreEntry.insert(0, game["genre"])
        self.genreEntry.pack()

        tk.Label(self, text="Platform:").pack()
        self.platformEntry = tk.Entry(self)
        self.platformEntry.insert(0, game["platform"])
        self.platformEntry.pack()

        tk.Label(self, text="Progress:").pack()
        self.progressEntry = tk.Entry(self)
        self.progressEntry.insert(0, game["progress"])
        self.progressEntry.pack()

        tk.Label(self, text="Notes:").pack()
        self.notesEntry = tk.Entry(self)
        self.notesEntry.insert(0, game["notes"])
        self.notesEntry.pack()

        self.imagePath = game["image_path"]
        tk.Button(self, text="Change Image", command=self.uploadImage).pack(pady=5)

        tk.Button(self, text="Save Changes", command=self.saveChanges).pack(pady=10)

    def uploadImage(self):
        """Open file dialog to select a new image for the game."""
        filepath = filedialog.askopenfilename(
            title="Select Game Artwork",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")]
        )
        if filepath:
            self.imagePath = filepath

    def saveChanges(self):
        """Validate input and save changes to the game."""
        title = self.titleEntry.get().strip()
        genre = self.genreEntry.get().strip()
        platform = self.platformEntry.get().strip()

        if not title or not genre or not platform:
            messagebox.showerror("Validation Error", "Title, Genre, and Platform are required.")
            return

        self.game["title"] = title
        self.game["genre"] = genre
        self.game["platform"] = platform
        self.game["progress"] = self.progressEntry.get().strip()
        self.game["notes"] = self.notesEntry.get().strip()
        self.game["image_path"] = self.imagePath

        self.master.saveGames()
        messagebox.showinfo("Updated", "Game updated successfully!")
        self.destroy()

if __name__ == "__main__":
    app = GameVaultApp()
    app.mainloop()
