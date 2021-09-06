# -*- coding: utf-8 -*-
import util, os, time, mark_collect

PrgGlobal = None
ErrorsLocal = list()

try:
    import tkinter as Tkinter
    import tkinter.filedialog as FileDialog
except ImportError:
    util.error_display("install.missing.module_tkinter - search this key from ui_messages.json", "ui_tkinter, tkinter/filedialog import")

try:
    from PIL import Image
except ImportError:
    util.error_display("install.missing.module_pillow - search this key from ui_messages.json", "ui_tkinter, Image import")

try:
    from PIL import ImageTk
except ImportError:
    util.error_display("install.missing.package_ImageTk - search this key from ui_messages.json", "ui_tkinter, ImageTk import")


def window_main(Prg):
    # store passed Prg as a global variable, too, because Tkinter buttons need a state
    # I collect the msg NOT in the if because if one of them is missing, it causes Error
    global PrgGlobal
    PrgGlobal = Prg

    Prg["Tkinter"] = dict()

    MainWidth = 1200
    MainHeight = 800
    SourceWidth = 300
    OnePageWidth = 600

    Window = window_new(Prg, "window.main.title")
    Window.geometry('{}x{}'.format(MainWidth, MainHeight))
    Prg["Tkinter"]["Window"] = Window

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

    Tkinter.Button(OnePageFrame, text=util.ui_msg(Prg, "ocr.page_current_analyse"),
                   command=marks_collect_from_page).pack()

    TextSelectPreviewImg = Image.new("RGB", Prg["UiTextSelectPreviewSize"], color="grey")
    Prg["Tkinter"]["OnePageTextSelectPreviewImgLoaded"] = None
    Prg["Tkinter"]["OnePageTextSelectPreviewImgRendered"] = TextSelectPreviewImg


    ImageTkPhotoImage = ImageTk.PhotoImage(TextSelectPreviewImg)
    Label = Tkinter.Label(OnePageFrame, image=ImageTkPhotoImage)
    Prg["Tkinter"]["OnePageTextSelectPreviewLabel"] = Label
    Label.pack()
    ##### Text Select Preview #################



    Tkinter.Button(FrameThumbnails, text=util.ui_msg(Prg, "file_operation.file_load_into_thumbnail_list"),
                   command=files_thumbnails_load_button_cmd).pack()

    Window.mainloop()


def files_thumbnails_load_button_cmd():  # it is called from Ui so we use global state to store objects.
    Prg = PrgGlobal
    Parent = Prg["Tkinter"]["FrameThumbnails"]

    for FileSelectedPath in files_selector(Prg):
        ImageTkPhotoImageThumbnail = image_file_load_to_tk(Prg, FileSelectedPath, Prg["UiThumbnailSize"])

        if ImageTkPhotoImageThumbnail:

            PixelsPreviewImg = image_file_load(Prg, FileSelectedPath, Prg["UiTextSelectPreviewSize"])
            PixelsPreview = PixelsPreviewImg.load()

            ImgId = util.img_generate_id_for_loaded_list(Prg, PreFix="thumbnail", PostFix=FileSelectedPath)
            util.img_load_into_prg_structure(Prg, FileSelectedPath, ImgId,
                                             PixelsPreview = PixelsPreview,
                                             PixelsPreviewImg=PixelsPreviewImg,
                                             ImageTkPhotoImageThumbnail = ImageTkPhotoImageThumbnail
            )

            Panel = Tkinter.Label(Parent, image=ImageTkPhotoImageThumbnail)
            Panel.pack()
            Panel.bind("<Button-1>", lambda Event: thumbnail_click_left_mouse(Prg, ImgId))

def thumbnail_click_left_mouse(Prg, ImgId):
    ImgLoaded = Prg["ImagesLoaded"][ImgId]
    Prg["Tkinter"]["OnePageTextSelectPreviewImgLoaded"] = ImgLoaded
    Prg["ImageIdSelected"] = ImgId

    # start with a new, empty canvas
    ImgTextSelectPreview = Image.new("RGB", Prg["UiTextSelectPreviewSize"], color="grey")

    img_redraw(ImgLoaded["TextSelectPreviewPixels"],
               ImgTextSelectPreview,
               ImgSrcWidth     = ImgLoaded["TextSelectPreviewPixelsWidth"],
               ImgSrcHeight    = ImgLoaded["TextSelectPreviewPixelsHeight"],
               ImgTargetWidth  = Prg["UiTextSelectPreviewSize"][0],
               ImgTargetHeight = Prg["UiTextSelectPreviewSize"][1],
               PixelDataSize   = ImgLoaded["PixelDataSize"],
               )
    text_select_preview_coords_draw(Prg, ImgLoaded, ImgTextSelectPreview,
                                    ParentLabelToRefresh=Prg["Tkinter"]["OnePageTextSelectPreviewLabel"])
    # TODO: detect mouse position and buttons to add/remove text selection frames

def text_select_preview_coords_draw(Prg, ImgLoaded, ImgTextSelectPreview, ParentLabelToRefresh=None):
    for Coords in ImgLoaded["TextSelectCoords"]:
        print(Coords)
        for Coord in Coords:
            ImgTextSelectPreview.im.putpixel(Coord, Prg["Color"]["TextSelectFrame"])
        img_parent_label_refresh(ParentLabelToRefresh, ImgTextSelectPreview)


def img_redraw(ImgSrc,              ImgTarget,
               ImgTargetWidth=1,    ImgTargetHeight=1,
               ImgSrcWidth=1,       ImgSrcHeight=1,
               Xfrom=0,             Xto=999999,
               Yfrom=0,             Yto=999999,
               PixelDataSize=3,     ParentLabelToRefresh=None):

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

    img_parent_label_refresh(ParentLabelToRefresh, ImgTarget)

def img_parent_label_refresh(ParentLabel, Img):
    if ParentLabel:
        ImageTkPhotoImage = ImageTk.PhotoImage(Img)
        ParentLabel.configure(image=ImageTkPhotoImage)
        ParentLabel.imageSaved = ImageTkPhotoImage

def files_selector(Prg):
    Dir = Prg["DirDefaultFileSelectPath"]
    print(Dir)
    return FileDialog.askopenfilenames(initialdir=Prg["DirDefaultFileSelectPath"], title="Select file",
                                       filetypes=(
                                       ("png files", "*.png"), ("jpeg files", "*.jpg"), ("all files", "*.*")))


def frame_new(Prg, Parent, Width, Height, bg=""):
    return Tkinter.Frame(Parent, bg=bg, width=Width, height=Height, pady=3)


def window_new(Prg, TitleKey=""):
    Window = Tkinter.Tk()
    if TitleKey:
        Window.title(util.ui_msg(Prg, TitleKey))
    return Window

def image_file_load_to_tk(Prg, Path, ThumbnailSize=None):
    return ImageTk.PhotoImage(image_file_load(Prg, Path, ThumbnailSize=ThumbnailSize))

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


def marks_collect_from_page():
    Prg = PrgGlobal
    # first we implement a naive algorithm:
    # Simple paragraphs on white paper
    # without any different text blocks backgrounds
    mark_collect.text_block_analyse(Prg)
