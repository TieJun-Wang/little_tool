import requests
import os
from openai import OpenAI

#==============================DeepSeek api=============================
def get_analysis(content):    
    client = OpenAI(
        api_key=os.environ.get('DEEPSEEK_API_KEY'),
        base_url="https://api.deepseek.com")

    print('AI is thinking.............')
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {"role": "system", 
            "content": '''你是一名资深加密货币分析师,
            我将给你我的代币数据你要帮我进行定投策略分析'''},
            {"role": "user", "content": content},
        ],
        stream=False,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )

    print(response.choices[0].message.content)

def get_price(symbol):
    "调用Binance获取实时数据"
    symbol = symbol + "USDT"
    url = 'https://api.binance.com/api/v3/ticker/price?'
    params = {"symbol":symbol}
    response = requests.get(url,params=params,timeout=10)
    price = response.json().get("price")
    return price
