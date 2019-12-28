
def text_block_analyse( Prg,
                        UserInterface="",
                        PositionStart=(0,0),
                        ColorBlockBackground=(255,255,255),
                        ColorBlockBackgroundDeltaMax=(30,30,30),
                        ScanDirectionHorizontal="from_left_to_righ",
                        ScanDirectionVertical="from_top_to_bottom"
                        ):
    print("Selected Image Id", Prg["ImageIdSelected"])
    ImgObj = Prg["ImagesLoaded"][Prg["ImageIdSelected"]]
    print("Img width, height: ", ImgObj["Width"], ImgObj["Height"])
