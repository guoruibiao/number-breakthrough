#!coding: utf8
import os
import sys
import time
import subprocess
from random import randint

"""
            数值型英语听力专项训练           
Features：
1 纯数字                        【已完成】
2 数字+单位（秒、公里、千克等）     【未完成】
3 公元纪年                      【未完成】 

Reference：
1 Number-practice:
    https://sunpeteraustralia.com/wp-content/uploads/2020/08/Number-practice.pdf
    
"""


def rand_num(level=1):
    level = int(level)
    if level <= 1:
        level = 1

    minimum = 10 ** (level - 1)
    maximum = 10 ** level

    return randint(minimum, maximum)


# 数字与英文标识的映射桶
bucket = [
    {'min': 0, 'name': 'zero', 'level': 0},
    {'min': 1, 'name': 'one', 'level': 1},
    {'min': 2, 'name': 'two', 'level': 1},
    {'min': 3, 'name': 'three', 'level': 1},
    {'min': 4, 'name': 'four', 'level': 1},
    {'min': 5, 'name': 'five', 'level': 1},
    {'min': 6, 'name': 'six', 'level': 1},
    {'min': 7, 'name': 'seven', 'level': 1},
    {'min': 8, 'name': 'eight', 'level': 1},
    {'min': 9, 'name': 'nine', 'level': 1},
    {'min': 10, 'name': 'ten', 'level': 1},
    {'min': 11, 'name': 'eleven', 'level': 1},
    {'min': 12, 'name': 'twelve', 'level': 1},
    {'min': 13, 'name': 'thirteen', 'level': 1},
    {'min': 14, 'name': 'fourteen', 'level': 1},
    {'min': 15, 'name': 'fifteen', 'level': 1},
    {'min': 16, 'name': 'sixteen', 'level': 1},
    {'min': 17, 'name': 'SEVENTEEN', 'level': 1},
    {'min': 18, 'name': 'eighteen', 'level': 1},
    {'min': 19, 'name': 'nineteen', 'level': 1},
    {'min': 20, 'name': 'twenty', 'level': 1},
    # 该分割线以上可逐一校对，以下则需要根据计算获取完整数据
    {'min': 30, 'name': 'thirty', 'level': 2},
    {'min': 40, 'name': 'forty', 'level': 2},
    {'min': 50, 'name': 'fifty', 'level': 2},
    {'min': 60, 'name': 'sixty', 'level': 2},
    {'min': 70, 'name': 'seventy', 'level': 2},
    {'min': 80, 'name': 'eighty', 'level': 2},
    {'min': 90, 'name': 'ninety', 'level': 2},
    {'min': 100, 'name': 'hundred', 'level': 2},
    {'min': 1000, 'name': 'thousand', 'level': 3},
    {'min': 10000, 'name': '*thousand', 'level': 3},  # 十位数 thousand
    {'min': 100000, 'name': '**thousand', 'level': 3},  # 百位数 thousand
    {'min': 1000000, 'name': 'million', 'level': 4},
    {'min': 10000000, 'name': 'million', 'level': 4},  # 十位数 million
    {'min': 100000000, 'name': 'million', 'level': 4},  # 百位数 million
    {'min': 1000000000, 'name': 'billion', 'level': 5},
    {'min': 10000000000, 'name': 'billion', 'level': 5},  # 十位数 billion
    {'min': 100000000000, 'name': 'billion', 'level': 5},  # 百位数 billion
]

# 单位映射
unit_mapper = {
    '0': '',
    '1': 'thousand',
    '2': 'million',
    '3': 'billion',
}


def get_item(number):
    item = bucket[0]
    for idx, tmp in enumerate(bucket):
        if number < tmp['min']:
            break
        item = tmp
    return item


def _num_to_string(number):
    if number <= bucket[0]['min']:
        return ''

    if number <= 20:
        return get_item(number)['name']
    else:
        item = get_item(number)

        level = ''
        if '**' in item['name']:
            prefix_number = int(number / item['min'])
            level = get_item(prefix_number * 10 ** 2)['name']
        elif '*' in item['name']:
            prefix_number = int(number / item['min'])
            level = get_item(prefix_number * 10 ** 1)['name']
        else:
            prefix_number = int(number / item['min'])
        prefix_item = get_item(prefix_number)
        # print('number={}, level={}, item={}, prefix_number={}, prefix_item={}'.format(number, level, item, prefix_number, prefix_item))
        if number < 100:
            return '{} {} {} '.format(item['name'], level, _num_to_string(number - prefix_number * item['min']))
        else:
            base = '{} {} {} and {} ' if number - prefix_number * item['min'] > 0 else '{} {} {} {} '
            return base.format(prefix_item['name'], level, item['name'],
                               _num_to_string(number - prefix_number * item['min']))


def num_to_string(number):
    num_str = str(number)[::-1]
    step = 3
    chunks = [int(num_str[i:i + step][::-1]) for i in range(0, len(num_str), step)]
    ls = []
    for idx, chunk in enumerate(chunks):
        item = get_item(chunk)
        if item['min'] == 0:
            continue
        prefix_number = int(chunk / item['min'])
        ret = _num_to_string(chunk)

        if idx > 0:
            ret += ' ' + unit_mapper[str(idx)]
        # print('number={}, item={}, prefix_number={}, ret={}'.format(chunk, item, prefix_number, ret))
        ls.insert(0, ret)

    return ls


def say(sentence):
    cmd = "say -v Alex '{}'".format(sentence)
    # os.system(cmd)
    subprocess.Popen(cmd, shell=True).wait()


def useless_but_for_test():
    testcases = [
        123,
        1234,
        12345,
        123456,
        1000000,
        10000000,
        100000001,
        109000000000,
    ]
    for testcase in testcases:
        seed = rand_num(len(str(testcase)))
        ret = num_to_string(seed)
        print('testcase={}, ret={}'.format(seed, ret))

        say(" ".join(ret))
        time.sleep(3)


# 入口
def main():
    level_str = input('请视自身情况，选择训练等级：1-N\n')
    if level_str.lower() == "exit":
        print('bye-bye :-)')
        sys.exit(0)
    level_num = int(level_str)
    if not level_str.isnumeric() or level_num <= 0:
        print("请输入数值 1-N（N 为正整数）")

    # 统计正确率
    testcases = []
    while True:
        seed = rand_num(level_num)
        target = num_to_string(seed)

        print('请根据你听到的表述，输入你的结果：')
        say(target)
        answer = input('')

        # 统计用
        case = {
            'seed': seed,
            'score': 0,
            'target': target,
            'answer': answer,
        }
        if answer.lower() == 'exit':
            # 主动退出不计入错误率
            break

        if not answer.lower().isnumeric():
            testcases.append(case)
            break

        if int(answer) == seed:
            case['score'] = 1
            print('恭喜你答对了，请听下题')
        else:
            print('不好意思，答错啦，正确答案是：')
            print('{} => {}'.format(seed, target))
            print('请再接再厉!')
        # 追加结果
        testcases.append(case)

    # 输出训练结果
    percentage = sum([0 + case['score'] for case in testcases])
    print('total={}, percentage={}%'.format(len(testcases), round((100 * percentage) / len(testcases)), 2))
    print('---------------------')
    for case in testcases:
        print(case)


if __name__ == "__main__":
    main()
