import os
import argparse
import natsort
import winshell

def build_parser():
    """Build and configure an ArgumentParser object"""
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION]... SOURCE...",
        add_help=False,
    )

    general = parser.add_argument_group("General Options")
    general.add_argument(
        "-h", "--help",
        action="help",
        help="Print this help message and exit",
    )
    general.add_argument(
        "-q",
        action="store_true",
        help=("Activate quiet mode"),
    )
    general.add_argument(
        "-d",
        type=str,
        help="Destination directory",
    )

    fold = parser.add_argument_group("General Options")
    fold.add_argument(
        "-f",
        action="store_true",
        help="force",
    )
    
    fold.add_argument(
        "-r",
        action="store_true",
        help="reverse",
    )
    
    fold.add_argument(
        "-n",
        action="store_true",
        help="normal sort",
    )

    parser.add_argument(
        "s",
        metavar="s", nargs="?",
        help=argparse.SUPPRESS,
    )

    return parser


def listdironly(dir):
    return next(os.walk(os.path.join(dir, ".")))[1]


def listfileonly(dir):
    return next(os.walk(os.path.join(dir, ".")))[2]


def isimage(filename):
    if not "." in filename:
        return False
    exts = ["jpg", "jpeg", "png", "psd", "gif", "webp", "lnk", "mp4", "mkv" , "webm"]
    ext = filename.split(".")[-1]
    if "!" in filename:
        return False
    if ext.lower() in exts:
        return True
    return False


def listimageonly(dir):
    return natsort.natsorted([name for name in next(os.walk(os.path.join(dir, ".")))[2] if isimage(name)])


class onefile:
    src = None
    dst = None
    tmp = None
    finished = False


def prepare(args):
    """preprocessing before fold or unfold"""
    if not args.s:
        args.s = os.getcwd()

    join = os.path.join

    start = 1
    s = args.s
    files = listimageonly(s)
    
    #foldr
    if args.r:
        files.reverse()
    
    namewidth = len(str(len(files) + start))
    count = len(files)
    output = []

    for i in range(0, count):
        element = onefile()

        filename = files[i]
        ext = filename.split(".")[-1]
        if ext == "jpeg":
            ext = "jpg"
        ext = ext.lower()

        element.src = join(s, filename)

        filename_ = filename.rsplit(".", 1)[0].lstrip(" 0123456789")
        if " " + filename_ in filename:
            filename_ = " " + filename_

        if not filename.isascii():
            if not args.n:
                element.dst = join(s, f"{(i + 1) * 10:>0{min(max(3, namewidth + 1), 4)}}{filename_}.{ext}")
            else:
                #foldn
                element.dst = join(s, f"{(i + 1):>0{max(namewidth, 2)}}{filename_}.{ext}")
        else:
            if not args.n:
                element.dst = join(s, f"{(i + 1) * 10:>0{min(max(3, namewidth + 1), 4)}}.{ext}")
            else:
                #foldn
                element.dst = join(s, f"{(i + 1):>0{max(namewidth, 2)}}.{ext}")
        
        if args.f:
            if not args.n:
                element.dst = join(s, f"{(i + 1) * 10:>0{min(max(3, namewidth + 1), 4)}}.{ext}")
            else:
                #foldn
                element.dst = join(s, f"{(i + 1):>0{max(namewidth, 2)}}.{ext}")
        
        files[i] = element
    return files


def fold(filelist):
    """fold or unfold file name"""
    before = len(os.listdir())
    
    tries = 0
    while filelist:
        for f in filelist:
            if f.finished:
                continue
            if f.src == f.dst:
                f.finished = True
                continue
            if os.path.isfile(f.dst):
                if tries > 0:
                    for i in range(8708050000, 8708050010):
                        tmp = os.path.join(os.path.dirname(f.src), str(i))
                        if os.path.isfile(tmp):
                            continue
                        else:
                            try:
                                os.rename(f.src, tmp)
                                f.tmp = tmp
                            except:
                                continue
                        break
                f.finished = False
                continue
            else:
                try:
                    if f.tmp:
                        os.rename(f.tmp, f.dst)
                    else:
                        os.rename(f.src, f.dst)
                    print("src:{} dst:{}".format(f.src, f.dst))
                except:
                    continue
                f.finished = True
        if any(f.finished for f in filelist):
            tries = 0
            filelist = [f for f in filelist if not f.finished]
        else:
            tries = 1
    
    after = len(os.listdir())
    if before != after:
        print(before, "個項目")
        print(after, "個項目")
        response = input("檔案數量改變，可能有問題，請按 Enter 繼續...")


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    fold(prepare(args))
