import random
import streamlit as st


def guess_the_number():
    # 세션 상태 초기화
    if 'secret_number' not in st.session_state:
        st.session_state.secret_number = random.randint(1, 100)
        st.session_state.attempts = 0
        st.session_state.game_over = False

    st.title("★ 1부터 100 사이의 숫자를 맞춰보세요! ★")

    if st.session_state.game_over:
        st.write(f"🎉 정답입니다! {st.session_state.secret_number}를 {st.session_state.attempts}번 만에 맞추셨습니다.")
        if st.button("다시 시작"):
            del st.session_state.secret_number
            del st.session_state.attempts
            del st.session_state.game_over
            st.rerun()
        return

    user_input = st.text_input("숫자를 입력하세요: ", key="unique_key")

    if user_input:
        try:
            guess = int(user_input)
            st.session_state.attempts += 1

            if guess < 1 or guess > 100:
                st.write("⚠️ 1부터 100 사이의 숫자만 입력해주세요.")
            elif guess < st.session_state.secret_number:
                st.write("🔺 업 (Up)! 더 큰 숫자입니다.")
            elif guess > st.session_state.secret_number:
                st.write("🔻 다운 (Down)! 더 작은 숫자입니다.")
            else:
                st.session_state.game_over = True
                st.rerun()
        except ValueError:
            st.write("⚠️ 오류: 유효한 숫자를 입력해주세요.")


if __name__ == "__main__":
    guess_the_number()
