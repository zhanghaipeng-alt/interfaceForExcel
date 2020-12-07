'''
    一些读取Excel中参数的工具
'''

import xlrd
import re
import ast
import json

# 以字典格式在Excel中接口配置和测试用例
def get_dic_excel(name):
    data = []
    work_book = xlrd.open_workbook('/Users/zhanghaipeng/PycharmProjects/InterfaceTestForExcel/suite.xlsx')

    try:
        sheet = work_book.sheet_by_name(sheet_name=name)
        header = sheet.row_values(0)
        for i in range(1, sheet.nrows):
            dic = {}
            for index, value in enumerate(sheet.row_values(i)):
                dic[header[index]] = value
            data.append(dic)
        return data
    except xlrd.biffh.XLRDError:
        print('页面不存在')
        return None

# 在Excel中获取全局变量
def get_dic_global(name):
    data = {}
    try:
        work_book = xlrd.open_workbook('/Users/zhanghaipeng/PycharmProjects/InterfaceTestForExcel/suite.xlsx')
        sheet = work_book.sheet_by_name(name)

        for i in range(1, sheet.nrows):
            data[sheet.row_values(i)[0]] = sheet.row_values(i)[1]
        return data
    except xlrd.biffh.XLRDError:
        raise Exception('文档不存在！')

DATA = get_dic_global('全局变量')
cases = get_dic_excel('测试用例')
TEMPLES = get_dic_excel('接口模板')
def replace_var(source):
    regex_value = r"\$([\w_]+)"
    result = re.findall(regex_value, source)

    if result:
        for r in result:
            if DATA.get(r) is not None:
                source =source.replace('$'+r, DATA.get(r))

    return source



if __name__ == '__main__':
    '''
        字符串转字典：使用json.loads()，但是这个方法中字符必须双引号，单引号不行
        通过 literal_eval，可以；
            ast.literal_eval
    '''
    a = get_dic_excel('接口模板')
    print(a)

