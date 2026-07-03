import os
import json
from api import get_price,get_analysis
#文件处理
#----文件位置
class Color():
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    
#展示数据
def show_data():
    "展示DCA数据"
    #读取文件
    symbol = input('请输入你所要查看的代币名称:').upper()
    data_dir = os.path.join(".","src","DCA_data")
    data_path = os.path.join(data_dir,f"{symbol}.json")
    os.makedirs(data_dir,exist_ok=True)
    if not os.path.exists(data_path):
        print('没有该代币的数据,请先去添加数据')
        return None
    
    with open(data_path,mode='r',encoding='utf-8') as f:
        data = json.load(f)
    
    if not data:
        print('该代币数据为空,请先去添加数据')
        return None
    
    print('查询信息中..........')
    #数据处理
    DCA_time = len(data)
    DCA_amount = 0
    DCA_cost = 0
    current_price = float(get_price(symbol))
    for i in data:
        DCA_amount += i.get('amount')
        DCA_cost += i.get('cost')

    profit = current_price*DCA_amount - DCA_cost
    content = f'''
    查询的代币是:{symbol}
    目前DCA总次数:{DCA_time}
    目前该DCA投入总金额:{DCA_cost}
    目前该DCA总代币数量:{DCA_amount}
    目前该DCA平均成本:{DCA_cost/DCA_amount}
    目前该代币价格为:{current_price}
    '''
    print(content)
    if profit > 0:
        print(f'目前该DCA的收益为:{Color.GREEN}{profit}{Color.RESET}')
    else:
        print(f'目前该DCA的收益为:{Color.RED}{profit}{Color.RESET}')

    input('请输入任意键以继续')
    return content

#录入数据
def insert_data():
    "记录输入的数据"
    symbol = input("请输入您本次DCA的代币名称:").upper()
    cost = float(input('请输入您这次DCA的投入:'))
    amount = float(input('请输入您该次定投的代币数量:'))
    avg_price = cost/amount
    date = input("请输入DCA的日期:")
    data_json = {
        "symbol":symbol,
        "cost":cost,
        "amount":amount,
        "date": date,
        "avg_cost":avg_price
    }
    data_path = os.path.join('.','src','DCA_data',f'{symbol}.json')
    #读取之前的数据
    try:
        with open(data_path,mode='r',encoding='utf-8') as f:
            data = json.load(f)
    except:
        data = []
    #重新写入
    data.append(data_json)
    with open(data_path,mode='w',encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False,indent=2)
    print('数据录入完毕')
    input('请按任意键以返回菜单栏')
    return None

def analyze_data():
    content = show_data()
    get_analysis(content)
    input('请输入任意键以返回菜单')