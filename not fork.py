import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class TextColorDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, title="Select Color", transient_for=parent, flags=0)
        self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK, Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)

        self.color_chooser = Gtk.ColorChooserWidget()
        self.get_content_area().add(self.color_chooser)
        self.show_all()

class BugsDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, title="Known Bugs", transient_for=parent, flags=0)
        self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)

        label = Gtk.Label(label="Known Issue: You can only set the text color once per launch.")
        box = self.get_content_area()
        box.add(label)
        self.show_all()

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Not Fork")
        self.set_border_width(10)
        self.set_default_size(400, 200)

        # Create a TextView for displaying content
        self.textview = Gtk.TextView()
        self.textview.set_editable(False)  # Make the TextView not editable
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text("Not fork is a forkie in collabvm. he keeps rm - rf ing vms. he got banned from lubuntuvm by guest24897")

        # Scrollable window for the TextView
        scrollable_tview = Gtk.ScrolledWindow()
        scrollable_tview.set_vexpand(True)
        scrollable_tview.add(self.textview)

        # VBox to hold menu and TextView
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        # Menu Bar
        menubar = Gtk.MenuBar()
        file_menu = Gtk.Menu()
        file_item = Gtk.MenuItem(label="File")
        file_item.set_submenu(file_menu)
        
        # Close menu item
        close_item = Gtk.MenuItem(label="Close")
        close_item.connect("activate", self.close_app)
        file_menu.append(close_item)

        # Tools Menu
        tools_menu = Gtk.Menu()
        tools_item = Gtk.MenuItem(label="Tools")
        tools_item.set_submenu(tools_menu)
        
        # Text Color menu item
        text_color_item = Gtk.MenuItem(label="Text Color")
        text_color_item.connect("activate", self.open_color_dialog)
        tools_menu.append(text_color_item)

        # Bugs menu item
        bugs_item = Gtk.MenuItem(label="Bugs")
        bugs_item.connect("activate", self.open_bugs_dialog)
        tools_menu.append(bugs_item)

        menubar.append(file_item)
        menubar.append(tools_item)

        vbox.pack_start(menubar, False, False, 0)
        vbox.pack_start(scrollable_tview, True, True, 0)

    def close_app(self, widget):
        self.close()

    def open_color_dialog(self, widget):
        dialog = TextColorDialog(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            color = dialog.color_chooser.get_rgba()
            text_tag = self.textbuffer.create_tag("colored_text", foreground_rgba=color)
            start_iter = self.textbuffer.get_start_iter()
            end_iter = self.textbuffer.get_end_iter()
            self.textbuffer.apply_tag(text_tag, start_iter, end_iter)

        dialog.destroy()

    def open_bugs_dialog(self, widget):
        dialog = BugsDialog(self)
        dialog.run()
        dialog.destroy()

win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
