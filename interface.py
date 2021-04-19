import tkinter
import tkinter.font
from tkinter import ttk
import sqlite3

global album_list
global album_display
global main_window
global display_frame
categories = ['Title', 'Artist', 'Year', 'Genre']


db = sqlite3.connect("albumtracker.sqlite")
db.execute("CREATE TABLE IF NOT EXISTS albums (title TEXT PRIMARY KEY NOT NULL, artist TEXT NOT NULL,"
           "year INT, genre TEXT)")
db.execute("CREATE TABLE IF NOT EXISTS classes (album TEXT PRIMARY KEY NOT NULL, listened INTEGER,"
           " desire INTEGER, veto INTEGER)")


def add_album():
    title, artist, year, genre = translate_info()
    album_str = "INSERT INTO albums (title, artist, year, genre) VALUES (?, ?, ?, ?)"
    class_str = "INSERT INTO classes (album, listened, desire, veto) VALUES (?, 0, 0, 0)"
    try:
        # print(title, artist, year, genre)
        db.execute(album_str, (title, artist, year, genre))
        db.execute(class_str, (title,))
        # clear item fields
        refresh_list(None)
        # print("submitted")
    except sqlite3.IntegrityError:
        pass
    db.commit()
    # clear_info()


def query_all():
    album_list = []
    cursor = db.cursor()
    entries = cursor.execute("SELECT * FROM albums")
    # print(entries)
    for each in entries:
        album_list.append(each)
    # print(album_list)
    return album_list


def search(query):
    query_list = []
    cursor = db.cursor()
    fixed_query = '%' + query + '%'
    album_query = "SELECT * FROM albums WHERE (title) LIKE ?"
    artist_query = "SELECT * FROM albums WHERE (artist) LIKE ?"
    year_query = "SELECT * FROM albums WHERE (year) LIKE ?"
    if query is None:
        refresh_list(None)
    else:
        for row in cursor.execute(album_query, (fixed_query,)):
            if row not in query_list:
                query_list.append(row)
        for row in cursor.execute(artist_query, (fixed_query,)):
            if row not in query_list:
                query_list.append(row)
        for row in cursor.execute(year_query, (fixed_query,)):
            if row not in query_list:
                query_list.append(row)
        return query_list


def update_classes(album, listened, desire, veto):
    class_update = "UPDATE classes SET (listened, desire, veto) = (?, ?, ?) WHERE album = ?"
    cursor = db.cursor()
    cursor.execute(class_update, (listened, desire, veto, album))
    db.commit()


def refresh_list(query):
    global album_list
    global display_frame
    global cur_sel_album
    if query == None or '':
        album_list = query_all()
    else:
        album_list = search(query)
    display_frame = tkinter.Frame(main_window)
    display_frame.grid(row=1, column=0, sticky='nsew', rowspan=3, columnspan=3)
    album_display = App(display_frame)
    # cur_sel_album = album_display('<<ListboxSelect>>')
    # album_display.bind('<<ListboxSelect>>', onselect) #todo: figure out bind


def selected_album(title):
    album_query = "SELECT * FROM albums WHERE title = ?"
    class_query = "SELECT * FROM classes WHERE albums = ?"
    cursor = db.cursor()
    al_title, artist, year, genre, = cursor.execute(album_query, (title,))
    _, listened, desire, veto = cursor.execute(class_query, (title,))
    return al_title, artist, year, genre, listened, desire, veto


def onselect(title):
    refresh_info(title)


def build_window():
    global main_window
    global display_frame
    global add_al_var, add_ar_var, add_yr_var, add_gr_var
    main_window = tkinter.Tk()

    main_window.title("Album Listening Tracker")
    main_window.geometry('1080x480-20-200')
    main_window['padx'] = 4

    album_label = tkinter.Label(main_window, text='Albums, bitch', font=1)
    album_label.grid(row=0, column=0, sticky='w')

    main_window.columnconfigure(0, weight=200)
    main_window.columnconfigure(1, weight=100)
    main_window.columnconfigure(2, weight=75)
    main_window.columnconfigure(3, weight=75)
    main_window.rowconfigure(0, weight=50)
    main_window.rowconfigure(1, weight=10)
    main_window.rowconfigure(2, weight=10)
    main_window.rowconfigure(3, weight=100)

    refresh_list_button = tkinter.Button(main_window, text="Refresh List", command=lambda: [refresh_list(None)])
    refresh_list_button.grid(row=0, column=1, sticky='w')
    search_field = tkinter.Entry(main_window)
    search_field.grid(row=0, column=1, sticky='e')
    search_button = tkinter.Button(main_window, text="Search", command=lambda: [refresh_list(search_field.get())])
    search_button.grid(row=0, column=2, sticky='w')
    # search_button.bind('<Return>', refresh_list(search_field.get())) #todo: can I make the enter button work?

    refresh_list(None)

    add_frame = tkinter.LabelFrame(main_window, text='Add album')
    add_frame.grid(row=2, column=3, sticky='n', rowspan=2)
    add_frame['padx'] = 8

    add_album_label = tkinter.Label(add_frame, text='Album:')
    add_album_label.grid(row=0, column=0, sticky='w', pady=4)
    add_artist_label = tkinter.Label(add_frame, text='Artist:')
    add_artist_label.grid(row=1, column=0, sticky='w', pady=4)
    add_year_label = tkinter.Label(add_frame, text='Year:')
    add_year_label.grid(row=2, column=0, sticky='w', pady=4)
    add_genre_label = tkinter.Label(add_frame, text='Genre:')
    add_genre_label.grid(row=3, column=0, sticky='w', pady=4)
    add_al_var = tkinter.StringVar()
    add_album_field = tkinter.Entry(add_frame, textvariable=add_al_var)          #todo: figure out suggestion dropdowns
    add_album_field.grid(row=0, column=1, sticky='w', pady=4)
    add_ar_var = tkinter.StringVar()
    add_artist_field = tkinter.Entry(add_frame, textvariable=add_ar_var)
    add_artist_field.grid(row=1, column=1, sticky='w', pady=4)
    add_yr_var = tkinter.IntVar()
    add_year_field = tkinter.Entry(add_frame, textvariable=add_yr_var)
    add_year_field.grid(row=2, column=1, sticky='w', pady=4)
    genre_options = ['Bluegrass', 'Blues', 'Classical', 'Country', 'Folk', 'Funk', 'Pop',
                     'Punk', 'R&B', 'Rap', 'Rock', 'Soundtrack', 'Jazz', 'Other']
    add_gr_var = tkinter.StringVar()
    add_gr_var.set("Country")
    add_genre_list = tkinter.OptionMenu(add_frame, add_gr_var, *genre_options)
    add_genre_list.grid(row=3, column=1, pady=4)
    submit_button = tkinter.Button(add_frame, text="Submit", command=add_album)
    submit_button.grid(row=4, column=1, sticky='n', pady=4)
    clear_button = tkinter.Button(add_frame, text='Clear', command=lambda: [(add_album_field.delete(0, 'end'), add_album_field.insert(0, ""),
                                                                             add_artist_field.delete(0, 'end'), add_artist_field.insert(0, ""),
                                                                             add_year_field.delete(0, 'end'), add_year_field.insert(0, ""),
                                                                             add_gr_var.set("Country"))])
    clear_button.grid(row=4, column=0, sticky='nw', pady=4)
    quit_button = tkinter.Button(main_window, text='Quit Program', command=main_window.quit)
    quit_button.grid(row=3, column=3, sticky='s', pady=8)
    # refresh_info(False)
    main_window.mainloop()


def translate_info():
    global add_al_var, add_ar_var, add_yr_var, add_gr_var
    album = str(add_al_var.get())
    artist = str(add_ar_var.get())
    year = str(add_yr_var.get())
    genre = str(add_gr_var.get())
    return album, artist, year, genre

# def refresh_info(album):
#     global album_display
#     if not album:
#         cur_album = 'Nada yet'
#         cur_artist = 'your mom'
#         cur_genyear = 'nope'
#     else:
#         cur_album, cur_artist, year, genre, listened, desire, veto = selected_album(album)
#         cur_genyear = (genre + ' from ' + year)
#     info_frame = tkinter.LabelFrame(main_window, text='Album Info')
#     info_frame.grid(row=0, column=3, ipadx=10, sticky='news', rowspan=2)
#     listened = tkinter.IntVar()
#     desire = tkinter.IntVar()
#     veto = tkinter.IntVar()
#     info_title = tkinter.Label(info_frame, text=cur_album)
#     info_title.grid(row=0, column=0, columnspan=3, sticky='nsew')
#     info_artist = tkinter.Label(info_frame, text=cur_artist)
#     info_artist.grid(row=1, column=0, columnspan=3, sticky='nsew')
#     info_genyear = tkinter.Label(info_frame, text=cur_genyear)
#     info_genyear.grid(row=2, column=0, columnspan=3, sticky='nsew')
#     listened_chk = tkinter.Checkbutton(info_frame, text="Listened to", variable=listened)
#     listened_chk.grid(row=3, column=0)
#     desire_chk = tkinter.Checkbutton(info_frame, text="Want to listen", variable=desire)
#     desire_chk.grid(row=4, column=0)
#     veto_chk = tkinter.Checkbutton(info_frame, text="Vetoed", variable=veto)
#     veto_chk.grid(row=5, column=0)
#     update_info = tkinter.Button(info_frame, text="Update", command=lambda: [update_classes(cur_album,
#                                                                              listened.get,
#                                                                              desire.get,
#                                                                              veto.get)])
#     fetch_info = tkinter.Button(info_frame, text="Retrieve", command=refresh_info)
#     update_info.grid(row=5, column=2, sticky='e')
#     fetch_info.grid(row=3, column=2, sticky='e')


def sortby(tree, col, descending):
    """Sort tree contents when a column is clicked on."""
    # grab values to sort
    data = [(tree.set(child, col), child) for child in tree.get_children('')]

    # reorder data
    data.sort(reverse=descending)
    for indx, item in enumerate(data):
        tree.move(item[1], '', indx)

    # switch the heading so that it will sort in the opposite direction
    tree.heading(col,
                 command=lambda col=col: sortby(tree, col, int(not descending)))


class App(object):
    def __init__(self, use_frame):
        self.tree = None
        self._setup_widgets(use_frame)
        self._build_tree()


    def _setup_widgets(self, use_frame):

        container = use_frame
        # XXX Sounds like a good support class would be one for constructing
        #     a treeview with scrollbars.
        self.tree = ttk.Treeview(columns=categories, show="headings")
        vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)

        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

    def _build_tree(self):
        for col in categories:
            self.tree.heading(col, text=col.title(),
                              command=lambda c=col: sortby(self.tree, c, 0))
            # XXX tkFont.Font().measure expected args are incorrect according
            #     to the Tk docs
            self.tree.column(col, width=tkinter.font.Font().measure(col.title()))

        for item in album_list:
            self.tree.insert('', 'end', values=item)

            # adjust columns lenghts if necessary
            for indx, val in enumerate(item):
                ilen = tkinter.font.Font().measure(val)
                if self.tree.column(categories[indx], width=None) < ilen:
                    self.tree.column(categories[indx], width=ilen)



def main():
    # album_list = populate_list()
    build_window()

    db.commit()
    db.close()

if __name__ == '__main__':
    main()