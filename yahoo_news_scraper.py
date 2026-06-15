import csv
import google.generativeai as genai
import streamlit as st

# 1. 填入你的 Gemini API 金鑰
# 1. 設定 Gemini AI 金鑰 (改用 Streamlit 安全密鑰機制，不寫死在代碼中)
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

print("開始讀取之前抓好的新聞資料...")

# 2. 自動讀取我們上一階段存好的 news.csv
titles = []
try:
    with open('titles.csv', mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader) # 跳過第一行的欄位名稱
        for row in reader:
            if row: 
                titles.append(row[0]) # 把標題存進清單中
except FileNotFoundError:
    print("【錯誤】找不到 news.csv 檔案！請確認你剛才是否有成功執行過爬蟲。")
    exit()

# 3. 把所有的標題組裝成一段大文字，準備餵給 AI  
all_titles_text = "\n".join([f"- {title}" for title in titles])

# 4. 設計你的第一個 AI 提示詞 (Prompt)
prompt = f"""
你是一個專業的商業數據分析師。以下是今天剛從網路爬蟲抓取到的熱門新聞標題：
{all_titles_text}

請幫我用大約 50 個字，精準總結出今天的核心重點或社會趨勢。
"""

print("資料組裝完畢！正在將數據送往雲端 Gemini AI 進行深度分析...")

# 5. 呼叫免費又強大的 AI 模型
try:
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    
    print("\n🎯 === AI 智慧新聞趨勢摘要 ===")
    print(response.text)
    print("================================\n")
    print("恭喜！你已經成功完成了一個自動化 AI 數據管線！")
    
except Exception as e:
    print(f"【呼叫 AI 失敗】請檢查 API 金鑰是否填寫正確。錯誤訊息: {e}")