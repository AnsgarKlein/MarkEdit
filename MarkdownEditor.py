#!/usr/bin/env python2

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

print "Trying to import markdown ...",
try:
    import markdown
    print "\t\t\t\tDONE"
except:
    print "\t\t\t\tERROR"
    sys.exit(1)

print "Trying to import Gdk from gi.repository ...",
try:
    from gi.repository import Gdk
    print "\t\tDONE"
except:
    print "\t\tERROR"
    sys.exit(1)

print "Trying to import Gtk from gi.repository ...",
try:
    from gi.repository import Gtk
    print "\t\tDONE"
except:
    print "\t\tERROR"
    sys.exit(1)

print "Trying to import GtkSource from gi.repository ...",
try:
    from gi.repository import GtkSource
    print "\tDONE"
except:
    print "\tERROR"
    sys.exit(1)

print "Trying to import WebKit from gi.repository ...",
try:
    from gi.repository import WebKit
    print "\t\tDONE"
except:
    print "\t\tERROR"
    sys.exit(1)

N_OPEN_WINDOWS = 0

class MyWindow(Gtk.Window):
    def __init__(self):
        global N_OPEN_WINDOWS
        N_OPEN_WINDOWS = N_OPEN_WINDOWS+1
        
        self.is_fullscreen = False
        self.file_path = None
        
        self.build_gui()
        self.show_all()
        
    def build_gui(self):
        Gtk.Window.__init__(self, title="MarkEdit")
        self.connect("delete-event", lambda a, b: self.exit_window())
        self.connect("window-state-event", self.on_window_state_change)
        self.set_default_size(1000,750)
        
        #Set application icon
        try:
            self.set_icon(Gtk.IconTheme.get_default().load_icon("text-editor", 256, 0))
        except:
            try:
                self.set_icon(Gtk.IconTheme.get_default().load_icon("application-x-executable", 256, 0))
            except:
                pass
        
        #create main box
        self.main_box = Gtk.Box()
        self.main_box.set_orientation(Gtk.Orientation.VERTICAL)
        self.add(self.main_box)
        
        #Create menu bar
        self.menu_accel = Gtk.AccelGroup()
        self.add_accel_group(self.menu_accel)
        
        # --- "File" item
        self.menu1 = Gtk.Menu()
        
        self.menuitem1_1 = Gtk.MenuItem.new_with_mnemonic("_New")
        self.menuitem1_1.connect("activate", lambda a: self.open_new_window())
        self.menuitem1_1.add_accelerator("activate",
                                         self.menu_accel,
                                         Gdk.keyval_from_name("N"),
                                         Gdk.ModifierType.CONTROL_MASK,
                                         Gtk.AccelFlags.VISIBLE)
        self.menu1.add(self.menuitem1_1)
        
        self.menuitem1_2 = Gtk.MenuItem.new_with_mnemonic("_Open")
        self.menuitem1_2.connect("activate", lambda a: self.open_file())
        self.menuitem1_2.add_accelerator("activate",
                                         self.menu_accel,
                                         Gdk.keyval_from_name("O"),
                                         Gdk.ModifierType.CONTROL_MASK,
                                         Gtk.AccelFlags.VISIBLE)
        self.menu1.add(self.menuitem1_2)
        
        self.menuitem1_3 = Gtk.MenuItem.new_with_mnemonic("_Save")
        self.menuitem1_3.connect("activate", lambda a: self.save_file(False))
        self.menuitem1_3.add_accelerator("activate",
                                         self.menu_accel,
                                         Gdk.keyval_from_name("S"),
                                         Gdk.ModifierType.CONTROL_MASK,
                                         Gtk.AccelFlags.VISIBLE)
        self.menu1.add(self.menuitem1_3)
        
        self.menuitem1_4 = Gtk.MenuItem.new_with_mnemonic("Save _As")
        self.menuitem1_4.connect("activate", lambda a: self.save_file(True))
        self.menuitem1_4.add_accelerator("activate",
                         self.menu_accel,
                         Gdk.keyval_from_name("S"),
                         (Gdk.ModifierType.CONTROL_MASK|Gdk.ModifierType.SHIFT_MASK),
                         Gtk.AccelFlags.VISIBLE)
        self.menu1.add(self.menuitem1_4)
        
        self.menuitem1_5 = Gtk.MenuItem.new_with_mnemonic("_Quit")
        self.menuitem1_5.connect("activate", lambda a: self.exit_window())
        self.menuitem1_5.add_accelerator("activate",
                                 self.menu_accel,
                                 Gdk.keyval_from_name("W"),
                                 Gdk.ModifierType.CONTROL_MASK,
                                 Gtk.AccelFlags.VISIBLE)
        self.menu1.add(self.menuitem1_5)
        
        self.menuitem1 = Gtk.MenuItem.new_with_mnemonic("_File")
        self.menuitem1.set_submenu(self.menu1)
        
        # --- "Edit" item
        self.menu2 = Gtk.Menu()
        
        self.menuitem2_1 = Gtk.MenuItem.new_with_mnemonic("_Undo")
        self.menuitem2_1.connect("activate", lambda a: self.undo())
        self.menuitem2_1.add_accelerator("activate",
                                 self.menu_accel,
                                 Gdk.keyval_from_name("Z"),
                                 Gdk.ModifierType.CONTROL_MASK,
                                 Gtk.AccelFlags.VISIBLE)
        self.menu2.add(self.menuitem2_1)
        
        self.menuitem2_2 = Gtk.MenuItem.new_with_mnemonic("_Redo")
        self.menuitem2_2.connect("activate", lambda a: self.redo())
        self.menuitem2_2.add_accelerator("activate",
                 self.menu_accel,
                 Gdk.keyval_from_name("Z"),
                 (Gdk.ModifierType.CONTROL_MASK|Gdk.ModifierType.SHIFT_MASK),
                 Gtk.AccelFlags.VISIBLE)
        self.menu2.add(self.menuitem2_2)
        
        self.menuitem2_3 = Gtk.MenuItem.new_with_mnemonic("Pr_eferences")
        self.menu2.add(self.menuitem2_3)
        
        self.menuitem2 = Gtk.MenuItem.new_with_mnemonic("_Edit")
        self.menuitem2.set_submenu(self.menu2)
        
        # --- "Help" item
        self.menu3 = Gtk.Menu()
        self.menuitem3_1 = Gtk.MenuItem.new_with_mnemonic("_About")
        self.menuitem3_1.connect("activate", lambda a: self.show_about_dialog())
        self.menu3.add(self.menuitem3_1)
        
        self.menuitem3 = Gtk.MenuItem.new_with_mnemonic("_Help")
        self.menuitem3.set_submenu(self.menu3)
        
        self.menubar = Gtk.MenuBar()
        self.menubar.add(self.menuitem1)
        self.menubar.add(self.menuitem2)
        self.menubar.add(self.menuitem3)
        self.main_box.add(self.menubar)
        
        #Create toolbar
        self.toolbar = Gtk.Toolbar()
        self.toolbar.get_style_context().add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)
        self.main_box.add(self.toolbar)
        
        self.new_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_NEW)
        self.new_button.connect("clicked", lambda a: self.open_new_window())
        self.toolbar.add(self.new_button)
        
        self.open_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_OPEN)
        self.open_button.connect("clicked", lambda a: self.open_file())
        self.toolbar.add(self.open_button)
        
        self.save_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_SAVE)
        self.save_button.connect("clicked", lambda a: self.save_file(False))
        self.toolbar.add(self.save_button)
        
        self.toolbar.add(Gtk.SeparatorToolItem())
        
        self.undo_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_UNDO)
        self.undo_button.set_sensitive(False)
        self.undo_button.connect("clicked", lambda a: self.undo())
        self.toolbar.add(self.undo_button)
        
        self.redo_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_REDO)
        self.redo_button.set_sensitive(False)
        self.redo_button.connect("clicked", lambda a: self.redo())
        self.toolbar.add(self.redo_button)
        
        self.toolbar.add(Gtk.SeparatorToolItem())
        
        self.cut_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_CUT)
        self.toolbar.add(self.cut_button)
        
        self.copy_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_COPY)
        self.toolbar.add(self.copy_button)
        
        self.paste_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_PASTE)
        self.toolbar.add(self.paste_button)
        
        self.toolbar.add(Gtk.SeparatorToolItem())
        
        self.fullscreen_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_FULLSCREEN)
        self.fullscreen_button.connect("clicked", lambda a: self.toggle_fullscreen())
        self.toolbar.add(self.fullscreen_button)
        
        
        #Create all three text views
        self.text_box = Gtk.Box()
        self.text_box.set_homogeneous(True)
        self.main_box.add(self.text_box)
        
        #Create markdown text view
        self.md_text_language = GtkSource.LanguageManager.get_default().get_language("markdown")
        self.md_text_buffer = GtkSource.Buffer.new_with_language(self.md_text_language)
        self.md_text_undoer = self.md_text_buffer.get_undo_manager()
        self.md_text_undoer.connect("can_redo_changed",
                                    lambda a: self.on_can_undoredo_changed())
        self.md_text_undoer.connect("can_undo_changed",
                                    lambda a: self.on_can_undoredo_changed())
        self.md_text = GtkSource.View.new_with_buffer(self.md_text_buffer)
        self.md_text.set_hexpand(True)
        self.md_text.set_vexpand(True)
        self.md_text.set_editable(True)
        self.md_text.get_buffer().connect("changed", self.md_text_changed)
        self.md_text.set_wrap_mode(Gtk.WrapMode.WORD)
        self.md_text_scroll = Gtk.ScrolledWindow()
        self.md_text_scroll.add(self.md_text)
        self.text_box.pack_start(self.md_text_scroll, True, True, 0)
        
        #Create Gtk.Notebook to switch between html text and rendered html
        self.html_switcher = Gtk.Notebook()
        self.text_box.pack_start(self.html_switcher, True, True, 0)
        
        #Create html text view
        self.html_text_language = GtkSource.LanguageManager.get_default().get_language("html")
        self.html_text_buffer = GtkSource.Buffer.new_with_language(self.html_text_language)
        self.html_text = GtkSource.View.new_with_buffer(self.html_text_buffer)
        self.html_text.set_hexpand(True)
        self.html_text.set_vexpand(True)
        self.html_text.set_editable(False)
        self.html_text.set_wrap_mode(Gtk.WrapMode.WORD)
        self.html_text_scroll = Gtk.ScrolledWindow()
        self.html_text_scroll.add(self.html_text)
        self.html_switcher.append_page(self.html_text_scroll, Gtk.Label("Text"))
        
        #Create rendered html view
        self.html_view = WebKit.WebView()
        self.html_view.set_hexpand(True)
        self.html_view.set_vexpand(True)
        self.html_view_scroll = Gtk.ScrolledWindow()
        self.html_view_scroll.add(self.html_view)
        self.html_switcher.append_page(self.html_view_scroll, Gtk.Label("View"))
        
        self.html_switcher.show_all()
        self.html_switcher.set_current_page(1)
        self.md_text.grab_focus()
        
    
    def md_text_changed(self, md_buffer):
        md_text = md_buffer.get_text(md_buffer.get_start_iter(), md_buffer.get_end_iter(), False)
        
        html_text = md_to_html(md_text)
        
        self.html_text.get_buffer().set_text(html_text)
        self.html_view.load_html_string(html_text, "")
    
    def on_can_undoredo_changed(self):
        self.undo_button.set_sensitive(self.md_text_undoer.can_undo())
        self.redo_button.set_sensitive(self.md_text_undoer.can_redo())
    
    def undo(self):
        if self.md_text_undoer.can_undo():
            self.md_text_undoer.undo()
    
    def redo(self):
        if self.md_text_undoer.can_redo():
            self.md_text_undoer.redo()
    
    def on_window_state_change(self, window, event):
        if bool(Gdk.WindowState.FULLSCREEN & event.new_window_state):
            self.is_fullscreen = True
        else:
            self.is_fullscreen = False
    
    def toggle_fullscreen(self):
        if self.is_fullscreen:
            self.unfullscreen()
        else:
            self.fullscreen()
    
    def show_about_dialog(self):
        about_dialog = Gtk.AboutDialog()
        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_transient_for(self)
        about_dialog.set_modal(True)
        
        about_dialog.set_program_name("MarkEdit")
        about_dialog.set_logo_icon_name("text-editor")
        about_dialog.set_comments("A simple native Markdown Editor.")
        about_dialog.set_license_type(Gtk.License.GPL_3_0)
        
        about_dialog.run()
        about_dialog.destroy()
    
    def open_file(self):
        dialog = Gtk.FileChooserDialog("Open", self,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL,
                                       Gtk.ResponseType.CANCEL,
                                       Gtk.STOCK_OPEN,
                                       Gtk.ResponseType.ACCEPT))
        
        if dialog.run() == Gtk.ResponseType.ACCEPT:
            self.file_path = dialog.get_filename()
            selected_file = open(self.file_path, "r")
            self.md_text_buffer.set_text(selected_file.read())
            selected_file.close()
        
        dialog.destroy()
    
    def save_file(self, save_as):
        md_text = self.md_text_buffer.get_text(
                        self.md_text_buffer.get_start_iter(),
                        self.md_text_buffer.get_end_iter(),
                        False)
        
        #if the normal save button was pressed
        #save the changes to the opened file
        if save_as == False and self.file_path != None:
            pass
        else:
            dialog = Gtk.FileChooserDialog("Save", self,
                                           Gtk.FileChooserAction.SAVE,
                                           (Gtk.STOCK_CANCEL,
                                           Gtk.ResponseType.CANCEL,
                                           Gtk.STOCK_SAVE,
                                           Gtk.ResponseType.ACCEPT))
            dialog.set_do_overwrite_confirmation(True)
            
            if dialog.run() == Gtk.ResponseType.ACCEPT:
                self.file_path = dialog.get_filename()
                dialog.destroy()
            else:
                dialog.destroy()
                return
        
        #actually write the file
        selected_file = open(self.file_path, "w")
        selected_file.write(md_text)
        selected_file.close()
    
    def open_new_window(self):
        MyWindow()
    
    def exit_window(self):
        self.hide()
        global N_OPEN_WINDOWS
        N_OPEN_WINDOWS = N_OPEN_WINDOWS-1
        
        if N_OPEN_WINDOWS == 0:
            Gtk.main_quit()
        

def md_to_html(text):
    try:
        return markdown.markdown(unicode(text, "UTF-8"))
    except UnicodeDecodeError, e:
        print "Error! - UnicodeDecodeError"
        print str(e)
        return text

if __name__=="__main__":
    MyWindow()
    
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()
