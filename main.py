import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pyautogui


class ScreenshotApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Screenshot App")
        self.geometry("300x100")
        self.resizable(False, False)
        self.canvas = tk.Canvas(self, width=300, height=100)
        self.canvas.pack()
        self.screenshot_region = None
        self.bind("<ButtonPress-1>", self.select_region)
        self.bind("<ButtonRelease-1>", self.take_screenshot)

    def select_region(self, event):
        self.canvas.delete("rect")
        self.canvas.delete("text")
        self.start_x, self.start_y = event.x, event.y
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y, outline="green", tags="rect"
        )

        self.canvas.create_text(
            event.x,
            event.y - 10,
            text="Release to capture screenshot",
            fill="green",
            tags="text",
        )

    def take_screenshot(self, event):
        self.screenshot_region = (
            self.start_x,
            self.start_y,
            event.x,
            event.y,
        )
        self.withdraw()  # Move this line to the select_region function
        try:
            screenshot = pyautogui.screenshot(region=self.screenshot_region)
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG", "*.png"), ("All Files", "*.*")],
            )
            screenshot.save(file_path)
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    app = ScreenshotApp()
    app.mainloop()