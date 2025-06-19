#!/usr/bin/env python3
# json_to_csv.py
import csv
import json
import sys
import argparse

def json_to_csv(json_data, output_file=sys.stdout):
    """
    JSONデータの配列をCSV形式に変換します。
    キーがCSVのヘッダーになります。

    Args:
        json_data (list): 変換するJSONデータのリスト。各辞書は同じキー構造を持つと仮定します。
        output_file (file object, optional): CSVの出力先ファイルオブジェクト。
                                            デフォルトは標準出力。
    """
    if not json_data:
        return

    all_keys = set()
    for item in json_data:
        all_keys.update(item.keys())

    headers = list(json_data[0].keys()) if json_data else []
    for key in sorted(list(all_keys - set(headers))):
        headers.append(key)

    writer = csv.DictWriter(output_file, fieldnames=headers)

    writer.writeheader()
    for row in json_data:
        writer.writerow(row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="JSONデータをCSVに変換するスクリプトです。",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '-i', '--input', type=str, default=None,
        help='入力JSONファイルのパス。指定しない場合は標準入力から読み込みます。\n例: -i input.json'
    )
    parser.add_argument(
        '-o', '--output', type=str, default=None,
        help='出力CSVファイルのパス。指定しない場合は標準出力に出力します。\n例: -o output.csv'
    )

    args = parser.parse_args()

    json_input = None
    if args.input:
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                json_input = json.load(f)
        except FileNotFoundError:
            print(f"エラー: ファイルが見つかりません: {args.input}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"エラー: 無効なJSON形式です: {args.input}", file=sys.stderr)
            sys.exit(1)
    else:
        try:
            json_input = json.load(sys.stdin)
        except json.JSONDecodeError:
            print("エラー: 標準入力が無効なJSON形式です。", file=sys.stderr)
            sys.exit(1)

    if args.output:
        try:
            with open(args.output, 'w', newline='', encoding='utf-8') as f:
                json_to_csv(json_input, f)
            print(f"CSVデータが '{args.output}' に正常に保存されました。", file=sys.stderr)
        except IOError as e:
            print(f"エラー: ファイルの書き込みに失敗しました: {args.output} - {e}", file=sys.stderr)
            sys.exit(1)
    else:
        json_to_csv(json_input, sys.stdout)