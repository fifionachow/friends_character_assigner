import os
import random
import sys

from PIL import ImageTk,Image
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

import friends
from friends import friends_generator as fg

code_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(code_dir)

print(f"Code dir: {code_dir}")
print(f"Project dir: {project_root}")

TO_CLEAR = False
output_widget = None

global process_widgets
process_widgets = {}

INPUT_ARGUMENTS = {
    "Player names (separated by comma)": {"widget_type": "entry", "options":{"default_value": "jim,james,julie,janet,joe"}},
    "Seasons to exclude (separated by comma)": {"widget_type": "entry", "options":{"default_value": "1-2,9,10"}},
    "Random integer": {"widget_type": "entry", "options":{"default_value": "30"}},
    "Pick characters": {"widget_type": "checkbutton"},
    "Pick starting episode": {"widget_type": "checkbutton"},
}

def warn_input_error(msg):
    showinfo("Error", message = msg)

def process_inputs(input_widgets):
    global TO_CLEAR

    inputs = {entry_name: input_widget.get() for entry_name, input_widget in input_widgets.items()}

    if TO_CLEAR:
        output_widget.delete("1.0","end")
 
    # selection done here
    random.seed(int(inputs['Random integer']))

    players = inputs["Player names (separated by comma)"].split(",")

    pick_inputs = [inputs[input_arg] for input_arg in inputs if input_arg.startswith('Pick')]

    if all(map(lambda x: x is False, pick_inputs)):
        warn_input_error('All toggles off - Must pick either players, episode or all')

    if inputs["Pick starting episode"] or all(pick_inputs):
        seasons = inputs["Seasons to exclude (separated by comma)"].split(",")
        season_episode = fg.select_episode(seasons)
        output_widget.insert(tk.END, season_episode)

    if inputs["Pick characters"] or all(pick_inputs):
        player_character_watch = fg.select_characters(players)
        output_widget.insert(tk.END, "\n"+player_character_watch)
    
    TO_CLEAR = True

def build_entry(window, entry_name, entry_options):
    configs = {
        "width": 20,
        "borderwidth": 1
    }

    if "default_value" in entry_options:
        configs['textvariable'] = tk.StringVar(window, entry_options['default_value'])

    target_entry = tk.Entry(window, **configs)
    process_widgets[entry_name] = target_entry
    return target_entry

def build_label(window, entry_name):
    return tk.Label(window, text=entry_name)

def build_checkbutton(window, entry_name):
    target_var = tk.IntVar() 
    target_check = tk.Checkbutton(window, text=entry_name, variable=target_var)
    process_widgets[entry_name] = target_var
    return target_check

def main():
    window = tk.Tk()
    window.title("Friends TV Show Drinking Game")
    canvas1 = tk.Canvas(window, width = 180, height = 300)

    RESCALE = 0.3
    image = Image.open(os.path.join(project_root, "assets/friends3.jpg"))
    resize_from_scale = map(lambda x: int(x*RESCALE), image.size)
    image = image.resize(resize_from_scale, Image.ANTIALIAS)
    application_image = ImageTk.PhotoImage(image)
    image_label = tk.Label(canvas1, image=application_image)
    image_label.image = application_image
    image_label.grid(row=0, column=0, sticky=tk.N, columnspan=3)

    row_num = 1

    for input_arg, input_values in INPUT_ARGUMENTS.items():
        if input_values['widget_type'] == 'entry':
            build_label(canvas1, input_arg).grid(row=row_num, column=0, sticky=tk.W)
            build_entry(canvas1, input_arg, input_values['options']).grid(row=row_num, column=1, sticky=tk.W)
            column = 0
        elif input_values['widget_type'] == 'checkbutton':
            build_checkbutton(canvas1, input_arg).grid(row=row_num, column=0, sticky=tk.W)
        else:
            print("Cannot build. Not entry or checkbutton")
        row_num += 1

    build_label(canvas1, 'Results:').grid(row=row_num+3, column=0, sticky=tk.NW)

    global output_widget
    output_widget = tk.Text(canvas1, background="#D3D3D3", relief=tk.RIDGE)
    output_widget.grid(row=row_num+4, column=0, columnspan=3)

    tk.Button(canvas1, text="Generate", command=(lambda: process_inputs(process_widgets))).grid(row=row_num, column=0, columnspan=3)

    canvas1.pack(anchor=tk.W)

    window.mainloop()

if __name__ == "__main__":
    main()