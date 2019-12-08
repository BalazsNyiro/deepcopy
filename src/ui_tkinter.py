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
    OnePageWidth = 600

    Window = window_new(Prg, "window.main.title")
    Window.geometry('{}x{}'.format(MainWidth, MainHeight))
    Prg["Tkinter"]["Window"] = Window

    TextRecognisedWidth = MainWidth - SourceWidth - OnePageWidth

    ############# SCROLLBAR ###################
    # # https://stackoverflow.com/questions/16188420/tkinter-scrollbar-for-frame
    FrameSourcePages = frame_new(Prg, Window, SourceWidth, MainHeight, bg="yellow")
    FrameSourcePages.grid(row=0, column=0, rowspan=3)

    CanvasForScrollBar = Tkinter.Canvas(FrameSourcePages)
    Prg["Tkinter"]["CanvasForScrollBar"] = CanvasForScrollBar
    CanvasForScrollBar.pack()

    FrameInner = frame_new(Prg, CanvasForScrollBar, SourceWidth, MainHeight)
    Prg["Tkinter"]["FrameInner"] = FrameInner
    Tkinter.Label(FrameInner, text="222").pack()
    Tkinter.Label(FrameInner, text="333").pack()
    FrameInner.pack()

    Scrollbar = Tkinter.Scrollbar(FrameInner, orient="vertical", command=CanvasForScrollBar.yview)

    CanvasForScrollBar.configure(yscrollcommand=Scrollbar.set)
    Scrollbar.pack(side="right", fill="y")
    CanvasForScrollBar.create_window((0, 0), window=FrameInner, anchor='nw')
    FrameInner.bind("<Configure>", lambda Event: CanvasForScrollBar.configure(scrollregion=CanvasForScrollBar.bbox("all"),width=200,height=200))
    ############# SCROLLBAR ###################

    FrameOnePageTextboxSelector = frame_new(Prg, Window, OnePageWidth, MainHeight)
    FrameOnePageTextboxSelector.grid(row=0, column=1, rowspan=3)

    FrameTextRecognised = frame_new(Prg, Window, TextRecognisedWidth, MainHeight, bg="green")
    FrameTextRecognised.grid(row=0, column=2, rowspan=3)

    # FIXME: ?? Maybe we can pass Frame with a lambda function, as in   files_thumbnails_load_button_cmd()
    Tkinter.Button(FrameOnePageTextboxSelector, text=util.ui_msg(Prg, "file_operation.file_load_into_thumbnail_list"), command=files_thumbnails_load_button_cmd).pack()

    Tkinter.Label(FrameTextRecognised, text="Text Recognised").grid(row=0, column=2)

    Window.mainloop()

def files_thumbnails_load_button_cmd(): # it is called from Ui so we use global state to store objects.
    Prg = PrgGlobal
    Parent = Prg["Tkinter"]["FrameInner"]
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
            Parent.update_idletasks()
            Prg["Tkinter"]["CanvasForScrollBar"].update_idletasks()
            Window.update_idletasks()

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
    return Tkinter.Frame(Parent, bg=bg, width=Width, height=Height,pady=3)

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

