###############################################################################
# Human Organ Quiz UI
#
# Desc: This script provides a Tkinter-based GUI for a human organ quiz game.
#       It uses AWSImgGen to generate images of human organs and quizzes the user
#       with multiple-choice questions. The UI manages user interaction, answer
#       checking, and feedback display.
#
# Author: Dipesh Karmakar
# Date: 07/08/2025
# License: MIT License
###############################################################################

# Import necessary libraries
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import random
import os

# Import your AWSImgGen class
from AWSImgGen import AWSImgGen

# List of human organs for quiz
ORGANS = [
    "Heart", "Liver", "Lung", "Kidney", "Stomach", "Brain", "Pancreas", "Small Intestine", "Large Intestine", "Spleen"
]

class QuizUI:
    """
    QuizUI creates a simple quiz interface for human body organs using AWSImgGen to generate images.
    Handles UI creation, question generation, answer checking, and feedback.
    """
    def __init__(self, root):
        """
        Initializes the QuizUI object, sets up the main window, variables, and starts the first question.
        Args:
            root (tk.Tk): The main Tkinter window.
        """
        self.root = root
        self.root.title("Human Organ Quiz")
        self.root.geometry("500x600")
        self.img_gen = AWSImgGen()
        self.correct_answer = None
        self.options = []
        self.selected_option = tk.StringVar()
        self.selected_option.trace_add("write", self.on_option_selected)  # Add this line
        self.image_label = None

        # UI Elements
        self.create_widgets()
        self.next_question()

    def create_widgets(self):
        """
        Creates and packs all the widgets for the quiz UI, including image display,
        radio buttons for options, control buttons, and status label.
        """
        # Image display section
        self.image_label = tk.Label(self.root, text="Loading image...", width=400, height=300)
        self.image_label.pack(pady=20)

        # Radio buttons for options
        self.radio_buttons = []
        for i in range(4):
            rb = ttk.Radiobutton(self.root, text="", variable=self.selected_option, value="", style='TRadiobutton')
            rb.pack(anchor='w', padx=40, pady=5)
            self.radio_buttons.append(rb)

        # Check and Next buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        self.check_button = tk.Button(button_frame, text="Check", command=self.check_answer, width=10)
        self.check_button.grid(row=0, column=0, padx=10)

        self.next_button = tk.Button(button_frame, text="Next", command=self.next_question, width=10)
        self.next_button.grid(row=0, column=1, padx=10)

        # Add a status label for messages
        self.status_label = tk.Label(self.root, text="", fg="blue", font=("Arial", 11))
        self.status_label.pack(pady=5)

    def next_question(self):
        """
        Generates a new quiz question, disables/enables appropriate buttons,
        generates a new image using AWSImgGen, and updates the UI.
        Handles image/content blocking by retrying with a new organ if needed.
        """
        # Immediately disable the Next button to prevent double clicks
        self.next_button.config(state="disabled")
        self.check_button.config(state="disabled")   # Start as disabled
        self.status_label.config(text="Wait for preparing the Quiz...")
        self.root.update()

        # Enable all radio buttons for the new question
        for rb in self.radio_buttons:
            rb.config(state="normal")

        while True:
            try:
                # Randomly select an organ as the correct answer
                self.correct_answer = random.choice(ORGANS)
                # Generate 3 random wrong options
                wrong_options = random.sample([o for o in ORGANS if o != self.correct_answer], 3)
                # Combine and shuffle options
                self.options = wrong_options + [self.correct_answer]
                random.shuffle(self.options)
                self.selected_option.set(None)

                # Update radio button texts and values
                for i, rb in enumerate(self.radio_buttons):
                    rb.config(text=self.options[i], value=self.options[i])

                # Generate new image using AWSImgGen
                prompt = f"A clear medical illustration of the human {self.correct_answer.lower()}."
                self.img_gen.PromptGeneration(prompt)
                response = self.img_gen.InvokeModel()
                image_path = self.img_gen.ProcessResponse(response)

                # Display the image
                self.display_image(image_path)

                # Remove waiting message and enable Next button
                self.status_label.config(text="")
                break  # Exit loop if successful

            except Exception as e:
                # If blocked or any error, try another organ
                self.status_label.config(text="Blocked or error, generating another image...")
                self.root.update()
                continue

    def display_image(self, image_path):
        """
        Opens and resizes the generated image, then displays it in the UI.
        Args:
            image_path (str): The file path of the image to display.
        """
        img = Image.open(image_path)
        # Use LANCZOS instead of ANTIALIAS
        img = img.resize((400, 300), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        self.image_label.configure(image=photo, text="")
        self.image_label.image = photo  # Keep a reference

    def check_answer(self):
        """
        Checks if the selected option is correct, shows feedback, and manages button states.
        Disables all option buttons and enables Next only after a correct answer.
        """
        selected = self.selected_option.get()
        print(f"Selected: {selected}, Correct: {self.correct_answer}")  # Debugging line
        if selected == None or selected == "" or selected not in self.options:
            self.show_custom_message("Select an option", "Please select an answer before checking.")
            print("No option selected.")
            return
        if selected == self.correct_answer:
            self.check_button.config(state="disabled")
            self.next_button.config(state="normal")  # Enable Next only after correct answer
            # Disable all radio buttons after correct answer
            for rb in self.radio_buttons:
                rb.config(state="disabled")
            self.show_custom_message("Congratulations!", "Correct! Well done!")
        else:
            self.show_custom_message("Try Again", f"Incorrect. The correct answer was: {self.correct_answer}")

    def show_custom_message(self, title, message):
        """
        Shows a custom popup message at the same coordinates as the main window.
        Args:
            title (str): The title of the popup window.
            message (str): The message to display.
        """
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        # Create a new top-level window
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry(f"+{x+80}+{y+80}")  # Offset a bit so it's not exactly overlapping
        popup.transient(self.root)
        popup.grab_set()
        popup.resizable(False, False)

        label = tk.Label(popup, text=message, font=("Arial", 12), padx=20, pady=20)
        label.pack()

        ok_button = tk.Button(popup, text="OK", width=10, command=popup.destroy)
        ok_button.pack(pady=(0, 10))

        # Make sure the popup is on top
        popup.attributes('-topmost', True)
        popup.focus_force()

    def on_option_selected(self, *args):
        """
        Callback for when a radio button is selected.
        Enables the Check button only if an option is selected.
        """
        if self.selected_option.get():
            self.check_button.config(state="normal")
        else:
            self.check_button.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    # Create the QuizUI instance
    app = QuizUI(root)
    # Start the Tkinter event loop
    root.mainloop()