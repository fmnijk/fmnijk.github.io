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
    lnks = []


def get_all_shortcuts_map():
    """獲取檔案與所有捷徑可能存在的映射關係
    返回格式: {目標檔案路徑: [捷徑路徑1, 捷徑路徑2, ...]}
    """
    lnk_directory = "D:\\H\\gallery-dl精選\\0"  # 固定路徑
    target_to_lnks = {}
    
    if not os.path.exists(lnk_directory):
        print(f"捷徑目錄不存在：{lnk_directory}")
        return target_to_lnks
    
    # 獲取所有lnk檔案
    lnk_files = []
    for root, dirs, files in os.walk(lnk_directory):
        for file in files:
            if file.endswith('.lnk'):
                lnk_files.append(os.path.join(root, file))
    
    # 讀取每個lnk檔案的目標路徑
    for lnk_path in lnk_files:
        try:
            shortcut = winshell.Shortcut(lnk_path)
            target_path = shortcut.path
            
            if target_path not in target_to_lnks:
                target_to_lnks[target_path] = []
            target_to_lnks[target_path].append(lnk_path)
        except Exception as e:
            input(f"讀取捷徑 {lnk_path} 時出錯: {str(e)} 請按 Enter 繼續...")
    
    return target_to_lnks


def prepare(args):
    """preprocessing before fold or unfold"""
    if not args.s:
        args.s = os.getcwd()

    join = os.path.join

    start = 1
    s = args.s
    files = listimageonly(s)
    
    # 獲取所有捷徑
    shortcuts_map = get_all_shortcuts_map()
    
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
        
        # 檢查是否有捷徑指向這個檔案
        if element.src in shortcuts_map:
            element.lnks = shortcuts_map[element.src]

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


def edit_lnk(lnk_path, new_target_path):
    """
    修改捷徑的目標路徑和工作目錄
    
    參數:
        lnk_path: 捷徑的路徑
        new_target_path: 新的目標路徑
    """
    try:
        shortcut = winshell.Shortcut(lnk_path)
        
        # 修改目標路徑
        shortcut.path = new_target_path
        
        # 修改工作目錄為新目標的父目錄
        from pathlib import Path
        shortcut.working_directory = str(Path(new_target_path).parent)
        
        # 儲存修改
        shortcut.write()
        
        return True
    except Exception as e:
        input(f"更新捷徑 {lnk_path} 時出錯: {str(e)} 請按 Enter 繼續...")
        return False


def fold(filelist):
    """fold or unfold file name"""
    before = len(os.listdir())
    
    # 追蹤已更新的捷徑數量
    shortcut_updates = 0
    
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
                    # 重命名檔案
                    old_path = f.tmp if f.tmp else f.src
                    os.rename(old_path, f.dst)
                    print("src:{} dst:{}".format(f.src, f.dst))
                    
                    # 更新捷徑
                    if f.lnks:
                        for lnk_path in f.lnks:
                            if edit_lnk(lnk_path, f.dst):
                                shortcut_updates += 1
                                print(f"更新捷徑: {lnk_path} -> {f.dst}")
                except Exception as e:
                    print(f"重命名檔案時出錯: {str(e)}")
                    continue
                f.finished = True
        if any(f.finished for f in filelist):
            tries = 0
            filelist = [f for f in filelist if not f.finished]
        else:
            tries = 1
    
    after = len(os.listdir())
    print("運行前", before, "個檔案")
    print("運行後", after, "個檔案")
    if before != after:
        input("檔案數量改變，可能有問題，請按 Enter 繼續...")
    else:
        print("檔案數量沒問題。")
    # 報告更新的捷徑數量
    print(f"已更新 {shortcut_updates} 個捷徑，指向重命名後的檔案")

if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    fold(prepare(args))


# 編譯指令
# pyinstaller --onefile fold.py
