from core.util import *
from core.client import *
from core.report import *
import report
import time

DATA = get_dic_global('全局变量')
TEMPLES = get_dic_excel('接口模板')
cases = get_dic_excel('测试用例')

def run():
    start_time = time.time()
    for index, case in enumerate(cases):
        if case.get('是否运行') == 1:
            cid = case.get('用例编号')
            temp_name = case.get('模板名称')
            depends = case.get('关联表达式（用例编号=参数路径=临时变量名）')
            param = case.get('参数')
            data = case.get('数据引用')
            check_s1 = case.get('响应内容校验1')
            check_s2 = case.get('响应内容校验2')
            check_s3 = case.get('响应内容校验3')
            check_code = case.get('响应状态码')
            # print('cid={a}'.format(a=cid), temp_name,param, data, len(cases))

            if cid:
                if temp_name:
                    for T in TEMPLES:
                        if T.get('接口名称') == temp_name:
                            url = T.get('地址')
                            method = T.get('方法类型')
                            body_type = T.get('参数类型')
                            headers = T.get('请求头', '')

                            # 判断头信息格式
                            if headers:
                                try:
                                    headers = ast.literal_eval(replace_var(headers))

                                    # headers = json.loads(headers)
                                except:
                                    # infos.append({'id': cid, 'result': 'skip', 'log': ['请求头数据格式错误！']})
                                    log(cid=cid, result='skip', error='请求头格式错误')
                            else:
                                headers = {}
                            # 拼接client对象
                            if url and method and body_type:
                                if body_type == '标准表单':
                                    body_type == 'form'
                                elif body_type == 'JSON':
                                    body_type == 'json'
                                elif body_type == '复合表单':
                                    body_type == 'file'

                            client = Client(url=DATA.get('base_url', '')+url, method=method,
                                            body_type=body_type, cid=cid)
                            client.set_headers(headers)

                            if param:
                                try:
                                    # param = replace_var(param)
                                    param = json.loads(param)
                                    if method == 'post':
                                        client.set_bodies(param)
                                    elif method == 'get':
                                        client.params = param
                                except:
                                    # infos.append({'id':cid, 'result':'skip', 'log':['正文参数格式错误。']})
                                    log(cid=cid, result='skip', error='请求正文格式错误')

                            if method == 'post':
                                client.set_bodies(param)
                            elif method == 'get':
                                client.params = param
                            # 发送请求
                            # print(client.url, client.headers, client.method, client.body_type)
                            client.send()
                            # 建立关联：获取接口响应的字段值加入到全局变量中
                            if depends:
                                var_name = depends.split('=')[1]
                                var_path = depends.split('=')[0]
                                value = client.res_content_json_path(path=var_path)
                                if value is not None:
                                    DATA[var_name] = value
                            # print(DATA)
                            #添加检查点
                            if check_code:
                                client.check_status_code(int(check_code))
                            else:
                                client.check_status_code_200()

                            if check_s1:
                                check_s1 = replace_var(check_s1)
                                check_list = check_s1.split(',')
                                if check_list[0] == '响应时间':
                                    client.check_respond_time(int(check_list[1]))
                                elif check_list[0] == '响应包含':
                                    client.check_respond_content(check_list[1])
                                elif check_list[0] == '节点响应':
                                    client.check_respond_json_content(check_list[1], check_list[2])
                                else:
                                    # infos.append({'id':cid, 'result':'skip', 'log':['检查点不支持。']})
                                    log(cid=cid, result='skip', error='不支持的检查点')
                            if check_s3:
                                check_list = check_s3.split(',')
                                if check_list[0] == '响应时间':
                                    client.check_respond_time(int(check_list[1]))
                                elif check_list[0] == '响应包含':
                                    client.check_respond_content(check_list[1])
                                elif check_list[0] == '节点响应':
                                    if check_list[2].isdigit:
                                        client.check_respond_json_content(check_list[1], int(check_list[2]))
                                    else:
                                        client.check_respond_json_content(check_list[1], check_list[2])
                                else:
                                    log(cid=cid, result='skip', error='不支持的检查点。')
                            # 判断用例执行的最终状态
                            if client.flag > 0:
                                log(cid=cid, result='false')
                            elif client.flag == 0:
                                log(cid=cid, result='success')
                            break
                    else:
                        log(cid=cid, result='skip', error='引用的接口模板不存在。')
                else:
                    log(cid=cid, result='skip', error='测试用例中模板名称为空。')
                    # infos.append({'id':cid, 'result':'skip', 'log': ['测试用例中模板名称为空。']})
            else:
                log(cid='',result='skip', error=f'第{index+1}行测试用例编号为空！')
        else:
            continue

    # 打印测试报告
    creat_report(duration=round(time.time()-start_time, 2), start_time=start_time, infos=infos)
    print(infos)

if __name__ == '__main__':
    run()
