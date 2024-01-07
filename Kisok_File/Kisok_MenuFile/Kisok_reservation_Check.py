import tkinter as tk
from tkinter import messagebox as box
import json
from tkinter import ttk

class ReservationCheck:
    def __init__(self, menu):
        self.menu = menu
        self.reservation_check_Frame = ttk.Frame(menu)  # 예약확인화면
        self.check_phone_var = tk.StringVar()  # 예약 확인 화면에서 번호 입력할 때 사용하는 변수
        self.check_phone_entry = None  # 예약 확인 화면의 휴대폰 번호 Entry 위젯을 저장할 변수
        self.confirm_check_button = None  # 예약 확인 화면의 확인 버튼을 저장할 변수

        # 프로그래스바
        self.progressbar = None

        #json 파일경로
        self.reservation_file_path = "reservation_data.json"

        # 프로그램 시작 시 저장된 예약 정보 불러오기
        self.load_reservation_data()

    #예약 화면 코드 함수 (예약 확인)
    def show_check_reservation_screen(self):
        result = box.askyesno("[알림]", "예약 확인을 하시겠습니까?.")
        
        if result is True:
            check_reservation_window = tk.Toplevel(self.menu)
            check_reservation_window.title("예약 확인")
            check_reservation_window.geometry("300x150")

            self.current_screen = self.reservation_check_Frame
            self.current_screen.pack()
            self.create_check_reservation_widgets(check_reservation_window)
        
        #프로그래스바
        self.progressbar = ttk.Progressbar(check_reservation_window, mode="indeterminate")
        self.progressbar.pack(pady=10) #pady: 프로그래스바와 예약 버튼 사이 간격 조절 

     #예약 확인 클릭 후 "YES"를 선택하면 위젯 출력
    def create_check_reservation_widgets(self, check_reservation_window):
        # 휴대폰 번호 입력 필드 및 라벨 생성
        phone_label = tk.Label(check_reservation_window, text="휴대폰 번호:")
        phone_label.pack()

        #예약의 휴대폰 번호와 예약 확인의 휴대폰 번호가 같이 입력되는 버그를 방지      
        self.check_phone_entry = ttk.Entry(check_reservation_window, textvariable=self.check_phone_var)
        self.check_phone_entry.pack()
        
        # 확인 버튼 생성
        self.confirm_check_button = ttk.Button(check_reservation_window, text="예약 확인", padding=(10, 10), width=15, command=lambda: self.progressBarStart(check_reservation_window))
        self.confirm_check_button.pack(pady=10)

    #예약 확인 버튼 클릭하면 프로세스바 작동 시작
    def progressBarStart(self, check_reservation_window):
        self.progressbar.start(20)
        # 2초 후에 프로그래스바 중지 및 예약 정보 확인 창 표시
        check_reservation_window.after(2000, lambda: self.process_reservation(check_reservation_window))

    #Entry에 전화번호가 입력이 되었는지 확인하는 함수.
    def process_reservation(self, check_reservation_window):
        # 전화번호 확인
        phone_to_check = self.check_phone_var.get()
        self.check_phone_var.set("")
        if not phone_to_check: #입력된 전화번호가 없으면 if문 실행
            box.showwarning("[경고]", "휴대폰 번호를 입력하세요.")
            return
        #입력된 전화번호가 있으면 show_reservation_info_window 함수로 값 전달
        self.show_reservation_info_window(check_reservation_window, phone_to_check)
    
    #입력된 전화번호로 예약이 되어있는지, 예약이 되어있지 않은지 확인하는 함수
    def show_reservation_info_window(self, check_reservation_window, phone_to_check):
        # 프로그래스바 중지
        self.progressbar.stop()

        found_reservation = False
        for reservation_info in self.reservation_list: #예약에서 입력했던 정보를 리스트에 추가하였는데 그 리스트를 info에 저장
            if reservation_info["휴대폰번호"] == phone_to_check: #info에 저장되어 있는 정보와 휴대폰 번호와 일치하는 정보가 있는지 확인
                # 일치하는 예약 정보를 새 창에 표시
                ReservationInfoWindow(check_reservation_window, reservation_info) #일치하는 정보가 있으면 새 창을 띄어준다.
                found_reservation = True
                return

        if not found_reservation:
            box.showinfo("[알림]", "일치하는 예약 정보가 없습니다.")

    # json 파일에서 데이터 불러오기
    def load_reservation_data(self):
        try:
            with open(self.reservation_file_path, "r") as file:
                # 파일의 각 줄을 읽어와서 JSON 형식으로 파싱하고 리스트에 추가
                self.reservation_list = [json.loads(line) for line in file]
        except FileNotFoundError:
            # 저장된 파일이 없는 경우 새로운 빈 리스트 생성
            self.reservation_list = []

# 새로운 창에 예약 정보를 표시하는 클래스 (예약 확인에서 실행되는 클래스)
class ReservationInfoWindow(tk.Toplevel):
    def __init__(self, master, reservation_info):
        super().__init__(master)
        self.title("예약 정보 확인")
        self.geometry("300x150")

        self.reservation_info = reservation_info

        self.create_widgets()

    def create_widgets(self):
        label_name = tk.Label(self, text=f"예약자명: {self.reservation_info['이름']}")
        label_name.pack(pady=10)

        label_phone = tk.Label(self, text=f"휴대폰 번호: {self.reservation_info['휴대폰번호']}")
        label_phone.pack(pady=10)

    