#!/usr/bin/env python

print "Trying to import markdown ...",
try:
    import markdown
    print "\t\t\t\tDONE"
except:
    print "\t\t\t\tERROR"
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
    print "Starting without Gtk.SourceView, advanced features will not be available."
    print "Install gtksourceview 3, its gir bindings and the language specific files for"
    print "html and markdown to enable syntax highlighting."
    WITH_SOURCEVIEW = False

print "Trying to import WebKit from gi.repository ...",
try:
    from gi.repository import WebKit
    print "\t\tDONE"
except:
    print "\t\tERROR"
    sys.exit(1)

WITH_SOURCEVIEW = True

class MyWindow(Gtk.Window):
    def __init__(self):
        self.build_gui()
        
    def build_gui(self):
        Gtk.Window.__init__(self, title="Markdown")
        self.connect("delete-event", Gtk.main_quit)
        self.set_default_size(900,750)
        
        self.text_box = Gtk.Box()
        self.text_box.set_homogeneous(True)
        self.add(self.text_box)
        
        if WITH_SOURCEVIEW:
            self.md_text_language = GtkSource.LanguageManager.get_default().get_language("markdown")
            self.md_text_buffer = GtkSource.Buffer.new_with_language(self.md_text_language)
            self.md_text = GtkSource.View.new_with_buffer(self.md_text_buffer)
        else:
            self.md_text = Gtk.TextView()
        self.md_text.set_hexpand(True)
        self.md_text.set_vexpand(True)
        self.md_text.set_editable(True)
        self.md_text.get_buffer().connect("changed", self.text_changed)
        self.md_text.set_wrap_mode(Gtk.WrapMode.WORD)
        self.md_text_scroll = Gtk.ScrolledWindow()
        self.md_text_scroll.add(self.md_text)
        self.text_box.pack_start(self.md_text_scroll, True, True, 0)
        
        self.html_switcher = Gtk.Notebook()
        self.text_box.pack_start(self.html_switcher, True, True, 0)
        
        if WITH_SOURCEVIEW:
            self.html_text_language = GtkSource.LanguageManager.get_default().get_language("html")
            self.html_text_buffer = GtkSource.Buffer.new_with_language(self.html_text_language)
            self.html_text = GtkSource.View.new_with_buffer(self.html_text_buffer)
        else:
            self.html_text = Gtk.TextView()
        self.html_text.set_hexpand(True)
        self.html_text.set_vexpand(True)
        self.html_text.set_editable(False)
        self.html_text.set_wrap_mode(Gtk.WrapMode.WORD)
        self.html_text_scroll = Gtk.ScrolledWindow()
        self.html_text_scroll.add(self.html_text)
        self.html_switcher.append_page(self.html_text_scroll, Gtk.Label("Text"))
        
        self.html_view = WebKit.WebView()
        self.html_view.set_hexpand(True)
        self.html_view.set_vexpand(True)
        self.html_view_scroll = Gtk.ScrolledWindow()
        self.html_view_scroll.add(self.html_view)
        self.html_switcher.append_page(self.html_view_scroll, Gtk.Label("View"))
        
        self.html_switcher.set_current_page(0)
        
    
    def text_changed(self, md_buffer):
        md_text = md_buffer.get_text(md_buffer.get_start_iter(), md_buffer.get_end_iter(), False)
        
        html_text = md_to_html(md_text)
        
        self.html_text.get_buffer().set_text(html_text)
        self.html_view.load_html_string(html_text, "")
        

def md_to_html(text):
    return markdown.markdown(text)

if __name__=="__main__":
    w = MyWindow()
    w.show_all()
    Gtk.main()
