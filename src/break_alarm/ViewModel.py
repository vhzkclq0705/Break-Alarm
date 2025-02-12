import time
import threading
import datetime
import pytz
import pygame
import streamlit as st
from pathlib import Path

# 현재 파일 (ViewModel.py)의 절대 경로를 기준으로 mp3 파일 경로 설정
BASE_DIR = Path(__file__).resolve().parent  # 현재 `ViewModel.py`가 있는 폴더
ALERT_SOUND = BASE_DIR / "Alarm_Remix.mp3"  # `Alarm_Remix.mp3` 파일의 경로

print(f"🔊 MP3 파일 경로: {ALERT_SOUND}")  # 디버깅용 출력

# 파일 존재 여부 확인
if not ALERT_SOUND.exists():
    raise FileNotFoundError(f"MP3 파일을 찾을 수 없습니다: {ALERT_SOUND}")

class ViewModel:
    def __init__(self):
        # 실행 중인지 상태 저장 (세션 상태 초기화)
        if "running" not in st.session_state:
            st.session_state.running = False
        
        # running 변수 추가 (스레드에서 직접 사용)
        self.running = st.session_state.running

        # 음악 재생을 위한 pygame 초기화
        pygame.mixer.init()

    def get_korea_time(self):
        """현재 한국(서울) 시간 반환"""
        KST = pytz.timezone("Asia/Seoul")
        return datetime.datetime.now(KST)

    def is_working_hours(self):
        """현재 시간이 알림이 울릴 시간대인지 확인 (한국 시간 기준)"""
        now = self.get_korea_time()
        weekday = now.weekday()  # 0=월요일, 4=금요일
        hour = now.hour
        minute = now.minute

        # 평일(월~금) & 특정 시간대 (9:50~12:50, 14:50~17:50)
        return 0 <= weekday <= 4 and (
            (9 <= hour < 13 and minute == 50) or (14 <= hour < 18 and minute == 50)
        )

    def play_alert(self):
        """반복적으로 알림을 실행하는 함수 (백그라운드 스레드)"""
        while self.running:  # session_state 대신 self.running 사용
            if self.is_working_hours():
                try:
                    pygame.mixer.music.load(str(ALERT_SOUND))  # 경로를 문자열로 변환 후 로드
                    pygame.mixer.music.play()
                except Exception as e:
                    print(f"🔴 알람 재생 오류: {e}")
                finally:
                    time.sleep(60)  # 1분 대기 (50분마다 실행되도록)
            else:
                time.sleep(30)  # 30초마다 체크하여 조건이 맞으면 실행

    def stop_alert(self):
        """실행 중인 알림을 종료하는 함수"""
        self.running = False
        st.session_state.running = False  # UI에서 상태 반영
        pygame.mixer.music.stop()

    def start_alert(self):
        """알림 실행 (백그라운드 스레드 시작)"""
        print("현재 상태:", self.running)  # 현재 상태 확인
        if not self.running:
            self.running = True
            st.session_state.running = True  # UI에서 상태 반영
            thread = threading.Thread(target=self.play_alert, daemon=True)
            thread.start()
            return True
        else:
            return False
