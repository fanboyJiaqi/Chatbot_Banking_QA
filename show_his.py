import pandas as pd

file_path = "Final_Project/chat_history.csv"
df = pd.read_csv(file_path)
people = ""
bot = ""

def show_history(data):
    for idx, row in data.iterrows():
        ques, ans = row["Câu hỏi"], row["Câu trả lời"]
    return ques, ans
people, bot = show_history(df)
print(people + "||" + bot)