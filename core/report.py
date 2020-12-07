from jinja2 import Template
import time


def creat_report(duration, infos, start_time):
    temp = time.strftime("%Y%m%d_%H%M%S", time.localtime(time.time()))
    with open('./report/template.html', mode='r', encoding='utf-8') as f:
        T = f.read()
    # infos处理
    success = []
    false = []
    skip = []
    for i in infos:
        if i['result'] == 'success':
            success.append(i)
        elif i['result'] == 'false':
            false.append(i)
        elif i['result'] == 'skip':
            skip.append(i)
    print(T)
    template = Template(T)

    with open('./report/' + temp + '.html', mode='w', encoding='utf-8') as f:
        f.write(template.render(html_report_name='票务系统',
                                start_datetime=time.strftime("%Y%m%d_%H:%M:%S",time.localtime(start_time)),
                                duration=duration,
                                file_name=temp + '.html',
                                testsRun=len(infos),
                                successes=len(success),
                                failures=len(false),
                                skipped=len(skip)
                                ))


if __name__ == '__main__':
    creat_report()