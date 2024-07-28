import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from code_lienquan import read_data

# Tải biến môi trường từ tệp .env
load_dotenv()

# Lấy khóa API từ biến môi trường
google_api_key = os.getenv("GOOGLE_API_KEY")
langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
os.environ['OPENAI_API_KEY'] = google_api_key
# Cài đặt tiêu đề
st.title("Chatbot")

# Khởi tạo biến để lưu trữ lịch sử trò chuyện
conversation_history = []

# Khởi tạo hoặc tải lịch sử tin nhắn
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
bot_response = ""

# Đọc file CSV
df = pd.read_csv('chat_history.csv')

# Hiển thị dữ liệu
for index, row in df.iterrows():
    st.write(f"Người dùng: {row['Câu hỏi']}")
    st.write(f"Bot: {row['Câu trả lời']}")
    
    
# Hàm xử lý tin nhắn
def process_message(message):
    # Thêm tin nhắn mới vào lịch sử trò chuyện
    conversation_history.append(f"Bạn: {message}")
    
    ketqua = read_data(message)

    # Thêm tin nhắn trả lời vào lịch sử trò chuyện
    conversation_history.append(f"{ketqua}")

    # Hiển thị lịch sử trò chuyện
    for message in conversation_history:
        st.write(message)
    return conversation_history[1]

# Tạo một hàm để cập nhật trạng thái submit
def submit_form():
    st.session_state.submit = True

# Kiểm tra nếu không có key submit trong session_state, đặt mặc định là False
if "submit" not in st.session_state:
    st.session_state.submit = False  
    

    
# Hộp văn bản để nhập tin nhắn
# Tạo một form
with st.form(key='my_form_input'):
    user_input = st.text_input("Nhập gì đó:", value="", key="user_input")
    submit_button = st.form_submit_button(label='Gửi', on_click=submit_form)
# Nút đính kèm tệp
file_upload = st.file_uploader("", type=['txt', 'pdf', 'docx'], label_visibility="collapsed")
# Nút gửi tin nhắn
if submit_button or st.session_state.submit:
    # Xử lý tin nhắn khi người dùng nhấp vào nút gửi
    bot_response = process_message(user_input)
    # Lưu câu hỏi và câu trả lời vào file CSV
    # Đầu tiên, đọc dữ liệu hiện tại từ file CSV (nếu tồn tại)
    try:
        df = pd.read_csv('chat_history.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Câu hỏi", "Câu trả lời"])
    
    # Thêm câu hỏi và câu trả lời mới vào DataFrame
    new_data = pd.DataFrame({"Câu hỏi": [user_input], "Câu trả lời": [bot_response]})
    df = pd.concat([df, new_data], ignore_index=True)
    
    # Lưu DataFrame vào file CSV
    df.to_csv('chat_history.csv', index=False)
    
    # Reset submit trạng thái và làm trống input
    st.session_state.submit = False