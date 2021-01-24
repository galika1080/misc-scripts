import gi
import time

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject, Gdk

class TimePanel(Gtk.Window):
    bar = None
    timelabel = None
    tasklabel = None

    paused = True

    time_task_started = 0
    time_elapsed = 0
    time_target = 0

    tasks = []
    task_idx = -1

    def __init__(self):
        Gtk.Window.__init__(self, title="pomodoro")

        grid = Gtk.Grid(row_spacing=6, column_spacing=6)
        self.add(grid)

        self.bar = Gtk.LevelBar()
        self.timelabel = Gtk.Label()
        self.tasklabel = Gtk.Label()

        b_done = Gtk.Button(label="done")
        b_done.connect("clicked", self.c_done)

        b_start = Gtk.Button(label="start")
        b_start.connect("clicked", self.c_start)

        b_pause = Gtk.Button(label="pause")
        b_pause.connect("clicked", self.c_pause)

        grid.add(b_done)
        grid.add(b_start)
        grid.add(b_pause)
        grid.attach_next_to(self.bar, b_done, Gtk.PositionType.TOP, 3, 1)
        grid.attach_next_to(self.timelabel, self.bar, Gtk.PositionType.TOP, 3, 1)
        grid.attach_next_to(self.tasklabel, self.timelabel, Gtk.PositionType.TOP, 3, 1)


        hb = Gtk.HeaderBar() 
        hb.set_show_close_button(True) 
        hb.props.title = ""
        hb.set_has_subtitle(False)

        self.set_titlebar(hb) 


        self.read_stuff()
        self.c_done(None)
    
    def read_stuff(self):
        taskfile = open('todo', 'r') 
        lines = taskfile.readlines()

        for line in lines:
            if line[0] == '#':
                continue

            words = line.split()

            time_str = words[len(words) - 1]
            taskname = line[:len(line) - len(time_str) - 1].rstrip()

            time = ...
            try:
                time = int(time_str)*60
            except ValueError:
                time = 0
                taskname = line.rstrip()
            
            tup = (taskname, time)
            self.tasks.append(tup)
        
        self.tasks.append(("you're done!", 0))

    def update_time(self):
        if not self.paused:
            self.time_elapsed = time.time() - self.time_task_started
        
        self.timelabel.set_label(time.strftime("%M:%S", time.gmtime(self.time_elapsed)) + "/" + time.strftime("%M:%S", time.gmtime(self.time_target)))

        if self.time_target != 0:
            ratio = self.time_elapsed / self.time_target

            if ratio > 1:
                self.modify_bg(Gtk.StateType.NORMAL, Gdk.Color(50000, 0, 0))
            elif ratio > 0.75:
                self.modify_bg(Gtk.StateType.NORMAL, Gdk.Color(65535, 40000, 0))
            elif ratio > 0.5:
                self.modify_bg(Gtk.StateType.NORMAL, Gdk.Color(65535, 65535, 0))
            else:
                self.modify_bg(Gtk.StateType.NORMAL, Gdk.Color(10000, 30000, 5000))

            self.bar.set_value(min(ratio, 1))
        else:
            self.modify_bg(Gtk.StateType.NORMAL, Gdk.Color(60000, 60000, 60000))
            self.bar.set_value(0)

        GObject.timeout_add(10, self.update_time)

    def c_done(self, widget):
        print("done")
        self.time_task_started = time.time()
        self.time_elapsed = 0
        self.bar.set_value(0)

        self.task_idx += 1
        if self.task_idx < len(self.tasks):
            task = self.tasks[self.task_idx]

            self.tasklabel.set_label(task[0])
            self.time_target = task[1]
    
    def c_start(self, widget):
        print("start")

        self.time_task_started = time.time() - self.time_elapsed
        self.paused = False
    
    def c_pause(self, widget):
        print("pause")
        self.paused = True

win = TimePanel()
win.connect("destroy", Gtk.main_quit)
win.show_all()
#win.get_window().set_decorations(Gdk.WMDecoration.BORDER)
win.update_time()
Gtk.main()