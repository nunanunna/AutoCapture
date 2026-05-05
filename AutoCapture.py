import tkinter as tk
import pyautogui
from PIL import ImageTk
import time
from datetime import datetime

class SnippingTool:
    def __init__(self, root, original_image):
        self.root = root
        self.root.attributes('-fullscreen', True)
        self.root.configure(cursor="cross")
        
        # 캡처한 원본 이미지를 저장하고 tkinter에서 띄울 수 있게 변환
        self.original_image = original_image
        self.tk_image = ImageTk.PhotoImage(self.original_image)
        
        # 캔버스를 만들고, 그 위에 캡처한 이미지를 배경으로 깔아줍니다
        self.canvas = tk.Canvas(self.root, cursor="cross")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)
        
        self.start_x = None
        self.start_y = None
        self.rect = None

        # 마우스 이벤트 바인딩
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, 1, 1, outline='red', width=2
        )

    def on_move_press(self, event):
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        end_x, end_y = (event.x, event.y)
        self.root.destroy()
        
        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)
        
        if x2 - x1 > 0 and y2 - y1 > 0:
            # 새로 화면을 캡처하는 것이 아니라, 아까 찍어둔 원본 이미지에서 해당 영역만 잘라냄(crop)
            cropped_img = self.original_image.crop((x1, y1, x2, y2))
            filename = f"image_{datetime.now().strftime('%Y_%m_%d_%H_%M')}.png"
            cropped_img.save(filename)
            print(f"캡처 완료! {filename} 파일이 저장되었습니다.")
        else:
            print("영역이 지정되지 않아 캡처가 취소되었습니다.")

if __name__ == "__main__":
    print("3초 뒤에 화면을 캡처하고 영역 지정 창을 띄웁니다...")
    print("캡처할 화면을 미리 띄워주세요!")
    time.sleep(3)
    
    # 1. GUI 창을 띄우기 전, DRM에 안 걸리던 순정 방식으로 전체 화면을 조용히 캡처
    screen = pyautogui.screenshot()
    
    # 2. 캡처가 완료된 이미지를 GUI로 띄워서 마우스로 자르기
    root = tk.Tk()
    app = SnippingTool(root, screen)
    root.mainloop()