import tkinter as tk
from tkinter import messagebox as box
import json
from PIL import Image, ImageTk
from ttkthemes import ThemedTk, ThemedStyle
from tkinter import ttk
from Kisok_MenuFile.Kisok_reservation_Check import ReservationCheck
from Kisok_MenuFile.Kisok_reservation_List import ReservationList

class Kisok_MainMenu:
    def __init__(self, menu):
        #화면 준비
        self.menu = menu
        self.menu.title("숙소 예약 프로그램")
        self.menu.geometry("600x600")
        
        # 이미지를 배경으로 사용할 때 사용할 Label 위젯 생성
        self.background_label = tk.Label(menu)
        self.background_label.place(relwidth=1, relheight=1)

        # 이미지 파일 경로
        image_path = "C:/Users/User/Desktop/image/TestImage.jpg"

        # 원하는 크기로 이미지 크기 조절
        new_size = (600, 600)  # Set your desired size

        # 이미지를 열어서 PIL Image로 변환 및 크기 조절
        img_pil = Image.open(image_path)
        img_pil = img_pil.resize(new_size, Image.ADAPTIVE)

        img = ImageTk.PhotoImage(img_pil)

        # Label의 이미지를 설정
        self.background_label.img = img
        self.background_label.configure(image=self.background_label.img)

        # --화면 바꾸기--
        self.main_Frame = ttk.Frame(menu)  # 메인화면
        self.reservation_Frame = ttk.Frame(menu, relief="solid", style="TFrame", border=2)  # 예약화면

        # 예약자명과 휴대폰 번호를 저장할 변수
        self.reservation_name = tk.StringVar()  # 예약자 이름 저장 (예약 화면에서 사용하는 변수)
        self.reservation_phone = tk.StringVar()  # 예약자 번호 저장

        self.reservation_entry_widgets = None  # 예약 화면의 Entry 위젯을 저장할 변수

        # 예약 정보를 저장할 리스트
        self.reservation_list = []  # 예약 정보를 리스트로 저장

        #reser_c = Kisok_reservation_Check.py의 ReservationCheck클래스로 연결
        self.reser_c = ReservationCheck(menu)

        #reser_l = Kisok_reservation_List.py의 ReservationList클래스로 연결
        self.reser_l = ReservationList(menu)

        self.current_screen = None  # 초기에는 현재 화면이 없음
        self.show_main_screen()  # 기본이 메인화면

        # --------------

        # 예약 정보 파일 경로
        self.reservation_file_path = "reservation_data.json"

        # 프로그램 시작 시 저장된 예약 정보 불러오기
        self.load_reservation_data()

        # 보여지는 메인 화면
        self.mainLabel()
        
        # 예약 버튼 추가
        self.create_button("예약", self.show_reservation_screen)

        # 예약 확인 버튼 추가
        self.create_button("예약 확인", self.reser_c.show_check_reservation_screen)

        # 예약 리스트 확인 버튼 추가
        self.create_button("예약 리스트 확인", self.reser_l.reservation_list_button_click)

        # 종료 버튼 추가
        self.create_button("종료", self.reservation_exit_button_click)

        # 메인 화면에 버튼을 추가하기 위해 레이아웃 매니저 사용
        self.add_buttons_to_main_frame()

    def show_main_screen(self): #메인화면
        self.current_screen = self.main_Frame
        self.current_screen.pack()

    # 예약, 예약 확인, 예약 리스트 확인, 종료 버튼을 가로로 배치
    def add_buttons_to_main_frame(self):
        for widget in self.menu.winfo_children():
            if isinstance(widget, ttk.Button):
                widget.pack(side="left", padx=10, pady=100, anchor="s")

    def create_button(self, text, command): #메인 화면 버튼 함수  
        button = ttk.Button(self.menu, text=text, padding=(10, 10), width=15, command=command, style="TButton")
        button.pack()  # side와 padx 옵션을 사용하여 좌우 정렬 및 간격을 조절합니다.

    def mainLabel(self):  # 메인 화면 안내 함수
        mainlabel = ttk.Label(self.menu, text="숙소 예약프로그램 화면", style="TLabel")
        mainlabel.pack(padx=10, pady=10, anchor="n")

    #예약 코드 함수(예약)
    def show_reservation_screen(self): # 예약 창이 열려 있으면 예약 화면을 숨기고, 아니면 보여줌(예약 화면)
        if self.current_screen == self.reservation_Frame:
            self.current_screen.pack_forget()
            self.current_screen = self.main_Frame
        else:
            # 예약 화면이 생성되지 않았다면 생성 후 표시
            self.reservation_Frame.pack()
            self.current_screen = self.reservation_Frame

        # 예약 화면의 Entry 위젯이 없으면 생성
        if not self.reservation_entry_widgets:
            self.create_reservation_widgets()
            # 예약 화면의 Entry 위젯이 없으면 생성
            if not self.reservation_entry_widgets:
                self.create_reservation_widgets()
        self.current_screen.pack()
    
    #예약을 클릭했을 때 Entry 위젯 나오는 함수(위젯이 닫혀있으면 열고, 열려있으면 닫힘)
    def create_reservation_widgets(self): 
        # 예약자명 입력 필드 및 라벨 생성
        name_label = ttk.Label(self.reservation_Frame, text="예약자명:", background="White") #예약자 명 라벨 출력
        name_label.pack()
        name_entry = ttk.Entry(self.reservation_Frame, textvariable=self.reservation_name, background="White") #예약자 명 엔트리 출력
        name_entry.pack()

        # 휴대폰 번호 입력 필드 및 라벨 생성
        phone_label = ttk.Label(self.reservation_Frame, text="휴대폰 번호:", background="White")
        phone_label.pack()
        phone_entry = ttk.Entry(self.reservation_Frame, textvariable=self.reservation_phone, background="White")
        phone_entry.pack()

        # 확인 버튼 생성
        confirm_button = ttk.Button(self.reservation_Frame, text="확인", padding=(10, 10), width=15, command=self.add_reservation)
        confirm_button.pack(pady=10)

        # Entry 위젯들을 리스트로 저장 (일괄적인 관리, 향후 확장성에 용이)
        self.reservation_entry_widgets = [name_label, name_entry, phone_label, phone_entry, confirm_button]

    #예약 위젯에서 정보 입력 후 확인 버튼을 클릭했을 때 실행되는 함수
    def add_reservation(self):
        name = self.reservation_name.get() #self.reservation_name = tk.StringVar()에 입력된 문자열을 가져오는 코드
        phone = self.reservation_phone.get() #self.reservation_phone = tk.StringVar()에 입력된 문자열을 가져오는 코드

        if name and phone:
            # 동일한 전화번호가 있을 경우 예약 불가.
            if self.check_duplicate_reservation(phone):
                box.showwarning("[경고]", "이미 해당 휴대폰 번호로 예약이 존재합니다.")
                return
            
            reservation_info = {"이름": name, "휴대폰번호": phone} #딕셔너리를 reservation_info 변수에 저장
            self.reservation_list.append(reservation_info) #reservation_info에 있는 정보를 리스트에 추가

            # 확인 메시지 표시 및 입력 창 초기화
            box.showinfo("[알림]", "예약이 완료되었습니다.") 
            self.reservation_name.set("") #확인 클릭 하면 입력된 엔트리가 사라지는 코드
            self.reservation_phone.set("")

            # 예약자명 Entry에 포커스 설정
            self.reservation_entry_widgets[1].focus_set()
            # 예약 정보 파일에 저장
            self.save_reservation_data()
            
            #예약 창 닫아주는 코드
            self.show_reservation_screen()
            
        else:
            box.showwarning("[경고]", "예약 정보가 제대로 입력되지 않았습니다.")

    # 휴대폰 번호가 이미 예약 리스트에 있는지 확인하는 함수 (동일한 전화번호가 있을 경우 예약 불가.)
    def check_duplicate_reservation(self, phone_to_check):
        return any(reservation_info["휴대폰번호"] == phone_to_check for reservation_info in self.reservation_list)
    
    # 예약 정보를 json 파일에 저장
    def save_reservation_data(self):
        with open(self.reservation_file_path, "w") as file:
            for reservation_info in self.reservation_list:
                json.dump(reservation_info, file)
                file.write('\n')
    
    # json 파일에서 데이터 불러오기
    def load_reservation_data(self):
        try:
            with open(self.reservation_file_path, "r") as file:
                # 파일의 각 줄을 읽어와서 JSON 형식으로 파싱하고 리스트에 추가
                self.reservation_list = [json.loads(line) for line in file]
        except FileNotFoundError:
            # 저장된 파일이 없는 경우 새로운 빈 리스트 생성
            self.reservation_list = []

    #프로그램 종료 함수
    def reservation_exit_button_click(self): #프로그램 종료
        result = box.askyesno("[알림]", "프로그램을 종료하시겠습니까?")
        if result is True:
            self.menu.destroy()

if __name__ == "__main__":
    root = ThemedTk(theme="arc")
    style = ThemedStyle(root)
    style.set_theme("adapta")
    app = Kisok_MainMenu(root)
    root.mainloop()