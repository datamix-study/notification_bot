# notification_bot

スクレイピングによりサイト更新の有無を検知し、更新内容をslackに通知するボット。  
大まかな処理の流れは下記となる。  
1. 起動引数の処理
1. スクレイピングの設定を読み込む
    - 設定はjsonファイルもしくはgoogle sheetsで管理している
    - 設定は対象のURLや過去のスクレイピング結果などを持つ
1. 設定で提示された対象のURLにアクセスし、レスポンスを取得する
1. レスポンスを処理し、過去のスクレイピング結果と比較しサイト更新の有無をチェックする
1. サイト更新があり、通知フラグがONの場合はスクレイピング設定の更新/slackへの通知を行う
    - 通知フラグは起動引数で渡される
1. 設定の数(= スクレイピングを行いたいページの数)だけ3~5を繰り返す

## 動作確認バージョン
- python==3.6.7
- beautifulsoup4==4.8.0
- gspread==3.1.0
- oauth2client==4.1.3

## 起動方法
起動コマンドは当`README.md`ファイルが存在するディレクトリに移動後を前提とする。

### スクリプト実行
```bash
python -m main [env] [run_mode]
```
`env`, `run_mode`引数の詳細に関しては後述する。  
とりあえず`python -m main`もしくはpycharmで実行すればデータの更新やslack通知は行わない、また仮にそれらが行われたとしても大した問題もないので気楽にやろう。  
具体例としては下記のようなコマンドを想定している。
```bash
# ローカルでサイトの更新チェックのみを行い、サイト更新があってもslack通知しないコマンド例
python -m main
```
```bash
# 本番環境で動作し、サイト更新時にslack通知を行うコマンド例
python -m main prod run
```

#### `env`引数に関して
動作環境を指定する。`error`, `p`, `prod`, `d`, `dev` とそれら以外の場合で下記のような設定が使われる。

| | `error` | `p` or `prod` | `d` or `dev` | (other or empty) |
| --- | --- | --- | --- | --- |
| 出力するログレベル | - |INFO | INFO | DEBUG |
| 読み込むコンフィグファイル名 | - | config_prod.ini | config.ini | config.ini |
| スクレイピングの設定の管理方法 | - | google sheets | google sheets | json file |
| 備考 | 起動後に即エラーを発生させる = エラー時の動作確認目的 | 本番環境想定 | 動作確認環境想定 | ローカル環境想定 |

#### `run_mode`引数に関して
通知フラグに該当。`run`を渡すとサイト更新があった場合は過去のスクレイピング結果データの更新やslackへの通知を行う。それ以外の場合はサイト更新の有無のチェックのみ行う。

### ユニットテスト実行
```bash
python -m unittest -v
```

## 環境構築
1. プロジェクトの準備(必須)
2. slack連携の準備(任意)
3. google sheets連携の準備(任意)

### 1. プロジェクトの準備
1. ワークスペースに当プロジェクトを`clone`する
    ```bash
    cd <work_directory>
    git clone git@github.com:datamix-study/notification_bot.git
    cd notification_bot
    ```
1. `src/resources`の`config_sample.ini`をコピーし、`config.ini`と`config_prod.ini`(こちらは本番環境で動かさない場合は作らなくても良い)を作成する
    - `cp src/resources/config_sample.ini src/resources/config.ini`, `cp src/resources/config_sample.ini src/resources/config_prod.ini`
    <pre>
    notification_bot/
    ├ README.md
    ├ src/
      ├ resources/
        ├ config.ini
        ├ config_prod.ini
        ├ config_sample.ini
    </pre>
1. (必要ならば) `venv`などを使って仮想環境を用意する
1. 必要なライブラリをインストールする
    ```bash
    pip install -r requirements.txt
    ```
1. `python -m main`でエラーなく動作することを確認

### 2. slack連携の準備
slack通知を実際に行いたい場合は設定がいる。行わない場合はスキップしても良い。

TODO: incoming_webhookを想定、手順を書くかリンクを貼るなどする

### 3. google sheets連携の準備
スクレイピングの設定をgoogle sheetsを使って管理したい場合は設定がいる。本番環境、動作確認環境で動かさない場合はスキップしても良い。

#### プロジェクトの作成
1. https://cloud.google.com/
1. ログイン、コンソールへ移動
1. プロジェクトの選択 > 新しいプロジェクト
1. 情報を入力して作成

#### google sheets認証キーを取得
1. APIとサービス > ライブラリ
1. Google Drive APIを探して有効にする
1. APIとサービス > ライブラリ
1. Google Sheets APIを探して有効にする
1. APIとサービス > 認証情報
1. 認証情報を作成 > サービスアカウントキー
1. 新しいサービスアカウント > (入力) > キーのタイプをJSONにする > 作成
    - サービスアカウント名はgoogle-sheetsなど適当に入寮
    - 役割はproject > 編集者
    - **ダウンロードしたXXX.jsonは外部に公開しないこと**
1. ダウンロードされたXXX.jsonを`src/resources`に移動
    <pre>
    notification_bot/
    ├ README.md
    ├ src/
      ├ resources/
        ├ config_sample.ini
        ├ XXX.json
    </pre>

#### google sheetsの作成
1. スプレッドシートを作成し下記を入力する
    - ファイル名やシート名は任意(シート名は手順書ではdevシートとする)
    - A1セルに`parser_name`が入力される

    | | **A** | **B** | **C** | **D** | **E** |
    | --- | --- | --- | --- | --- | --- |
    | **1** | parser_name | access_url | last_article_urls | do_notify_empty | message_template |
    | **2** | DataMixInformationParser | https://datamix.co.jp/news/ |  | 1 | データミックスのお知らせが更新されました [{0[title]}] {0[url]} |
    | **3** | DataMixMediaParser | https://datamix.co.jp/news/ |  | 1 | データミックスのメディア掲載が更新されました [{0[title]}] {0[url]} |
    | **4** | DataMixBlogParser | https://datamix.co.jp/blog/ |  | 1 | データミックスのブログが更新されました [{0[title]}] {0[url]} |
    | **5** | MeetupApiParser | https://api.meetup.com/datamix/events?&sign=true&photo-host=public&page=20 |  | 0 | meetupにイベントが追加されました [{0[title]}] {0[url]} |
1. 作成したシートをコピーして同ファイル内に計2つのシートを持つようにする
    - シート名は手順書ではprodシートとする → dev, prodシートがある
1. シート右上の共有
1. XXX.jsonの`client_email`行のコロン以下のダブルクォーテーション内を入力し、編集者権限で完了
    - `hoge@foo.iam.gserviceaccount.com` のような文字列

#### configの編集
1. `config.ini`および`config_prod.ini`を編集する
    - key_json_file_name = <ダウンロードしたXXX.jsonのファイル名>
    - spreadsheet_key = <spreadsheetのID>
        - https://docs.google.com/spreadsheets/d/<ここの部分>/edit#gid=0
    - sheet_name = <スプレッドシートのシート名>
        - 手順書の例ならdev(config.iniの場合) or prod(config_prod.iniの場合)

## デプロイ

TODO: 手順を書くかリンクを貼るなどする
