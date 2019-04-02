import os
import sys
import shutil
from datetime import datetime
from enum import Enum, auto

import tkinter, tkinter.filedialog
from PIL import Image
import cv2

Face_ICON_FILE = "smile.png"
CASCADE_FILE = "data/haarcascades/haarcascade_frontalface_default.xml"

class Mode(Enum):
    BLG = auto() #ブログ用
    TMB = auto() # サムネイル用

def mask_face(img_cv, cascade, img_pil, mask):
    # 顔認識を実行
    faces = cascade.detectMultiScale(img_cv, scaleFactor=1.5)
    
    #認識された顔にアイコンを貼り付け
    for(x, y, w, h) in faces:
        mask = mask.resize((w, h))
        img_pil.paste(mask, (x,y), mask)





# メイン処理
# 顔アイコンの画像読み込み
face_icon = Image.open(Face_ICON_FILE)

# 識別器の生成
cascade = cv2.CascadeClassifier(CASCADE_FILE)

# 元画像フォルダの選択
root = tkinter.Tk()
root.withdraw()
msg = "画像フォルダを選択してください"
img_dir_path = tkinter.filedialog.askdirectory(titile=msg)
if (not img_dir_path):
    print("フォルダを選択してください")
    sys.exit()

# 出力先フォルダの選択
msg = "出力先のフォルダを選択してください"
output_dir_path = tkinter.filedialog.askdirectory(title=msg)
if (not img_dir_path):
    print("フォルダを選択してください")
    sys.exit()

# 元画像フォルダ内の画像を１つずつ処理
for img_file in os.listdir(img_dir_path):
    #元画像の読み込み
    img_path = os.path.join(img_dir_path, img_file)
    img_pil = Image.open(img_path)

    # 顔認識用にグレースケール化
    img_cv = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    #顔を隠す
    mask_face(img_cv, cascade, img_pil, face_icon)

    # ファイルの移動先フォルダー作成
    output_path = mkdir_dto(img_pil, output_dir_path)

    # ファイル名に文字列を付加して保存

    # 元画像（PIL）を閉じる
    img_pil.close()

    # 元画像を移動
    shutil.move(img_path, output_path)
