# -*- coding: utf-8 -*-
import util, os, time

PrgGlobal = None
ErrorsLocal = []

try:
    import tkinter as Tkinter
    import tkinter.filedialog as FileDialog
except ImportError:
    ErrorsLocal.append("install.missing.module_tkinter")

try:
    from PIL import Image
except ImportError:
    ErrorsLocal.append("install.missing.module_pillow")

try:
    from PIL import ImageTk
except ImportError:
    ErrorsLocal.append("install.missing.package_ImageTk")


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

    def frame_thumbnail_bind(Event, Canvas):
        print("Event:", Event)
        print("canvas bbox all", Canvas.bbox("all"))
        ScrollRegion = Canvas.bbox("all")
        Canvas.configure(scrollregion=ScrollRegion)

    ############# SCROLLBAR ###################
    ContainerLeft = Tkinter.Frame(Window, bg="blue", width=SourceWidth)
    ContainerLeft.pack(side="left")
    # # https://stackoverflow.com/questions/16188420/tkinter-scrollbar-for-frame
    CanvasForScrollBar = Tkinter.Canvas(ContainerLeft, bg="red", width=SourceWidth,
                                        height=9999)  # auto fitting in Y direction, until reach this value
    CanvasForScrollBar.pack(side="left", fill="y",
                            expand=True)  # IMPORTANT: the canvas FILL, expand settins Modifiy the scrollbar's look!!!!!
    Prg["Tkinter"]["CanvasForScrollBar"] = CanvasForScrollBar
    # Tkinter.Label(CanvasForScrollBar, text="canvas").pack()

    FrameThumbnails = Tkinter.Frame(CanvasForScrollBar, bg="purple")
    Prg["Tkinter"]["FrameThumbnails"] = FrameThumbnails

    Scrollbar = Tkinter.Scrollbar(ContainerLeft, orient="vertical", command=CanvasForScrollBar.yview)
    CanvasForScrollBar.configure(yscrollcommand=Scrollbar.set)
    Scrollbar.pack(side="right", fill="y")

    CanvasForScrollBar.create_window((0, 0), window=FrameThumbnails, anchor='nw')
    FrameThumbnails.bind("<Configure>", lambda Event, Canvas=CanvasForScrollBar: frame_thumbnail_bind(Event, Canvas))
    ############# SCROLLBAR ###################

    FrameOnePage = frame_new(Prg, Window, OnePageWidth, MainHeight)
    FrameOnePage.pack()

    CanvasWidth, CanvasHeight = Prg["UiTextBubbleSelectionCanvas"]
    CanvasOnePage = Tkinter.Canvas(FrameOnePage, width=CanvasWidth, height=CanvasHeight, bg="#000000")
    CanvasOnePage.pack()
    Prg["Tkinter"]["CanvasOnePage"] = CanvasOnePage
    Prg["Tkinter"]["ImgRenderedBubbleSelection"] = None

    ImgRenderedBubbleSelection = Tkinter.PhotoImage(width=CanvasWidth, height=CanvasHeight)
    Prg["Tkinter"]["CanvasOnePageCreatedImage"] = CanvasOnePage.create_image((CanvasWidth / 2, CanvasHeight / 2), image=ImgRenderedBubbleSelection, state="normal")



    FrameTextRecognised = frame_new(Prg, Window, TextRecognisedWidth, MainHeight, bg="green")
    FrameTextRecognised.pack()

    Tkinter.Button(FrameThumbnails, text=util.ui_msg(Prg, "file_operation.file_load_into_thumbnail_list"),
                   command=files_thumbnails_load_button_cmd).pack()

    Tkinter.Label(FrameTextRecognised, text="Text Recognised").pack(side="top")

    Window.mainloop()


def files_thumbnails_load_button_cmd():  # it is called from Ui so we use global state to store objects.
    Prg = PrgGlobal
    Parent = Prg["Tkinter"]["FrameThumbnails"]

    for FileSelected in files_selector(Prg):
        ImgId = img_generate_id_for_loaded_list(Prg, PreFix="thumbnail", PostFix=FileSelected)
        ImageTkPhotoImage = image_file_load_to_tk(Prg, FileSelected, Prg["UiThumbnailSize"])
        if ImageTkPhotoImage:
            ImageTkPhotoImage.ImgId = ImgId  # all image knows his own id, if you want to remove them, delete them from loaded image list
            Pixels, PixelDataSize, ImgWidth, ImgHeight = img_load_pixels(Prg, FileSelected)  # RGB has 3 integers, RGBA has 4, Grayscale has 1 integer
            # Prg["Tkinter"]["images_loaded"][ImgId] = ImageTkPhotoImage # save reference of Img, otherwise garbace collector remove it
            Prg["Tkinter"]["images_loaded"][ImgId] = {
                "reference_to_avoid_garbage_collector": ImageTkPhotoImage,
                "TextBubbles": [],  # here can be lists, with coordinate pairs,
                "FilePath_original": FileSelected,
                "Pixels": Pixels,
                "PixelDataSize": PixelDataSize,
                "Width": ImgWidth,
                "Height": ImgHeight
            }

            #  example      "TextBubbles" : [    one bubble can contain any coordinate pairs
            #                                     [ [5,10], [256, 10], [256, 612], [5, 612] ]
            #                                ]

            Panel = Tkinter.Label(Parent, image=ImageTkPhotoImage)
            Panel.pack()
            Panel.bind("<Button-1>", lambda Event: thumbnail_click_left_mouse(Prg, ImgId))
            # print("loaded images: ", Prg["Tkinter"]["images_loaded"])


def thumbnail_click_left_mouse(Prg, ImgId):

    Displayed = Image.new("RGB", Prg["UiTextBubbleSelectionCanvas"], color=0)
    Prg["Tkinter"]["ImgRenderedBubbleSelection"] = Displayed

    TimeStart = time.time()
    CanvasWidth, CanvasHeight = Prg["UiTextBubbleSelectionCanvas"]

    ImgLoaded = Prg["Tkinter"]["images_loaded"][ImgId]

    PixelDataSize = ImgLoaded["PixelDataSize"]

    RangeCanvasHeight = range(0, min(CanvasHeight, ImgLoaded["Height"]))

    print("imt output ")
    print(dir(ImgLoaded))
    if PixelDataSize == 3:
        def draw_pixel(ImgOutput, ImgInput, XY):
            # original, nice working solution:
            # ImgOutput.putpixel(XY, ImgInput["Pixels"][XY])
            # we can use original tuple with 3 elements

            # faster, direct solution, not nice:
            # but we don't do a lot of checking, it's a 2x faster solution
            # It was inside ImgOutput.putpixel()
            ImgOutput.im.putpixel(XY, ImgInput["Pixels"][XY])

    elif PixelDataSize == 4:
        def draw_pixel(ImgOutput, ImgInput, XY):
            R, G, B, _A = ImgInput["Pixels"][XY]
            ImgOutput.putpixel(XY, (R, G, B))

    for X in range(0, min(CanvasWidth, ImgLoaded["Width"])):
        for Y in RangeCanvasHeight:
                    draw_pixel(Displayed, ImgLoaded, (X, Y) )

    TimeEnd = time.time() - TimeStart
    print("render time:", TimeEnd)
    CanvasOnePage = Prg["Tkinter"]["CanvasOnePage"]
    # Prg["Tkinter"]["CanvasOnePageCreatedImage"] = \
    # CanvasOnePage.create_image((CanvasWidth / 2, CanvasHeight / 2), image=ImageTk.PhotoImage(Displayed))
    Prg["Tkinter"]["LastDisplayedTextBubble"] = ImageTk.PhotoImage(Displayed)
    CanvasOnePage.itemconfig(Prg["Tkinter"]["CanvasOnePageCreatedImage"], image=Prg["Tkinter"]["LastDisplayedTextBubble"])

def files_selector(Prg):
    Dir = Prg["PathDefaultFileSelectDir"]
    print(Dir)
    return FileDialog.askopenfilenames(initialdir=Prg["PathDefaultFileSelectDir"], title="Select file",
                                       filetypes=(
                                       ("png files", "*.png"), ("jpeg files", "*.jpg"), ("all files", "*.*")))


def img_load_pixels(Prg, ImgPath, Timer=False):
    ImgOriginal = Image.open(ImgPath)
    ImgWidth, ImgHeight = ImgOriginal.size

    # detect once that it's RGB or RGBA (3 or 4 elements in the tuple)
    PixelSample = ImgOriginal.getpixel((0, 0))
    PixelDataSize = len(PixelSample)
    print("Pixel Data size: ", PixelDataSize)

    # https://pillow.readthedocs.io/en/3.0.x/reference/PixelAccess.html
    # slow way to load pixels
    # Pixels = dict()
    # for X in range(0, ImgWidth):
    #     Pixels[X] = dict()
    #     for Y in range(0, ImgHeight):
    #         # we can have Alpha value here
    #         Pixels[X][Y] = ImgOriginal.getpixel((X, Y))
    Pixels = ImgOriginal.load()

    return Pixels, PixelDataSize, ImgWidth, ImgHeight

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
