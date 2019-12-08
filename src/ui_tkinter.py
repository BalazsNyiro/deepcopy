# -*- coding: utf-8 -*-
import util, os, time
PrgGlobal = None
ErrorsLocal = []

try:
    import tkinter as Tkinter
    import tkinter.filedialog as FileDialog
except ImportError: ErrorsLocal.append("install.missing.module_tkinter")

try:    from PIL import Image
except ImportError: ErrorsLocal.append("install.missing.module_pillow")

try:    from PIL import ImageTk
except ImportError: ErrorsLocal.append("install.missing.package_ImageTk")

def window_main(Prg):
    for ErrTxtKey in ErrorsLocal:
        Prg["Errors"].append(util.ui_msg(Prg, ErrTxtKey))

    if Prg["Errors"]: return

    # store passed Prg as a global variable, too, because Tkinter buttons need a state
    # I collect the msg NOT in the if because if one of them is missing, it causes Error
    global PrgGlobal
    PrgGlobal = Prg

    Prg["Tkinter"] = {"images_loaded": {}}

    MainWidth = 1200
    MainHeight = 800
    SourceWidth = 300
    SourceHeight = MainHeight
    SourceFrameWidth = SourceWidth
    SourceFrameHeight = SourceHeight
    OnePageWidth = 600

    Window = window_new(Prg, "window.main.title")
    Window.geometry('{}x{}'.format(MainWidth, MainHeight))
    Prg["Tkinter"]["Window"] = Window

    TextRecognisedWidth = MainWidth - SourceWidth - OnePageWidth

    def frame_thumbnail_bind(Event, Canvas):
        print("Event:", Event)
        print("canvas bbox all", Canvas.bbox("all"))
        ScrollRegion = Canvas.bbox("all")
        Canvas.configure(scrollregion=ScrollRegion)

    ############# SCROLLBAR ###################
    container = frame_new(Prg, Window,  SourceWidth, SourceHeight, bg="blue")
    container.grid(row=0, column=0)
    # # https://stackoverflow.com/questions/16188420/tkinter-scrollbar-for-frame
    CanvasForScrollBar = Tkinter.Canvas(container, width=SourceWidth-30, height=MainHeight-20, bg="red")
    CanvasForScrollBar.pack()
    Prg["Tkinter"]["CanvasForScrollBar"] = CanvasForScrollBar
    # Tkinter.Label(CanvasForScrollBar, text="canvas").pack()

    FrameThumbnails = frame_new(Prg, CanvasForScrollBar,  SourceWidth-40, SourceHeight/3, bg="purple")
    Prg["Tkinter"]["FrameThumbnails"] = FrameThumbnails

    Scrollbar = Tkinter.Scrollbar(container, orient="vertical", command=CanvasForScrollBar.yview)
    CanvasForScrollBar.configure(yscrollcommand=Scrollbar.set)
    Scrollbar.pack(side="right", fill="y")

    CanvasForScrollBar.create_window((0, 0), window=FrameThumbnails, anchor='nw')     # OK
    FrameThumbnails.bind("<Configure>", lambda Event, Canvas=CanvasForScrollBar: frame_thumbnail_bind(Event, Canvas))
    ############# SCROLLBAR ###################



    FrameOnePageTextboxSelector = frame_new(Prg, Window, OnePageWidth, MainHeight)
    FrameOnePageTextboxSelector.grid(row=0, column=1)

    FrameTextRecognised = frame_new(Prg, Window, TextRecognisedWidth, MainHeight, bg="green")
    FrameTextRecognised.grid(row=0, column=2)

    # FIXME: ?? Maybe we can pass Frame with a lambda function, as in   files_thumbnails_load_button_cmd()
    Tkinter.Button(FrameOnePageTextboxSelector, text=util.ui_msg(Prg, "file_operation.file_load_into_thumbnail_list"), command=files_thumbnails_load_button_cmd).pack()

    Tkinter.Label(FrameTextRecognised, text="Text Recognised").grid(row=0, column=2)

    Window.mainloop()

def files_thumbnails_load_button_cmd(): # it is called from Ui so we use global state to store objects.
    Prg = PrgGlobal
    Parent = Prg["Tkinter"]["FrameThumbnails"]
    Window = Prg["Tkinter"]["Window"]

    for FileSelected in files_selector(Prg):
        ImgId = img_generate_id_for_loaded_list(Prg, PreFix="thumbnail", PostFix=FileSelected)
        ImageTkPhotoImage = image_file_load_to_tk(Prg, FileSelected, Prg["UiThumbnailSize"])
        if ImageTkPhotoImage:
            ImageTkPhotoImage.ImgId = ImgId # all image knows his own id, if you want to remove them, delete them from loaded image list
            ImageTkPhotoImage.File = FileSelected
            Prg["Tkinter"]["images_loaded"][ImgId] = ImageTkPhotoImage # save reference of Img, otherwise garbace collector remove it
            Panel = Tkinter.Label(Parent, image=ImageTkPhotoImage)
            Panel.pack()
            Panel.bind("<Button-1>", lambda Event, File=FileSelected: thumbnail_click_left_mouse(File))
            print("loaded images: ", Prg["Tkinter"]["images_loaded"])
            #Parent.update_idletasks()
            # Prg["Tkinter"]["CanvasForScrollBar"].update_idletasks()
            # Window.update_idletasks()

def thumbnail_click_left_mouse(ImgPath):
    print("Thumbnail click:", ImgPath)
    # TODO load selected image into the Textbox selector area

def files_selector(Prg):
    Dir = Prg["PathDefaultFileSelectDir"]
    print(Dir)
    return FileDialog.askopenfilenames(initialdir=Prg["PathDefaultFileSelectDir"], title="Select file",
                                       filetypes=( ("png files", "*.png"), ("jpeg files", "*.jpg"),("all files", "*.*")))

def img_generate_id_for_loaded_list(Prg, PreFix="", PostFix=""):
    NumOfLoadedPics = len(Prg["Tkinter"]["images_loaded"].keys())
    if PreFix: PreFix += "_"
    if PostFix: PostFix = "_" + PostFix
    return "{:s}{:d}{:s}".format(PreFix, NumOfLoadedPics + 1, PostFix)

def frame_new(Prg, Parent, Width, Height, bg=""):
    return Tkinter.Frame(Parent, bg=bg, width=Width, height=Height, pady=3)

def window_new(Prg, TitleKey=""):
    Window = Tkinter.Tk()
    if TitleKey:
        Window.title(util.ui_msg(Prg, TitleKey))
    return Window

def img_resize(Prg, Source, Destination):
    pass

def image_file_load_to_tk(Prg, Path, ThumbnailSize=None):
    if not os.path.isfile(Path):
        Msg = util.ui_msg(Prg, "file_operation.file_missing", PrintInTerminal=True)
        Prg["Warning"].append(Msg)
        return False

    Load = Image.open(Path)
    if ThumbnailSize:
        Load.thumbnail(ThumbnailSize)
    return ImageTk.PhotoImage(Load)

