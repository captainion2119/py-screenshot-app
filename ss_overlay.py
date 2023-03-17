import tkinter as tk
from PIL import ImageGrab, ImageTk
from PIL import Image
import os

class ScreenshotApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Screenshot App")

        # create buttons
        self.region_button = tk.Button(self.master, text="Select Region", command=self.select_region)
        self.region_button.pack()

        self.screenshot_button = tk.Button(self.master, text="Take Screenshot", command=self.take_screenshot)
        self.screenshot_button.pack()

        # set up variables for selecting region
        self.screenshot_region = None
        self.screenshot_counter = 1

    def select_region(self):
        # hide the root window and grab a screenshot of the entire screen
        self.master.withdraw()
        screenshot = ImageGrab.grab()

        # create a semi-transparent overlay on top of the screenshot
        overlay = Image.new('RGBA', screenshot.size, (0,0,0,128))


        # show the overlay and wait for the user to click twice
        self.overlay_window = tk.Toplevel()
        self.overlay_canvas = tk.Canvas(self.overlay_window, width=screenshot.size[0], height=screenshot.size[1])
        self.overlay_canvas.pack()
        self.overlay_image = ImageTk.PhotoImage(overlay)
        self.overlay_canvas.create_image(0, 0, anchor=tk.NW, image=self.overlay_image)
        self.overlay_window.attributes('-fullscreen', True)
        self.overlay_canvas.bind("<Button 1>", self.on_first_click)

    def on_first_click(self, event):
        # record the first click position
        self.first_click = (event.x, event.y)
        self.overlay_canvas.bind("<Button 1>", self.on_second_click)

    def on_second_click(self, event):
        # record the second click position and close the overlay window
        self.second_click = (event.x, event.y)
        self.overlay_window.destroy()

        # calculate the screenshot region
        x1, y1 = self.first_click
        x2, y2 = self.second_click
        self.screenshot_region = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))

        # show the root window again
        self.master.deiconify()

    def take_screenshot(self):
        if self.screenshot_region is None:
            return

        # take a screenshot of the selected region
        screenshot = ImageGrab.grab(bbox=self.screenshot_region)

        # save the screenshot
        screenshot_filename = f"screenshot_{self.screenshot_counter}.png"
        screenshot_path = os.path.join(os.getcwd(), screenshot_filename)
        screenshot.save(screenshot_path)

        # increment the screenshot counter
        self.screenshot_counter += 1

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenshotApp(root)
    root.mainloop()