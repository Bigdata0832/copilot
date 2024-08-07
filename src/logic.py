from utils.llm.openai_chatCompletion import chat_completion
from utils.llm.openai_assistant import LLMAssistant

def create():
    instruction = """###CONTEXT###
KEYPO是一個輿情分析軟體，可以透過搜索條件來獲得相應的網路文章，你作為KEYPO Copilot，\
能夠回答關於從KEYPO搜索得到的文章中的任何問題，滿足使用者對相關信息的需求。\n
###ABILITY###
你能夠對網路文章進行多種分析操作、內容問答、資訊摘要和洞見分析等，\
在必要的情況，透過Code Interpreter你可以進一步有效的分析為使用者分析當前網路文章的更多統計資訊
"""
    obj = LLMAssistant()
    assistant = obj.create_assistant(
        name="KEYPO Copilet2.0",
        description="KEYPO輿情分析專用AI",
        instructions=instruction,
        temperature=0,
        code_interpreter=True
    )
    print(assistant.id)

# def init_reply(assistant_id, data):
#     obj = LLMAssistant()
#     thread = obj.create_thread(
#         messages=[
#             {"role": "assistant", "content": f"Think: 使用者已使用KEYPO搜索了{data["amount"]}筆網路文章，搜索關鍵字為{data["keyword"]}，搜索區間為{period}，我應該詢問使用者需要提供什麼幫助"}
#         ]
#     )
#     run_obj = obj.run_assistant(thread_id=thread.id, assistant_id=assistant_id)
#     chat_history = obj.get_chat_history(run=run_obj, thread_id=thread.id)
#     return thread.id, chat_history[-1]

def chat():
    assistant_id = "asst_A41UZOuopRcl9RpYhu9CSZW1"
    thread_id = "thread_tPoJg5QRLm0CliuCDJxKlQYW"
    obj = LLMAssistant()
    obj.create_message_in_thread(thread_id=thread_id, role="user", content="想要知道哪些新潮美食在國外或一些特定社群之中流行，但還沒被大眾市場看到")
    obj.create_message_in_thread(thread_id=thread_id, role="user", content="請你思考並告訴我我上一句問你的問題是否是跟KEYPO Copilot的職責相關且應該回答的問題")
    run = obj.run_assistant(
        thread_id=thread_id, assistant_id=assistant_id, 
        instructions="以\"Thinking:\"開頭"
    )
    print(run)
    chat_history = obj.get_chat_history(run=run, thread_id=thread_id)
    print(chat_history)


def duty_detection(user_message):
    context="""###CONTEXT###
KEYPO是一個輿情分析軟體，可以透過搜索條件來獲得相應的網路文章，你作為KEYPO Copilot，\
能夠回答關於從KEYPO搜索得到的文章中的任何問題，滿足使用者對相關信息的需求。\n
###ABILITY###
你能夠對網路文章進行多種分析操作、內容問答、資訊摘要、數值統計、文本分析和洞見分析等，\
在必要的情況，透過Code Interpreter你可以進一步有效的分析為使用者分析當前網路文章的更多統計資訊
"""
    simulate_reply = "您好！請問您需要什麼樣的幫助呢？例如，您想要進行內容摘要、特定問題的解答\
、數據統計分析，還是其他方面的洞見分析？請告訴我您的需求！"
    thinking_prompt = "Think: 我需要思考並判斷使用者問我的問題是否是跟KEYPO \
Copilot的職責相關且是否是應該回答的問題\n以json格式回傳\"decide\"值為yes or no，和\"think_step\"我的判斷原因"

    messages = [
        {"role": "system", "content": context},
        {"role": "assistant", "content": simulate_reply},
        {"role": "user", "content": user_message},
        {"role": "system", "content": thinking_prompt}
    ]
    ai_resp = chat_completion(messages=messages, temperature=0)
    return ai_resp

def relat_detection(user_message, data):
    context = """###CONTEXT###
KEYPO是一個輿情分析軟體，可以透過搜索條件來獲得相應的網路文章，你作為KEYPO Copilot，\
能夠回答關於從KEYPO搜索得到的文章中的任何問題，滿足使用者對相關信息的需求。\n
"""
    simulate_reply = f"您好！您已查詢"
    thinking_prompt = "Think: 我需要思考並判斷使用者問我的問題是否是跟KEYPO \
Copilot的職責相關且是否是應該回答的問題\n以json格式回傳\"decide\"值為yes or no，和\"think_step\"我的判斷原因"

    messages = [
        {"role": "system", "content": context},
        {"role": "assistant", "content": simulate_reply},
        {"role": "user", "content": user_message},
        {"role": "system", "content": thinking_prompt}
    ]
    ai_resp = chat_completion(messages=messages, temperature=0)
    return ai_resp


if __name__ == "__main__":
    # 獲取KEYPO資料
    keyword = "(川普&保護費)|(台灣&美國&晶片&(付費|付錢))"
    amount = 1092
    period = "20240630-20240729"
    sample = """類型	文章標題	作者	來源	頻道	摘要	回文數	按讚數/星等	分享數	觀看數	情緒	編修後情緒	時間	網址
主文	川普質疑美國是否應保衛台灣：應付保護費	今日新聞NOWnews	Yahoo 新聞	國際	先前他曾接受《彭博社》採訪，其中提到了台灣議題，川普表示，美國保護台灣多年，但台灣卻偷走了晶片事業，「台灣為我們做了什麼？」 ... 並認為台灣應該要付美國保護費。 ... 川普有此質疑，一部分是基於他認為在跨太平洋去防衛一個島嶼，有實質困難，此外，他希望台灣為美國保護付費。 ... 川普表示，「他們確實100％奪取了我們的晶片事業，我認為，台灣應該付給我們保護費。」 ... 我們多年來保護台灣，他們卻偷走了我們的晶片事業，如今中國迫切想併吞台灣，我不確定美國繼續捍衛台灣有什麼意義。」	4277	0	0		中立		2024-07-17 08:52	https://tw.news.yahoo.com/%E5%B7%9D%E6%99%AE%E8%B3%AA%E7%96%91%E7%BE%8E%E5%9C%8B%E6%98%AF%E5%90%A6%E6%87%89%E4%BF%9D%E8%A1%9B%E5%8F%B0%E7%81%A3-%E6%87%89%E4%BB%98%E4%BF%9D%E8%AD%B7%E8%B2%BB-000724087.html
主文	美國不是台灣保單！川普：台灣搶走晶片市場「超有錢」　要付美國保護費	上報	LINE TODAY	國際	https://today-obs.line-scdn.net/0hA6-N9Wo7HhkQNw7pXkhhTihhEmgjUQQQMgNRKjcxECg9G1tMflVNejNgEjU1AV4YMFMDL2EwFH40Ug1Oew/w644美國前總統川普日前在與拜登的電視辯論前，接受《彭博商業周刊》專訪，內容談及台灣，顯示川普對美國保衛台灣的想法依舊「不以為然」，他直言：「台灣為我們（美國）做了什麼 ... 川普還聲稱台灣搶走晶片市場，並認為台灣應該付美國保護費。 ... 另外在外交政策方面，川普也不諱言可能會改變美國長期以來的外交方針。 ... 針對是否保護台灣免受中國侵略，川普認為台灣距離美國過於遙遠，保護「半個地球以外的島嶼」是有難度的，而且，台灣還「搶走美國所有的晶片生意，（台灣）應該付美國更多保護費」。 ... 川普表示，台灣100％奪取了美國的晶片事業，他認為，台灣應該付給美國保護費。	3309	0	0		中立		2024-07-17 09:05	https://today.line.me/tw/v2/article/zNxpNOD"""
    data = {
        "keyword": keyword,
        "amount": amount,
        "period": period,
        "sample": sample
    }
#     # 呼喚KEYPO Copilot打個招呼
#     (
#         thread_id,
#         init_resp
#     ) = init_reply(
#         assistant_id="asst_A41UZOuopRcl9RpYhu9CSZW1",
#         data=data
#     )
    # chat()
    user_m = """文字當中出現「好吃」的數量是多少"""
    ai_resp = duty_detection(user_message=user_m)
    print(ai_resp)
