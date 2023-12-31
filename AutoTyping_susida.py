import os
import numpy as np
from PIL import Image
import pyocr
import pyautogui
from tempfile import NamedTemporaryFile
import time
import keyboard 

DEBUG = False
EXMODE =False

def add_margin(pil_img, top, right, bottom, left, color):
    """
    画像に指定したサイズの余白を追加する関数
    """
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result

def cleanup(temp_files):
    """
    プログラム終了時に一時ファイルを削除する関数
    """
    for file in temp_files:
        try:
            os.remove(file)
        except Exception as e:
            print(f"Error removing {file}: {e}")


# Tesseract OCRの設定
pyocr.tesseract.TESSERACT_CMD = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# 利用可能なOCRツールの取得
tools = pyocr.get_available_tools()
tool = tools[0]

# 入力スピードを調整するための遅延時間（秒）
input_delay = 0.00

# プログラム起動前のカウントダウン
print("プログラム起動中。ゲームを開始して下さい。その際ウィンドウをフォアグラウンドにして下さい。")
countdown_duration = 10

for i in range(countdown_duration, 0, -1):
    print(f"プログラム起動まで {i} 秒...")
    time.sleep(1)

print("プログラム起動完了。")

# 一時ファイルの管理用リスト
temp_files = []
max_count = 1000


# メインループ
for i in range(max_count): 
     # Escキーが押されたか監視
    if keyboard.is_pressed('esc'):  # <- Escキーを監視
        print("Escキーが押されたため、プログラムを終了します。")
        break  # <- ループを終了

    x, y = pyautogui.position()
    print(f"現在のループ番号: {i+1}/{max_count}  現在のマウス座標: {x}, {y}")

    # スクリーンショットの撮影(x, y, width, height)
    with NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:  
        temp_files.append(tmp.name)
        photo = pyautogui.screenshot(region=(240, 468, 400, 38))
        photo.save(tmp.name)

        if DEBUG:
            import matplotlib.pyplot as plt
            # スクリーンショットの撮影(x, y, width, height)
            photo = pyautogui.screenshot(region=(220, 468, 420, 38))

            # 画像の表示
            plt.imshow(photo)
            plt.axis('off')  # 軸を非表示にする
            plt.show()

        # 画像の前処理
        img = Image.open(tmp.name).convert('RGB')
        np_img = np.array(img)

        border = 110
        mask = np_img < border
        np_img[mask] = 0  # Redチャンネルを0に設定
        np_img[mask] = 10  # Greenチャンネルを10に設定
        np_img[mask] = 0  # Blueチャンネルを0に設定

        img2 = Image.fromarray(np_img)
        img2.save(tmp.name)

        im = Image.open(tmp.name)
        im_new = add_margin(im, 35, 35, 50, 50, (0, 0, 0))
        im_new.save(tmp.name)

        img3 = Image.open(tmp.name)

        # OCRによるテキスト認識
        builder = pyocr.builders.TextBuilder(tesseract_layout=3)
        text = tool.image_to_string(img3, lang="eng", builder=builder)
        lines = text.split("\n")

        print(f"認識されたテキスト: {lines}")


        if EXMODE:
            # テキストの入力(本気モード)
            pyautogui.typewrite(text, interval=input_delay)
        else:
            # テキストの入力(人間モード)
            for char in text:
                pyautogui.typewrite(char, interval=input_delay)
