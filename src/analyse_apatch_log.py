# coding:utf-8

import apache_log_parser
import argparse
import os
from datetime import datetime
from collections import defaultdict

# デフォルトのログフォーマット
LOG_FORMAT='%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"'

# アクセスログの解析結果を保存するresult:dictの初期化
def init_result():
    result = {'remote_hosts':defaultdict(int), 'hour':{}}
    for i in range(24):
        result['hour'][i] = 0

    return result

# アクセスログの解析結果の更新
def update_result(parsedData, result):
    remote_host = parsedData['remote_host']
    hour = parsedData['time_received_datetimeobj'].hour

    result['remote_hosts'][remote_host] += 1
    result['hour'][hour] += 1

# アクセスログの解析
def ana_log(files:list, log_format=LOG_FORMAT, term=None) -> dict:
    # ファイルパスを絶対パスへ変換
    files = [os.path.abspath(_file) for _file in args.files]
    # アクセスログファイルが存在するか確認
    for _file in files:
        if not os.path.isfile(_file):
            raise FileExistsError('file is not found\n{0}'.format(_file))

    # 期間を指定しているならdatetime型へ変換
    if args.term:
        term = [datetime.strptime(args.term[i], '%Y/%m/%d') for i in range(2)]

    # apache_logのparserを作成
    parser = apache_log_parser.make_parser(log_format)

    # エラーが見つかったどうかのフラグ
    find_error = False
    # 初期化
    result = init_result()
    # ファイルを読み込み、1行毎（逐次的）にログを解析する
    for _file in files:
        with open(_file, 'r') as f:
            counter = 0
            for line in f:
                counter += 1
                try:
                    parsed = parser(line)
                except:
                    # 読み込めない行に対するエラー処理：読み込めない行と、その行があるファイルをコマンドラインで表示。次の行へ移行
                    if find_error == False:
                        find_error = True
                        print('ValueError')
                    print('file: {0}'.format(_file))
                    print('line {0}: {1}'.format(counter, line))
                    continue

                # 期間が設定されていれば期間内のデータかどうか判定
                if term is not None:
                    if term[0] >= parsed['time_received_datetimeobj'] or term[1] <= parsed['time_received_datetimeobj']:
                        continue

                # 結果の更新
                update_result(parsed, result)

    return result

# 解析結果をコマンドラインで表示
def print_result(result, term=None):
    if term is not None:
        print('{0} ~ {1}'.format(term[0], term[1]))

    print('時間帯 : アクセス数')
    print('――――――――――――――――――')
    for hour, num in result['hour'].items():
        print('{0}:00 ~ {0}:59 : {1}'.format(hour, num))

    print()
    print('リモートホスト : アクセス数')
    print('―――――――――――――――――――――――――――')
    sorted_access = sorted(result['remote_hosts'].items(), key=lambda x:x[1], reverse=True)
    for access in sorted_access:
        print('{0} : {1}'.format(access[0], access[1]))

def main(args):
    result = ana_log(args.files, log_format=args.logformat, term=args.term)
    print_result(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--files', nargs='*', default='/var/log/httpd/access_log')
    parser.add_argument('-t', '--term', nargs=2, help='format:%Y/%m/%d %Y/%m/%d')
    parser.add_argument('--logformat', default=LOG_FORMAT)

    args = parser.parse_args()

    main(args)