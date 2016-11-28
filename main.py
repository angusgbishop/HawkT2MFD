from classes import *
from data_grabber import *
from time import *

def run(root,mybackground):
    time_var = time()
    fps_counter = 0
    while True:
        root.update_idletasks()
        root.update()
        widget_updater(mybackground)

        fps_counter += 1
        if time() - time_var > 1:
            print("The MFD is running at %s FPS"%fps_counter)
            fps_counter=0
            time_var=time()

    return

def widget_updater(mybackground):
    # Updates all updatable widgets on the currently displayed page.
    # Find all updatable widgets and their requested variables

    widget_variable_dict = mybackground.current_page.updatable_widgets
    widget_data = {}
    for id, vars in widget_variable_dict.items():
        if type(vars) is tuple:
            for each in vars:
                vars = get_var(each)
        else:
            vars = get_var(vars)
        if vars is None:
            return
        widget_data[id] = vars

    for widget_id , data in widget_data.items():  # Call widgets update function with data
        widget = mybackground.current_page.updatable_widget_ids[widget_id]
        widget.update(data)

def main():
    root = Tk()
    root.title("Hawk MFD Manager")
    mybackground = background(root)
    mybackground.change_page(enginePage)
    run(root,mybackground)
    #root.mainloop()

if __name__ == "__main__":
    main()
