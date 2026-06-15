import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import urllib.parse

# 1. 設定 Gemini AI 金鑰 (請換成你自己的金鑰)
# 1. 設定 Gemini AI 金鑰 (改用 Streamlit 安全密鑰機制，不寫死在代碼中)
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

# 2. 網頁質感優化
st.set_page_config(page_title="商業 AI 輿情雷達", page_icon="📡", layout="centered")

st.title("📡 商業 AI 輿情監測與情報控制台")
st.write("輸入任何商業關鍵字，系統將自動橫掃全網最新數據，並由 AI 產出核心決策報告。")
st.markdown("---")

# 3. 變現核心：讓客戶自己輸入關鍵字
keyword = st.text_input("🔍 請輸入你想監測的商業關鍵字：", placeholder="例如：台積電、台北房價、電動車趨勢...")

st.markdown("---")

if st.button("🚀 啟動全網搜刮與 AI 深度分析", type="primary"):
    if not keyword:
        st.warning("請先輸入關鍵字才能進行搜刮！")
    else:
        with st.spinner(f"正在全網搜刮關於『{keyword}』的最新情報..."):
            
            # 4. 強大的即時搜尋引擎介接 (Google News RSS)
            encoded_keyword = urllib.parse.quote(keyword)
            url = f"https://news.google.com/rss/search?q={encoded_keyword}&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
            
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, "html.parser")
                items = soup.find_all("item") # 抓取所有的資料節點
                
                titles = []
                links = []
                
                # 只拿前 8 則最新最相關的資料
                for item in items[:8]:
                    title_tag = item.find("title")
                    link_tag = item.find("link")
                    if title_tag:
                        titles.append(title_tag.text)
                    if link_tag:
                        links.append(link_tag.text)
                
                if not titles:
                    st.warning(f"搜尋完畢，但目前網路上似乎沒有關於『{keyword}』的即時新聞。")
                else:
                    st.success(f"🎯 成功擷取 {len(titles)} 則關於『{keyword}』的即時情報！")
                    
                    # 5. 餵給 AI 大腦進行商業提煉
                    with st.spinner("AI 正在解構數據，編寫決策報告..."):
                        all_titles_text = "\n".join([f"- {t}" for t in titles])
                        
                        prompt = f"""
                        你是一位身價百萬的頂尖商業戰略顧問。
                        請針對以下關於『{keyword}』的最新市場情報進行深度分析：
                        {all_titles_text}
                        
                        請用非常專業、精煉的繁體中文，為老闆提供以下結構的報告：
                        1. 【今日核心趨勢總結】(約 60 字，一針見血指出當前局面)
                        2. 【潛在的商業風險或機會】(條列式 2 點，指出這對企業有何影響)
                        3. 【具體行動建議】(條列式 2 點，告訴老闆下一步該怎麼做)
                        """
                        
                        model = genai.GenerativeModel('gemini-2.5-flash')
                        response = model.generate_content(prompt)
                        
                        # 噴出慶祝氣球並顯示結果
                        st.balloons()
                        st.subheader(f"📊 『{keyword}』商業決策報告")
                        st.info(response.text)
                        
                        # 摺疊顯示原始來源，增加專業度
                        with st.expander("🔗 查看今日情報來源連結"):
                            for t, l in zip(titles, links):
                                st.markdown(f"[{t}]({l})")
                                
            except Exception as e: 
                st.error(f"系統執行失敗，請聯絡開發者。錯誤代碼: {e}") 