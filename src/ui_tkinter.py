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




    ##### Text Select Preview #################
    OnePageFrame = frame_new(Prg, Window, OnePageWidth, MainHeight)
    OnePageFrame.pack()

    TextSelectPreviewImg = Image.new("RGB", Prg["UiTextSelectPreviewSize"], color="grey")
    Prg["Tkinter"]["OnePageTextSelectPreviewImgLoaded"] = None
    Prg["Tkinter"]["OnePageTextSelectPreviewImgRendered"] = TextSelectPreviewImg


    ImageTkPhotoImage = ImageTk.PhotoImage(TextSelectPreviewImg)
    Label = Tkinter.Label(OnePageFrame, image=ImageTkPhotoImage)
    Prg["Tkinter"]["OnePageTextSelectPreviewLabel"] = Label
    Label.pack()
    ##### Text Select Preview #################





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
        ImageTkPhotoImageThumbnail = image_file_load_to_tk(Prg, FileSelected, Prg["UiThumbnailSize"])

        PixelsPreviewImg = image_file_load(Prg, FileSelected, Prg["UiTextSelectPreviewSize"])
        PixelsPreview = PixelsPreviewImg.load()

        if ImageTkPhotoImageThumbnail:
            ImageTkPhotoImageThumbnail.ImgId = ImgId  # all image knows his own id, if you want to remove them, delete them from loaded image list
            Pixels, PixelDataSize, ImgWidth, ImgHeight = img_load_pixels(Prg, FileSelected)  # RGB has 3 integers, RGBA has 4, Grayscale has 1 integer

            Prg["Tkinter"]["images_loaded"][ImgId] = {
                "reference_to_avoid_garbage_collector": ImageTkPhotoImageThumbnail,
                "TextSelectCoords": [],  # here can be lists, with coordinate pairs,
                "TextSelectPreviewPixels": PixelsPreview,
                "TextSelectPreviewPixelsWidth": PixelsPreviewImg.size[0],
                "TextSelectPreviewPixelsHeight": PixelsPreviewImg.size[1],
                "FilePath_original": FileSelected,
                "Pixels": Pixels,
                "PixelDataSize": PixelDataSize,
                "Width": ImgWidth,
                "Height": ImgHeight
            }

            #  example  "TextSelectCoords" : [    one bubble can contain any coordinate pairs
            #                                     [ [5,10], [256, 10], [256, 612], [5, 612] ]
            #                                ]

            Panel = Tkinter.Label(Parent, image=ImageTkPhotoImageThumbnail)
            Panel.pack()
            Panel.bind("<Button-1>", lambda Event: thumbnail_click_left_mouse(Prg, ImgId))
            # print("loaded images: ", Prg["Tkinter"]["images_loaded"])


def thumbnail_click_left_mouse(Prg, ImgId):
    ImgLoaded = Prg["Tkinter"]["images_loaded"][ImgId]
    Prg["Tkinter"]["OnePageTextSelectPreviewImgLoaded"] = ImgLoaded

    # start with a new, empty canvas
    TextSelectPreviewImg = Image.new("RGB", Prg["UiTextSelectPreviewSize"], color="grey")

    img_redraw(ImgLoaded["TextSelectPreviewPixels"],
               TextSelectPreviewImg,
               ImgSrcWidth = ImgLoaded["TextSelectPreviewPixelsWidth"],
               ImgSrcHeight= ImgLoaded["TextSelectPreviewPixelsHeight"],
               ImgTargetWidth= Prg["UiTextSelectPreviewSize"][0],
               ImgTargetHeight= Prg["UiTextSelectPreviewSize"][1],
               PixelDataSize=ImgLoaded["PixelDataSize"]
               )
    ImageTkPhotoImage = ImageTk.PhotoImage(TextSelectPreviewImg)
    Prg["Tkinter"]["OnePageTextSelectPreviewLabel"].configure(image=ImageTkPhotoImage)
    Prg["Tkinter"]["OnePageTextSelectPreviewLabel"].imageSaved=ImageTkPhotoImage

def img_redraw(ImgSrc,              ImgTarget,
               ImgTargetWidth=1,    ImgTargetHeight=1,
               ImgSrcWidth=1,       ImgSrcHeight=1,
               Xfrom=0,             Xto=999999,
               Yfrom=0,             Yto=999999,
               PixelDataSize=3):

    if PixelDataSize == 3:
        def draw_pixel(ImgInput, ImgOutput, XY):
            # original, nice working solution with correct API call
            # ImgOutput.putpixel(XY, ImgInput["Pixels"][XY])
            # DANGEROUS BUT FAST
            ImgOutput.im.putpixel(XY, ImgInput[XY])
            # ImgOutput.im.putpixel(XY, ImgInput[PixelKey][XY])

    elif PixelDataSize == 4:
        def draw_pixel(ImgInput, ImgOutput, XY):
            R, G, B, _A = ImgInput[XY]
            # ImgOutput.putpixel(XY, (R, G, B))
            ImgOutput.im.putpixel(XY, (R, G, B))

    Ytop = min(ImgTargetHeight, ImgSrcHeight, Yto)
    Xtop = min(ImgTargetWidth, ImgSrcWidth, Xto)
    #print("Ytop:", Ytop, "   Xtop:", Xtop)
    RangeCanvasHeight = range(Yfrom, Ytop)

    TimeStart = time.time()
    for X in range(Xfrom, Xtop):
        for Y in RangeCanvasHeight:
            draw_pixel(ImgSrc, ImgTarget, (X, Y) )

    TimeEnd = time.time() - TimeStart
    print("render time:", TimeEnd)


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


def image_file_load(Prg, Path, ThumbnailSize=None, PixelReturn=False):
    if not os.path.isfile(Path):
        Msg = util.ui_msg(Prg, "file_operation.file_missing", PrintInTerminal=True)
        Prg["Warning"].append(Msg)
        return False

    Img = Image.open(Path)
    if ThumbnailSize:
        Img.thumbnail(ThumbnailSize)

    if PixelReturn:
        return Img.load()

    return Img

def image_file_load_to_tk(Prg, Path, ThumbnailSize=None):
    return ImageTk.PhotoImage(image_file_load(Prg, Path, ThumbnailSize=ThumbnailSize))
