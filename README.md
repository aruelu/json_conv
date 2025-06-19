## 1. JSONからCSVへの変換 (json_to_csv.py)

json_to_csv.py は、JSON形式のデータ（オブジェクトの配列）をCSV形式に変換するスクリプトです。
使い方
``` Bash

python3 json_to_csv.py [-h] [-i INPUT] [-o OUTPUT]
```

オプション

    -h, --help: ヘルプメッセージを表示して終了します。
    -i INPUT, --input INPUT: 入力JSONファイルのパスを指定します。指定しない場合、標準入力からJSONデータを読み込みます。
        例: -i input.json
    -o OUTPUT, --output OUTPUT: 出力CSVファイルのパスを指定します。指定しない場合、変換されたCSVデータを標準出力に出力します。
        例: -o output.csv

実行例
JSONファイルからCSVファイルへ変換

input.json:
```  JSON

[
  { "ID": 1, "名前": "田中 太郎", "年齢": 30, "メール": "taro@example.com" },
  { "ID": 2, "名前": "鈴木 花子", "年齢": 25, "メール": "hanako@example.com, inc.", "備考": "新しい社員" },
  { "ID": 3, "名前": "山田 次郎", "年齢": 35, "メール": "jiro@example.com", "備考": "部長" }
]
``` 
コマンド:
``` Bash

python3 json_to_csv.py -i input.json -o output.csv
``` 
生成される output.csv:
``` 

ID,名前,年齢,メール,備考
1,田中 太郎,30,taro@example.com,
2,鈴木 花子,25,"hanako@example.com, inc.",新しい社員
3,山田 次郎,35,jiro@example.com,部長
``` 
標準入力からJSONを読み込み、標準出力へCSVを出力
``` Bash

echo '[{"Product": "Apple", "Price": 1.0}, {"Product": "Banana", "Price": 0.5}]' | python3 json_to_csv.py
``` 
出力:
``` 

Product,Price
Apple,1.0
Banana,0.5
``` 
## 2. CSVからJSONへの変換 (csv_to_json.py)

csv_to_json.py は、CSV形式のデータ（先頭行がキー）をJSON形式（オブジェクトの配列）に変換するスクリプトです。このスクリプトは、数値変換の有無や特定のキーのブーリアン強制変換をオプションで制御できます。
使い方
``` Bash

python3 csv_to_json.py [-h] [-i INPUT] [-o OUTPUT] [-b BOOLEAN_KEYS] [-n]
``` 
オプション

    -h, --help: ヘルプメッセージを表示して終了します。
    -i INPUT, --input INPUT: 入力CSVファイルのパスを指定します。指定しない場合、標準入力からCSVデータを読み込みます。
        例: -i input.csv
    -o OUTPUT, --output OUTPUT: 出力JSONファイルのパスを指定します。指定しない場合、変換されたJSONデータを標準出力に出力します。
        例: -o output.json
    -b BOOLEAN_KEYS, --boolean-keys BOOLEAN_KEYS: 値をブーリアン型 (true/false) に強制変換するキー名をカンマ区切りで指定します。
        指定されたキーの値は '1', 'true', 'TRUE' (大文字小文字無視) であれば true に、それ以外は false に変換されます。
        例: -b is_active,enabled_flag
    -n, --enable-number-conversion: このオプションを指定すると、数値に見える値が自動的に数値型（整数/浮動小数点数）に変換されます。
        デフォルトでは数値変換は行われず、文字列として保持されます（-b 指定は優先されます）。

実行例
CSVファイルからJSONファイルへ変換（デフォルト：数値は文字列）

input.csv:
``` 

ID,Name,IsActive,AdminStatus,Score
1,Alice,TRUE,1,100
2,Bob,false,0,75.5
3,Charlie,1,0,90
``` 
コマンド:
``` Bash

python3 csv_to_json.py -i input.csv -o output.json -b IsActive,AdminStatus
``` 
生成される output.json:
JSON

[
  {
    "ID": "1",
    "Name": "Alice",
    "IsActive": true,
    "AdminStatus": true,
    "Score": "100"
  },
  {
    "ID": "2",
    "Name": "Bob",
    "IsActive": false,
    "AdminStatus": false,
    "Score": "75.5"
  },
  {
    "ID": "3",
    "Name": "Charlie",
    "IsActive": true,
    "AdminStatus": false,
    "Score": "90"
  }
]

数値変換を有効にしてCSVファイルからJSONファイルへ変換

input.csv: (上記と同じ内容)

コマンド:
``` Bash

python3 csv_to_json.py -i input.csv -o output.json -b IsActive,AdminStatus -n
``` 
生成される output.json:
JSON

[
  {
    "ID": 1,
    "Name": "Alice",
    "IsActive": true,
    "AdminStatus": true,
    "Score": 100
  },
  {
    "ID": 2,
    "Name": "Bob",
    "IsActive": false,
    "AdminStatus": false,
    "Score": 75.5
  },
  {
    "ID": 3,
    "Name": "Charlie",
    "IsActive": true,
    "AdminStatus": false,
    "Score": 90
  }
]

標準入力からCSVを読み込み、標準出力へJSONを出力
``` Bash

echo 'Status,Value\nTRUE,123\nfalse,45.6' | python3 csv_to_json.py -b Status -n
``` 
出力:
JSON

[
  {
    "Status": true,
    "Value": 123
  },
  {
    "Status": false,
    "Value": 45.6
  }
]


