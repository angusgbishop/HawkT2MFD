from tkinter import *
from functions import *
import math


class background:
    def __init__(self, parent):
        background_frame = Frame(parent, bd=0, bg="red", height=600, width=800)
        background_frame.pack()
        self.background_canvas = Canvas(background_frame, bg="black", height=550, width=550, bd=0)
        self.background_canvas.pack()
        self.current_page = standybyPage

        self.OBS_dict = {}
        self.border_offset = 10
        self.line_length = 25

        self.midpoint = (self.background_canvas.winfo_reqwidth() / 2, self.background_canvas.winfo_reqheight() / 2)

        self.screen_canvas_height = self.background_canvas.winfo_reqheight() - 2 * (
            2 * self.border_offset + self.line_length)
        self.screen_canvas_width = self.background_canvas.winfo_reqwidth() - 2 * (
            2 * self.border_offset + self.line_length)

    def create_button_guide(self, button_number, inp_text):
        screen = self.background_canvas
        y_guide_spacing = screen.winfo_reqwidth() / 6
        x_guide_spacing = screen.winfo_reqheight() / 6
        bar_loc = get_units(button_number)
        y_bar_loc = get_units(button_number - 5)

        line_length = self.line_length
        x_line_offset = 0
        y_line_offset = screen.winfo_reqwidth() - (2 * self.border_offset + line_length)

        if get_tens(button_number) != 0:
            x_line_offset = screen.winfo_reqheight() - (2 * self.border_offset + line_length)
            y_line_offset = 0

        if button_number in (1, 2, 3, 4, 5, 11, 12, 13, 14, 15):
            x_pos0 = ((bar_loc * x_guide_spacing) - x_guide_spacing / 2)
            x_pos1 = x_pos0
            y_pos0 = self.border_offset + x_line_offset
            y_pos1 = y_pos0 + line_length

            line1 = screen.create_line(x_pos0, y_pos0, x_pos1, y_pos1, fill="white", width=4)
            line2 = screen.create_line(x_pos0 + x_guide_spacing, y_pos0, x_pos1 + x_guide_spacing, y_pos1, fill="white",
                                       width=4)

            midpoint = ((x_pos0 + x_guide_spacing / 2), (y_pos0 + y_pos1) / 2)
            text = screen.create_text(midpoint, text=inp_text, fill="white")
        else:
            x_pos0 = self.border_offset + y_line_offset
            x_pos1 = x_pos0 + line_length
            y_pos0 = (((y_bar_loc) * y_guide_spacing) - y_guide_spacing / 2)
            y_pos1 = y_pos0

            line1 = screen.create_line(x_pos0, y_pos0, x_pos1, y_pos1, fill="white", width=4)
            line2 = screen.create_line(x_pos0, y_pos0 + y_guide_spacing, x_pos1, y_pos1 + y_guide_spacing, fill="white",
                                       width=4)

            midpoint = ((x_pos0 + x_pos1) / 2, (y_pos0 + y_guide_spacing / 2))
            text = screen.create_text(midpoint, text=inp_text, fill="white")

        self.OBS_dict[button_number] = (text, line1, line2)

        return (text, line1, line2)

    def clear_canvas(self):

        for x in self.OBS_dict.items():
            self.background_canvas.delete(x)

    def change_page(self, window_class):

        self.current_page = window_class(self)


class mfdPage():
    def __init__(self, master, button_dict, **kwargs):
        master.clear_canvas()
        self.active_buttons = {}
        self.updatable_widgets = {}
        self.updatable_widget_ids = {}

        for x, y in button_dict.items():  # Create all buttons on init
            self.active_buttons[x] = y
            master.create_button_guide(x, y)

        self.screen = Canvas(bg="black", bd=0, height=master.screen_canvas_height, width=master.screen_canvas_width,
                             highlightthickness=0)
        self.screen_id = master.background_canvas.create_window(master.midpoint, window=self.screen)

        self.midpoint = (self.screen.winfo_reqwidth() / 2, self.screen.winfo_reqheight() / 2)

    def relx(self, ratio):
        relx = self.midpoint[0] + (self.screen.winfo_reqwidth() * (ratio - 0.5))

        return relx

    def rely(self, ratio):
        rely = self.midpoint[1] + (self.screen.winfo_reqheight() * (ratio - 0.5))

        return rely

    def register_updatable_widget(self, widget, *args):
        id = len(self.updatable_widgets)
        self.updatable_widgets[id] = args
        self.updatable_widget_ids[id] = widget


#
#   PAGES BELOW THIS LINE
#

class standybyPage(mfdPage):
    def __init__(self, master):
        mfdPage.__init__(self, master, {})


class elevPage(mfdPage):
    def __init__(self, master):
        active_buttons = {11: "MAP", 12: "HSI", 13: "DCRS", 15: "RWI"}
        mfdPage.__init__(self, master, active_buttons)
        attitudeIndicator(self, (self.relx(0.55), self.rely(0.55)), ('pitch', 'roll', 'hdg'))


class enginePage(mfdPage):
    def __init__(self, master):
        active_buttons = {11: "MAP", 12: "HSI", 13: "ADI", 14: "", 16: "DISP"}
        mfdPage.__init__(self, master, active_buttons)
        rotaryDial(self, (self.relx(0.25), self.rely(0.75)), "engine_rpm_percentage", unit_text="% RPM", )
        rotaryDial(self, (self.relx(0.75), self.rely(0.75)), 'egt', unit_text="°C TGT")
        updateableTextbox(self, (self.relx(0.4), self.rely(0.15)), 'port_fuel', boxed=True)
        updateableTextbox(self, (self.relx(0.7), self.rely(0.15)), 'stbd_fuel', boxed=True)
        updateableTextbox(self, (self.relx(0.55), self.rely(0.32)), 'total_fuel', boxed=True)
        updateableTextbox(self, (self.relx(0.8), self.rely(0.35)), 'fuel_flow', boxed=True)
        self.screen.create_line(self.relx(0), self.rely(0.5), self.relx(1), self.rely(0.5), fill="white", width=3)
        self.screen.create_text((self.relx(0.55), self.rely(0.37)), text="TOTAL", fill="green")
        self.screen.create_text((self.relx(0.7), self.rely(0.35)), text="F/F", fill="green")
        self.screen.create_text((self.relx(0.93), self.rely(0.35)), text="LBS/MIN", fill="green")
        self.screen.create_text((self.relx(0.4), self.rely(0.2)), text="PORT", fill="green")
        self.screen.create_text((self.relx(0.7), self.rely(0.2)), text="STBD", fill="green")
        self.screen.create_text((self.relx(0.55), self.rely(0.08)), text="FUEL CONTENTS LBS", fill="green")


class storesPage(mfdPage):
    def __init__(self, master):
        active_buttons = {1: "AIM", 2: "BFF", 3: "GUN"}
        mfdPage.__init__(self, master, active_buttons)


#
#   CUSTOM WIDGETS BELOW THIS LINE
#

class rotaryDial():
    def __init__(self, master, coord, import_vars, **kwargs):

        ratio = 0
        # Default values
        self.params = {}
        self.params["width"] = 180
        self.params["height"] = 180
        self.params["bar_color"] = "light green"
        self.params["outline_color"] = "light grey"
        self.params["redline"] = -1
        self.params["value_text"] = ratio * 100
        self.params["import_vars"] = import_vars
        self.params["unit_text"] = "%"
        self.params["bar_width"] = 10
        self.params["outline_width"] = 1.5
        value_extent = -270 * ratio

        # Custom values
        if kwargs is not None:
            for arg, val in kwargs.items():
                self.params[arg] = val

        # Create Subcanvas and give it a midpoint
        sub_canvas = Canvas(bg="black", width=self.params["width"], height=self.params["height"], highlightthickness=0)
        master.screen.create_window(coord, window=sub_canvas, anchor="center")
        midpoint = (sub_canvas.winfo_reqwidth() / 2, sub_canvas.winfo_reqheight() / 2)

        self.sub_canvas = sub_canvas

        # Draw dial
        coord = self.params["bar_width"], self.params["bar_width"], sub_canvas.winfo_reqwidth() - self.params[
            "bar_width"], sub_canvas.winfo_reqheight() - self.params["bar_width"]
        sub_canvas.create_arc(coord, start=-133, extent=-274, outline=self.params["outline_color"], style="arc",
                              width=self.params["bar_width"] + 2 * self.params["outline_width"])
        sub_canvas.create_arc(coord, start=-135, extent=-270, outline="black", style="arc",
                              width=self.params["bar_width"] - 1)
        self.value_dial_id = sub_canvas.create_arc(coord, start=-135, extent=value_extent,
                                                   outline=self.params["bar_color"], style="arc",
                                                   width=self.params["bar_width"])

        # Create text items
        self.value_text_id = sub_canvas.create_text((midpoint[0], midpoint[1] - 20), text=self.params["value_text"],
                                                    fill="green")
        sub_canvas.create_text((midpoint[0], midpoint[1] + 15), text=self.params["unit_text"], fill="green")

        master.register_updatable_widget(self, self.params["import_vars"])

    def update(self, vars, **kwargs):
        percentage = float(vars.get(self.params["import_vars"]))
        myExtent = self.get_extent(percentage)
        self.params["value_text"] = percentage
        self.sub_canvas.itemconfig(self.value_dial_id, extent=myExtent)
        self.sub_canvas.itemconfig(self.value_text_id, text=int(percentage * 100))

    def get_extent(self, percentage):
        return -270 * percentage


class updateableTextbox():
    def __init__(self, master, coord, update_variable, **kwargs):

        self.params = {}
        self.params["width"] = 50
        self.params["height"] = 20
        self.params["color"] = "white"
        self.params["disp_text"] = 'NaN'
        self.params["update_variable"] = update_variable
        self.params["boxed"] = False

        # Custom values
        if kwargs is not None:
            for arg, val in kwargs.items():
                self.params[arg] = val

        self.sub_canvas = Canvas(bg="black", width=self.params["width"], height=self.params["height"],
                                 highlightthickness=2)
        master.screen.create_window(coord, window=self.sub_canvas, anchor="center")
        midpoint = (self.sub_canvas.winfo_reqwidth() / 2, self.sub_canvas.winfo_reqheight() / 2)

        self.text_id = self.sub_canvas.create_text((midpoint[0], midpoint[1]), text=self.params["disp_text"],
                                                   fill=self.params["color"], justify="right")

        master.register_updatable_widget(self, self.params["update_variable"])

    def update(self, vars, **kwargs):
        self.params["disp_text"] = vars.get(self.params["update_variable"])
        self.sub_canvas.itemconfig(self.text_id, text=self.params["disp_text"])
        self.box_update()

    def box_update(self):
        update_decider = self.params["boxed"]
        if update_decider:
            self.sub_canvas.highlightthickness = 0
        else:
            self.sub_canvas.highlightthickness = 2


class attitudeIndicator():
    def __init__(self, master, coord, update_variable, **kwargs):

        self.params = {}
        self.params["width"] = master.relx(0.9)
        self.params["height"] = master.rely(0.9)
        self.params["color"] = "white"
        self.params["disp_text"] = 'NaN'
        self.params["update_variable"] = update_variable
        self.params["angleLines"] = {}
        self.params["angleText"] = {}
        self.params["headingLines"] = {}
        self.params["hdg_text"] = {}
        self.params["pitch_range"] = 45
        self.params["hdg_range"] = 35

        # Custom values
        if kwargs is not None:
            for arg, val in kwargs.items():
                self.params[arg] = val

        self.sub_canvas = Canvas(bg="black", width=self.params["width"], height=self.params["height"],
                                 highlightthickness=0)
        master.screen.create_window(coord, window=self.sub_canvas, anchor="center")
        midpoint = (self.sub_canvas.winfo_reqwidth() / 2, self.sub_canvas.winfo_reqheight() / 2)
        self.midpoint = midpoint

        self.radii = ((self.params["height"] - 150) / 2)

        bounding_box = (
            midpoint[0] - self.radii, midpoint[1] - self.radii,
            midpoint[0] + self.radii, midpoint[1] + self.radii)



        self.sub_canvas.create_oval(bounding_box, fill="#F2BF18", outline="white", width=5)
        self.sky = self.sub_canvas.create_arc(bounding_box, fill="#1873F2", outline="white", style=CHORD, width=3)

        self.create_pitch_lines()
        self.create_heading_lines()

        self.sub_canvas.create_rectangle((midpoint[0] - 5, midpoint[1] - 5, midpoint[0] + 5, midpoint[1] + 5),
                                         outline="black")
        self.sub_canvas.create_line(midpoint[0] - 100, midpoint[1], midpoint[0] - 30, midpoint[1], midpoint[0] - 30,
                                    midpoint[1] + 30, fill="black")
        self.sub_canvas.create_line(midpoint[0] + 100, midpoint[1], midpoint[0] + 30, midpoint[1], midpoint[0] + 30,
                                    midpoint[1] + 30, fill="black")

        for each in self.params["update_variable"]:
            master.register_updatable_widget(self, self.params["update_variable"])

    def update(self, vars, **kwargs):
        sky_vals = self.get_chord_start(vars["pitch"], vars["roll"])
        self.sub_canvas.itemconfig(self.sky, start=sky_vals[0], extent=sky_vals[1])
        self.update_angle_lines(vars["pitch"], vars["roll"])
        self.update_heading_lines(vars["hdg"])

    def get_chord_start(self, pitch, roll):
        pitch_range = self.params["pitch_range"]
        roll += 180  # Flip sky

        if abs(pitch) < pitch_range:
            roll_midline = roll - 90
            start = degrees(acos(-pitch / pitch_range)) + roll_midline
            extent = -2 * (start - roll_midline)
            return (start, extent)
        elif pitch >= pitch_range:
            return (0, -359.99)
        elif pitch < pitch_range:
            return (0, 0)

    def get_horizon_midpoint(self, pitch, roll):
        mid_delta = pol2cart(self.radii * (pitch / self.params["pitch_range"]), 180 - roll)
        mid = (self.midpoint[0] + mid_delta[0], self.midpoint[1] + mid_delta[1])
        return mid

    def create_pitch_lines(self):
        for each in range(-90, 90):
            if each % 10 == 0:
                self.params["angleLines"][each] = self.sub_canvas.create_line((0, 0, 0, 0),
                                                                              width=2, fill="white")
            elif each % 5 == 0:
                self.params["angleLines"][each] = self.sub_canvas.create_line((0, 0, 0, 0),
                                                                              width=2, fill="white")
            else:
                pass

    def update_angle_lines(self, pitch, roll):
        # Refresh or create the pitch and roll angle lines
        angleLines = self.params["angleLines"]
        horiz = self.get_horizon_midpoint(pitch, roll + 90)
        for lineIncrement, id in angleLines.items():
            if self.params["pitch_range"] * 0.95 - pitch > lineIncrement > -self.params["pitch_range"] * 0.95 - pitch:  # If the line can be displayed on screen

                self.sub_canvas.itemconfig(id, fill="white")

                if lineIncrement % 10 == 0:
                    pitch_line_length = 50
                else:
                    pitch_line_length = 20

                line_offset = pol2cart(self.radii * (lineIncrement / self.params["pitch_range"]), 90 - roll)

                midx = line_offset[0] + horiz[0]
                midy = line_offset[1] + horiz[1]

                self.sub_canvas.coords(id, line_coords(pitch_line_length, (midx, midy), -roll))
                # print("Adjusting the %s pitch line"%lineIncrement)
                pass
            else:
                # "Switch off" the bar
                self.sub_canvas.itemconfigure(id, fill="")
                pass
        return

    def create_heading_lines(self):
        for each in range(0, 360):
            if each % 30 == 0:
                self.params["headingLines"][each] = self.sub_canvas.create_line((0, 0, 0, 0),
                                                                                width=3, fill="white")

                self.params["hdg_text"][each] = self.sub_canvas.create_text((0, 0), text=str(each),fill="white",font=("Helvetica", 10,"bold"))
            elif each % 5 == 0:
                self.params["headingLines"][each] = self.sub_canvas.create_line((0, 0, 0, 0),
                                                                                width=2, fill="white")
            else:
                pass

    def update_heading_lines(self, hdg):
        heading_lines = self.params["headingLines"]

        for headingVal, id  in heading_lines.items():
            if (hdg + self.params["hdg_range"]) > headingVal > (hdg - self.params["hdg_range"]):
                self.sub_canvas.itemconfig(id, fill="light green")

                hdg_angle = headingVal - hdg

                if headingVal % 30 == 0:
                    line_length = 25
                    text_id = self.params["hdg_text"][headingVal]
                    text_offset = pol2cart(self.radii + 22, (hdg_angle * 2) - 90)
                    self.sub_canvas.itemconfigure(text_id, fill="light green")
                    self.sub_canvas.coords(text_id,(self.midpoint[0]+text_offset[0],self.midpoint[1]+text_offset[1]))
                elif headingVal % 10 == 0:
                    line_length = 17
                else:
                    line_length = 12


                self.sub_canvas.coords(id, radius_line_coords(self.midpoint,self.radii+60,(hdg_angle*2)-90,line_length))

            else:
                self.sub_canvas.itemconfigure(id, fill="")
                try:
                    self.sub_canvas.itemconfigure(self.params["hdg_text"][headingVal],fill="")
                    pass
                except:
                    pass
                pass