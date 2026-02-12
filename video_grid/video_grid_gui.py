
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar, Button, Label
from video_grid.video_grid import VideoGrid

class VideoGridGUI:
    """ Create a GUI that allows the user to select video files and show them in a list"""

    def __init__ (self, root):
        self.root = root
        self.root.title("Video Grid Selector")

        self.input_paths = []
        self.output_path = ""

        self.label = Label(root, text="Select video files to display in a grid:")
        self.label.pack(pady=10)

        self.listbox = Listbox(root, selectmode=tk.MULTIPLE, width=100, height=15)
        self.listbox.pack(pady=20)

        self.scrollbar = Scrollbar(root)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.add_button = Button(root, text="Add Videos", command=self.add_videos)
        self.add_button.pack(pady=5)

        self.show_button = Button(root, text="Show Selected Videos", command=self.show_selected_videos)
        self.show_button.pack(pady=5)

        self.run_button = Button(root, text="Create Video Grid", command=self.create_output_video)
        self.run_button.pack(pady=5)

        self.quit_button = Button(root, text="Exit", command=root.quit)
        self.quit_button.pack(pady=5)

    def add_videos (self):
        file_paths = filedialog.askopenfilenames(
            title = "Select Video Files", 
            filetypes = [("Video Files", "*.mp4;*.avi;*.mov;*.mkv")])
        for path in file_paths:
            if path not in self.listbox.get(0, tk.END):
                self.listbox.insert(tk.END, path)

    def get_all_listbox_items (self):
        # Use the get method with indices 0 and tk.END
        all_items_tuple = self.listbox.get(0, tk.END)
        self.input_paths = list (all_items_tuple)

    def show_selected_videos (self):
        # selected_indices = self.listbox.curselection()
        # selected_files = [self.listbox.get(i) for i in selected_indices]
        # if not selected_files:
        #     messagebox.showwarning("No Selection", "Please select at least one video file.")
        #     return
        # messagebox.showinfo("Selected Videos", "\n".join(selected_files))
        # self.get_all_listbox_items()
        pass

    def create_output_video (self):
        self.get_all_listbox_items ()
        print(self.input_paths)
        if not self.input_paths:
            messagebox.showwarning ("No Videos", "Please add video files to create a grid.")
            return
        num_videos = len(self.input_paths)
        print(num_videos)
        # output_path = "../outputs/out_video.avi"
        output_path = f"outputs/video_grid_{num_videos}.avi"
        print(output_path)
        vg = VideoGrid (self.input_paths, output_path)
        vg.create_video_grid ()
