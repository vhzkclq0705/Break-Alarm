import streamlit as st
from src.break_alarm.ViewModel import ViewModel

# --View Model--
view_model = ViewModel()

# --UI--
st.title("🔔 쉬는시간 알림 시스템")
is_tapped_play_button = st.button("▶️ 알림 시작")
is_tapped_stop_button = st.button("⏹️ 음악 중지")

# --Logic--

if is_tapped_play_button:
    if view_model.start_alert():
        st.success("🔔 알림이 시작되었습니다!")
    else:
        st.warning("⚠️ 이미 알림이 실행 중입니다.")

if is_tapped_stop_button:
    view_model.stop_alert()
    st.success("🔕 알림이 중지되었습니다.")

