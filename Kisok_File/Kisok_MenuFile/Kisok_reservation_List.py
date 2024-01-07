import tkinter as tk
from tkinter import messagebox as box
import json
import tkinter.simpledialog as sd


class ReservationList:
    def __init__(self, menu):
        self.menu = menu

        # 예약 정보 파일 경로
        self.reservation_file_path = "reservation_data.json"
        # 프로그램 시작 시 저장된 예약 정보 불러오기
        self.load_reservation_data()
    
    #예약 리스트 코드 함수 (예약 리스트)
    def reservation_list_button_click(self):
        # 관리자 암호 확인 창 표시
        admin_password = self.show_admin_password_dialog()
        if admin_password == "admin":
            # 암호가 일치하면 예약 리스트 창을 엽니다.
            ReservationListWindow(self.menu, self.reservation_list)
        else:
            box.showwarning("[경고]", "잘못된 암호입니다.")
    
    #예약 리스트 클릭 시 관리자 암호 입력화면
    def show_admin_password_dialog(self):
        # 관리자 암호를 입력받는 다이얼로그 표시
        admin_password = sd.askstring("관리자 암호", "관리자 암호를 입력하세요:", show='*')
        return admin_password
    
    # json 파일에서 데이터 불러오기
    def load_reservation_data(self):
        try:
            with open(self.reservation_file_path, "r") as file:
                # 파일의 각 줄을 읽어와서 JSON 형식으로 파싱하고 리스트에 추가
                self.reservation_list = [json.loads(line) for line in file]
        except FileNotFoundError:
            # 저장된 파일이 없는 경우 새로운 빈 리스트 생성
            self.reservation_list = []
    
    
# 새로운 창에 예약 리스트를 표시하는 클래스 (예약 리스트에서 실행되는 클래스)
class ReservationListWindow(tk.Toplevel):
    def __init__(self, master, reservation_list):
        super().__init__(master)
        self.title("예약 리스트 확인")
        self.geometry("300x300")

        self.reservation_list = reservation_list

        self.create_widgets()

    def create_widgets(self):
        label_title = tk.Label(self, text="예약 리스트")
        label_title.pack(pady=10)

        for i, reservation_info in enumerate(self.reservation_list, start=1):
            label_name = tk.Label(self, text=f"{i}. 예약자명: {reservation_info['이름']}")
            label_name.pack()

            label_phone = tk.Label(self, text=f"   휴대폰 번호: {reservation_info['휴대폰번호']}")
            label_phone.pack()