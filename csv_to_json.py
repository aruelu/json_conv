#!/usr/bin/env python3
# csv_to_json.py
import csv
import json
import sys
import argparse

def csv_to_json(csv_data, output_file=sys.stdout, boolean_keys=None, enable_number_conversion=False):
    """
    CSVデータをJSONデータのリストに変換します。
    先頭行をキー（ヘッダー）として扱います。

    Args:
        csv_data (file object): 変換するCSVのファイルオブジェクト。
        output_file (file object, optional): JSONの出力先ファイルオブジェクト。
                                            デフォルトは標準出力。
        boolean_keys (list, optional): 値をブーリアンに強制変換するキー名のリスト。
                                       これらのキーについては、'1', 'true', 'TRUE' (大文字小文字無視)
                                       が True に、それ以外は False になります。
                                       例: ['is_active', 'enabled_flag']
        enable_number_conversion (bool, optional): Trueの場合、数値に見える値を数値型に変換します。
                                                    デフォルトはFalse（数値変換を行わない）。
    """
    reader = csv.DictReader(csv_data)
    json_output = []

    if boolean_keys is None:
        boolean_keys = []

    true_values = {'1', 'true'}

    for row in reader:
        processed_row = {}
        for key, value in row.items():
            if key in boolean_keys:
                normalized_value = value.strip().lower() if value is not None else ''
                processed_row[key] = normalized_value in true_values
            else:
                if value is None or value == '':
                    processed_row[key] = None
                elif value.lower() == 'true':
                    processed_row[key] = True
                elif value.lower() == 'false':
                    processed_row[key] = False
                elif enable_number_conversion:
                    try:
                        if '.' in value and value.count('.') == 1:
                            if value.replace('.', '', 1).isdigit() and value.strip() != '.' and value.strip() != '-.' :
                                processed_row[key] = float(value)
                            else:
                                processed_row[key] = value
                        elif value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
                            processed_row[key] = int(value)
                        else:
                            processed_row[key] = value
                    except ValueError:
                        processed_row[key] = value
                else:
                    processed_row[key] = value
        json_output.append(processed_row)

    json.dump(json_output, output_file, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CSVデータをJSONに変換するスクリプトです。\n\n"
                    "デフォルトでは、数値は文字列として保持されます。数値変換を有効にするには -n/--enable-number-conversion を指定してください。\n"
                    "特定のキーの値をブーリアンに強制変換することもできます。",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '-i', '--input', type=str, default=None,
        help='入力CSVファイルのパス。指定しない場合は標準入力から読み込みます。\n例: -i input.csv'
    )
    parser.add_argument(
        '-o', '--output', type=str, default=None,
        help='出力JSONファイルのパス。指定しない場合は標準出力に出力します。\n例: -o output.json'
    )
    parser.add_argument(
        '-b', '--boolean-keys', type=str, default='',
        help='値をブーリアン型(true/false)に強制変換するキー名をカンマ区切りで指定します。\n'
             '指定されたキーの値は \'1\', \'true\', \'TRUE\' (大文字小文字無視) であれば true に、\n'
             'それ以外は false に変換されます。\n例: -b is_active,enabled_flag'
    )
    parser.add_argument(
        '-n', '--enable-number-conversion', action='store_true',
        help='このオプションを指定すると、数値に見える値が自動的に数値型(整数/浮動小数点数)に変換されます。\n'
             'デフォルトでは数値変換は行われず、文字列として保持されます（-b指定は優先されます）。'
    )

    args = parser.parse_args()

    boolean_keys_list = [k.strip() for k in args.boolean_keys.split(',') if k.strip()]

    input_file_obj = None
    output_file_obj = None

    try:
        if args.input:
            input_file_obj = open(args.input, 'r', newline='', encoding='utf-8')
        else:
            input_file_obj = sys.stdin

        if args.output:
            output_file_obj = open(args.output, 'w', encoding='utf-8')
        else:
            output_file_obj = sys.stdout

        csv_to_json(
            input_file_obj,
            output_file_obj,
            boolean_keys=boolean_keys_list,
            enable_number_conversion=args.enable_number_conversion
        )

        if args.output:
            print(f"JSONデータが '{args.output}' に正常に保存されました。", file=sys.stderr)

    except FileNotFoundError:
        print(f"エラー: ファイルが見つかりません: {args.input}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"エラー: 処理中にエラーが発生しました: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if args.input and input_file_obj:
            input_file_obj.close()
        if args.output and output_file_obj:
            output_file_obj.close()