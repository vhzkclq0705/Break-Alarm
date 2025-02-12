import time
import threading
import datetime
import pytz
import pygame

# 알림 사운드 파일
ALERT_SOUND = "Alarm_Remix.mp3"

class ViewModel:
    def __init__(self):
        # 실행 중인지 상태 저장
        self.running = False
        
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
        if 0 <= weekday <= 4:
            if (9 <= hour < 13 and minute == 50) or (14 <= hour < 18 and minute == 50):
                return True
        return False

    def play_alert(self):
        """반복적으로 알림을 실행하는 함수 (백그라운드 스레드)"""
        while self.running:
            if self.is_working_hours():
                try:
                    pygame.mixer.music.load(ALERT_SOUND)
                    pygame.mixer.music.play()
                except Exception as e:
                    print(str(e))
                finally:
                    # 1분 대기 (50분마다 실행되도록)
                    time.sleep(60)
            else:
                # 30초마다 체크하여 조건이 맞으면 실행
                time.sleep(30)

    def stop_alert(self):
        """실행 중인 알림을 종료하는 함수"""
        self.running = False
        pygame.mixer.music.stop()

    def start_alert(self):
        """알림 실행 (백그라운드 스레드 시작)"""
        if not self.running:
            self.running = True
            thread = threading.Thread(target=self.play_alert, daemon=True)
            thread.start()
            return True
        else:
            return False