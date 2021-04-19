# import tkinter
# import tkinter.font
# from tkinter import ttk
#
# tree_columns = ("country", "capital", "currency")
# tree_data = [
#     ("Argentina",      "Buenos Aires",     "ARS"),
#     ("Australia",      "Canberra",         "AUD"),
#     ("Brazil",         "Brazilia",         "BRL"),
#     ("Canada",         "Ottawa",           "CAD"),
#     ("China",          "Beijing",          "CNY"),
#     ("France",         "Paris",            "EUR"),
#     ("Germany",        "Berlin",           "EUR"),
#     ("India",          "New Delhi",        "INR"),
#     ("Italy",          "Rome",             "EUR"),
#     ("Japan",          "Tokyo",            "JPY"),
#     ("Mexico",         "Mexico City",      "MXN"),
#     ("Russia",         "Moscow",           "RUB"),
#     ("South Africa",   "Pretoria",         "ZAR"),
#     ("United Kingdom", "London",           "GBP"),
#     ("United States",  "Washington, D.C.", "USD")
# ]
#
# def sortby(tree, col, descending):
#     """Sort tree contents when a column is clicked on."""
#     # grab values to sort
#     data = [(tree.set(child, col), child) for child in tree.get_children('')]
#
#     # reorder data
#     data.sort(reverse=descending)
#     for indx, item in enumerate(data):
#         tree.move(item[1], '', indx)
#
#     # switch the heading so that it will sort in the opposite direction
#     tree.heading(col,
#                  command=lambda col=col: sortby(tree, col, int(not descending)))
#
# class App(object):
#     def __init__(self):
#         self.tree = None
#         self._setup_widgets()
#         self._build_tree()
#
#     def _setup_widgets(self):
#         msg = ttk.Label(wraplength="4i", justify="left", anchor="n",
#                         padding=(10, 2, 10, 6),
#                         text=("Ttk is the new Tk themed widget set. One of the widgets it "
#                               "includes is a tree widget, which can be configured to "
#                               "display multiple columns of informational data without "
#                               "displaying the tree itself. This is a simple way to build "
#                               "a listbox that has multiple columns. Clicking on the "
#                               "heading for a column will sort the data by that column. "
#                               "You can also change the width of the columns by dragging "
#                               "the boundary between them."))
#         msg.pack(fill='x')
#
#         container = ttk.Frame()
#         container.pack(fill='both', expand=True)
#
#         # XXX Sounds like a good support class would be one for constructing
#         #     a treeview with scrollbars.
#         self.tree = ttk.Treeview(columns=tree_columns, show="headings")
#         vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
#         hsb = ttk.Scrollbar(orient="horizontal", command=self.tree.xview)
#         self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
#         self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
#         vsb.grid(column=1, row=0, sticky='ns', in_=container)
#         hsb.grid(column=0, row=1, sticky='ew', in_=container)
#
#         container.grid_columnconfigure(0, weight=1)
#         container.grid_rowconfigure(0, weight=1)
#
#     def _build_tree(self):
#         for col in tree_columns:
#             self.tree.heading(col, text=col.title(),
#                               command=lambda c=col: sortby(self.tree, c, 0))
#             # XXX tkFont.Font().measure expected args are incorrect according
#             #     to the Tk docs
#             self.tree.column(col, width=tkinter.font.Font().measure(col.title()))
#
#         for item in tree_data:
#             self.tree.insert('', 'end', values=item)
#
#             # adjust columns lenghts if necessary
#             for indx, val in enumerate(item):
#                 ilen = tkinter.font.Font().measure(val)
#                 if self.tree.column(tree_columns[indx], width=None) < ilen:
#                     self.tree.column(tree_columns[indx], width=ilen)
#
# def main():
#     root = tkinter.Tk()
#     root.wm_title("Multi-Column List")
#     root.wm_iconname("mclist")
#
#     # import plastik_theme
#     # try:
#     #     plastik_theme.install('~/tile-themes/plastik/plastik')
#     # except Exception:
#     #     import warnings
#     #     warnings.warn("plastik theme being used without images")
#
#     app = App()
#     root.mainloop()
#
# if __name__ == "__main__":
#     main()
#
# """
# tkentrycomplete.py
#
# A Tkinter widget that features autocompletion.
#
# Created by Mitja Martini on 2008-11-29.
# Updated by Russell Adams, 2011/01/24 to support Python 3 and Combobox.
# Updated by Dominic Kexel to use Tkinter and ttk instead of tkinter and tkinter.ttk
#    Licensed same as original (not specified?), or public domain, whichever is less restrictive.
# """
# import sys
# import os
# import tkinter
# from tkinter import ttk
# # import ttk
#
# __version__ = "1.1"
#
# # I may have broken the unicode...
# Tkinter_umlauts=['odiaeresis', 'adiaeresis', 'udiaeresis', 'Odiaeresis', 'Adiaeresis', 'Udiaeresis', 'ssharp']
#
# class AutocompleteEntry(tkinter.Entry):
#     """
#     Subclass of Tkinter.Entry that features autocompletion.
#
#     To enable autocompletion use set_completion_list(list) to define
#     a list of possible strings to hit.
#     To cycle through hits use down and up arrow keys.
#     """
#     def set_completion_list(self, completion_list):
#         self._completion_list = sorted(completion_list, key=str.lower) # Work with a sorted list
#         self._hits = []
#         self._hit_index = 0
#         self.position = 0
#         self.bind('<KeyRelease>', self.handle_keyrelease)
#
#     def autocomplete(self, delta=0):
#         """autocomplete the Entry, delta may be 0/1/-1 to cycle through possible hits"""
#         if delta: # need to delete selection otherwise we would fix the current position
#             self.delete(self.position, tkinter.END)
#         else: # set position to end so selection starts where textentry ended
#             self.position = len(self.get())
#         # collect hits
#         _hits = []
#         for element in self._completion_list:
#             if element.lower().startswith(self.get().lower()):  # Match case-insensitively
#                 _hits.append(element)
#         # if we have a new hit list, keep this in mind
#         if _hits != self._hits:
#             self._hit_index = 0
#             self._hits=_hits
#         # only allow cycling if we are in a known hit list
#         if _hits == self._hits and self._hits:
#             self._hit_index = (self._hit_index + delta) % len(self._hits)
#         # now finally perform the auto completion
#         if self._hits:
#             self.delete(0,tkinter.END)
#             self.insert(0,self._hits[self._hit_index])
#             self.select_range(self.position,tkinter.END)
#
#     def handle_keyrelease(self, event):
#         """event handler for the keyrelease event on this widget"""
#         if event.keysym == "BackSpace":
#             self.delete(self.index(tkinter.INSERT), tkinter.END)
#             self.position = self.index(tkinter.END)
#         if event.keysym == "Left":
#             if self.position < self.index(tkinter.END): # delete the selection
#                 self.delete(self.position, tkinter.END)
#             else:
#                 self.position = self.position-1 # delete one character
#                 self.delete(self.position, tkinter.END)
#         if event.keysym == "Right":
#             self.position = self.index(tkinter.END) # go to end (no selection)
#         if event.keysym == "Down":
#             self.autocomplete(1) # cycle to next hit
#         if event.keysym == "Up":
#             self.autocomplete(-1) # cycle to previous hit
#         if len(event.keysym) == 1 or event.keysym in Tkinter_umlauts:
#             self.autocomplete()
#
# class AutocompleteCombobox(ttk.Combobox):
#
#     def set_completion_list(self, completion_list):
#         """Use our completion list as our drop down selection menu, arrows move through menu."""
#         self._completion_list = sorted(completion_list, key=str.lower) # Work with a sorted list
#         self._hits = []
#         self._hit_index = 0
#         self.position = 0
#         self.bind('<KeyRelease>', self.handle_keyrelease)
#         self['values'] = self._completion_list  # Setup our popup menu
#
#     def autocomplete(self, delta=0):
#         """autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
#         if delta: # need to delete selection otherwise we would fix the current position
#             self.delete(self.position, tkinter.END)
#         else: # set position to end so selection starts where textentry ended
#             self.position = len(self.get())
#         # collect hits
#         _hits = []
#         for element in self._completion_list:
#             if element.lower().startswith(self.get().lower()): # Match case insensitively
#                 _hits.append(element)
#         # if we have a new hit list, keep this in mind
#         if _hits != self._hits:
#             self._hit_index = 0
#             self._hits=_hits
#         # only allow cycling if we are in a known hit list
#         if _hits == self._hits and self._hits:
#             self._hit_index = (self._hit_index + delta) % len(self._hits)
#         # now finally perform the auto completion
#         if self._hits:
#             self.delete(0,tkinter.END)
#             self.insert(0,self._hits[self._hit_index])
#             self.select_range(self.position,tkinter.END)
#
#     def handle_keyrelease(self, event):
#         """event handler for the keyrelease event on this widget"""
#         if event.keysym == "BackSpace":
#             self.delete(self.index(tkinter.INSERT), tkinter.END)
#             self.position = self.index(tkinter.END)
#         if event.keysym == "Left":
#             if self.position < self.index(tkinter.END): # delete the selection
#                 self.delete(self.position, tkinter.END)
#             else:
#                 self.position = self.position-1 # delete one character
#                 self.delete(self.position, tkinter.END)
#         if event.keysym == "Right":
#             self.position = self.index(tkinter.END) # go to end (no selection)
#         if len(event.keysym) == 1:
#             self.autocomplete()
#         # No need for up/down, we'll jump to the popup
#         # list at the position of the autocompletion
#
# def test(test_list):
#     """Run a mini application to test the AutocompleteEntry Widget."""
#     root = tkinter.Tk(className=' AutocompleteEntry demo')
#     entry = AutocompleteEntry(root)
#     entry.set_completion_list(test_list)
#     entry.pack()
#     entry.focus_set()
#     combo = AutocompleteCombobox(root)
#     combo.set_completion_list(test_list)
#     combo.pack()
#     combo.focus_set()
#     # I used a tiling WM with no controls, added a shortcut to quit
#     root.bind('<Control-Q>', lambda event=None: root.destroy())
#     root.bind('<Control-q>', lambda event=None: root.destroy())
#     root.mainloop()
#
# if __name__ == '__main__':
#     test_list = ('apple', 'banana', 'CranBerry', 'dogwood', 'alpha', 'Acorn', 'Anise' )
#     test(test_list)


#or try: https://github.com/Coal0/Utilities/tree/master/tkinter_autocomplete

#https://codereview.stackexchange.com/questions/174108/autocomplete-for-tkinter-entry-widgets
try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    # Python 2
    import Tkinter as tk
    import ttk

__all__ = ["Autocomplete"]

NO_RESULTS_MESSAGE = "No results found for '{}'"


def _longest_common_substring(s1, s2):
    """Get the longest common substring for two strings.
    Source: [1]
    """
    m = [[0] * (1 + len(s2)) for i in range(1 + len(s1))]
    longest, x_longest = 0, 0
    for x in range(1, 1 + len(s1)):
        for y in range(1, 1 + len(s2)):
            if s1[x - 1] == s2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
            else:
                m[x][y] = 0
    return s1[x_longest - longest: x_longest]


class Autocomplete(tk.Frame, object):
    """An autocomplete object is a container for tk.Entry and tk.Listbox
    widgets. Together, these widgets can provide end users with relevant
    results (autocomplete entries).
    Methods defined here:
    __init__(): The init method initializes a new tk.Frame object, as
                well as the tk.Entry and tk.Listbox widgets. These can
                be modified by accessing respectively
                `Autocomplete.entry_widget` and
                `Autocomplete.listbox_widget`.

    build(): The build method sets up the autocompletion settings for
             the tk.Entry widget. It is mandatory to call build()
             to be able to display the frame.

    _update_autocomplete(): The _update_autocomplete method evaluates
                            whatever the tk.Entry widget contains and
                            updates the tk.Listbox widget to display
                            relevant matches. It is called on
                            <KeyRelease> and should never be called
                            explicitly.
    _select_entry(): The _select_entry method replaces the textvariable
                     connected to the tk.Entry widget with the current
                     listbox selection. It is called on
                     <<ListboxSelect>> and should never be called
                     explicitly.

    Constants defined here:
    DEFAULT_LISTBOX_HEIGHT: The default 'height' attribute for the
                            tk.Listbox widget. This value directly
                            corresponds to the maximum amount of results
                            shown in the tk.Listbox widget at once.
                            Note that the user may view more results
                            by scrolling vertically.
                            --- DEFAULT = 5 ---

    DEFAULT_LISTBOX_WIDTH: The default 'width' attribute for the
                           tk.Listbox widget. This value directly
                           corresponds to the maximum amount of
                           characters shown per result at once.
                           Note that the user may view more characters
                           by scrolling horizontally.
                           --- DEFAULT = 25 ---

    DEFAULT_ENTRY_WIDTH: The default 'width' attribute for the tk.Entry
                         widget.
                         --- DEFAULT = 25 ---
    """

    DEFAULT_LISTBOX_HEIGHT = 5
    DEFAULT_LISTBOX_WIDTH = 25
    DEFAULT_ENTRY_WIDTH = 25

    def __init__(self, *args, **kwargs):
        """Constructor.
        Initialize a new tk.Frame object and create a tk.Entry and
        tk.Listbox widget for later configuration.
        ---
        Arguments:
        All arguments passed here will be directly passed to a new
        tk.Frame instance. For further help:
            >>> help(tk.Frame)
        ---
        Example:
            >>> autocomplete = Autocomplete(tk.Tk())
            >>> autocomplete["width"] = 50
            >>> # Corresponds to tk.Frame["width"]
        ---
        Returns:
        None
        """

        super(Autocomplete, self).__init__(*args, **kwargs)
        self.text = tk.StringVar()
        self.entry_widget = tk.Entry(
            self,
            textvariable=self.text,
            width=self.DEFAULT_ENTRY_WIDTH
        )
        self.listbox_widget = tk.Listbox(
            self,
            height=self.DEFAULT_LISTBOX_HEIGHT,
            width=self.DEFAULT_LISTBOX_WIDTH
        )

    def build(self, entries, match_exact=False, case_sensitive=False,
              no_results_message=NO_RESULTS_MESSAGE):
        """Set up the tk.Entry and tk.Listbox widgets.
        ---
        Arguments:
        * entries: [iterable] Autocompletion entries.
        * match_exact: [bool] Treat only entries that start with
                              the current entry as matches.
                              If False, select the most relevant results
                              based on the length of the longest common
                              substring (LCS).
                              Defaults to False.
        * case_senstive: [bool] Treat only entries with the exact same
                                characters as matches. If False, allow
                                capitalization to be mixed.
                                Defaults to False.
        * no_results_message: The message to display if no matches
                              could be found for the current entry.
                              May include a formatting key to display
                              the current entry. If None, the tk.Listbox
                              widget will be hidden until the next
                              <KeyRelease> event.
        ---
        Example:
            >>> autocomplete = Autocomplete(tk.Root())
            >>> autocomplete.build(
            ...     entries=["Foo", "Bar"],
            ...     case_sensitive=True,
            ...     no_results_message="<No results for '{}'>"
            ... )
        ---
        Returns:
        None
        """
        if not case_sensitive:
            entries = list(map(
                lambda entry: entry.lower(), entries
            ))

        self._case_sensitive = case_sensitive
        self._entries = entries
        self._match_exact = match_exact
        self._no_results_message = no_results_message

        self.entry_widget.bind("<KeyRelease>", self._update_autocomplete)
        self.entry_widget.focus_set()
        self.entry_widget.grid(column=0, row=0)

        self.listbox_widget.bind("<<ListboxSelect>>", self._select_entry)
        self.listbox_widget.grid(column=0, row=1)
        self.listbox_widget.grid_forget()

    def _update_autocomplete(self, event):
        """Update the tk.Listbox widget to display new matches.
        Do not call explicitly.
        """
        self.listbox_widget.delete(0, tk.END)
        self.listbox_widget["height"] = self.DEFAULT_LISTBOX_HEIGHT

        text = self.text.get()
        if not self._case_sensitive:
            text = text.lower()
        if not text:
            self.listbox_widget.grid_forget()
        elif not self._match_exact:
            matches = {}
            for entry in self._entries:
                lcs = len(_longest_common_substring(text, entry))
                if lcs:
                    matches[entry] = lcs
            sorted_items = sorted(list(matches.items()),
                                  key=lambda match: match[1])
            for item in sorted_items[::-1]:
                self.listbox_widget.insert(tk.END, item[0])
        else:
            for entry in self._entries:
                if entry.strip().startswith(text):
                    self.listbox_widget.insert(tk.END, entry)

        listbox_size = self.listbox_widget.size()
        if not listbox_size:
            if self._no_results_message is None:
                self.listbox_widget.grid_forget()
            else:
                try:
                    self.listbox_widget.insert(
                        tk.END,
                        self._no_results_message.format(text)
                    )
                except UnicodeEncodeError:
                    self.listbox_widget.insert(
                        tk.END,
                        self._no_results_message.format(
                            text.encode("utf-8")
                        )
                    )
                if listbox_size <= self.listbox_widget["height"]:
                    # In case there's less entries than the maximum
                    # amount of entries allowed, resize the listbox.
                    self.listbox_widget["height"] = listbox_size
                self.listbox_widget.grid()
        else:
            if listbox_size <= self.listbox_widget["height"]:
                self.listbox_widget["height"] = listbox_size
            self.listbox_widget.grid()

    def _select_entry(self, event):
        """Set the textvariable corresponding to self.entry_widget
        to the value currently selected.
        Do not call explicitly.
        """
        widget = event.widget
        value = widget.get(int(widget.curselection()[0]))
        self.text.set(value)