from data_handler import insert_data,show_data,analyze_data
if __name__ == "__main__":
    while True:
        print('================请选择你要进行操作=================')
        print('-----------------1.查看定投数据--------------------')
        print('-----------------2.录入定投数据--------------------')
        print('-----------------3.分析定投数据--------------------')
        print('-----------------4.退出定投程序--------------------')
        print('==================================================')
        while True:
            try:
                option = int(input('请输入对应功能的序号:'))
                if option not in range(1,5):
                    print("输入范围有误,即将重新输入")
                    continue
            except:
                print('请输入整数')
                continue
            break

        if option == 1:
            show_data()
        elif option == 2:
            insert_data()
        elif option == 3:
            analyze_data()
        elif option == 4:
            break
            
    
 