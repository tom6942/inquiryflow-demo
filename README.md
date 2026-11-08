# InquiryFlow — 海外営業の問い合わせ対応デモ

日本酒を扱う貿易会社の海外営業を想定した、面接・ポートフォリオ用の合成データによるデモです。

## 体験する
1. 01A（見積依頼）または04A（破損対応）を選び、「保存済みのAPI結果を開く」を押します。
2. 返信案・社内向けメモを確認し、確認者名を入力して承認します。
3. 自動で案件画面に進み、模擬CRMとフォローを確認できます。フォロー完了後に案件を完了できます。
4. 06Aは2組の商品・配送先を含み、現在の構造では扱えないため自動登録を止める例です。

保存済みAPI出力には出所と版情報があり、人が編集した展示稿とは分けて保存しています。保存済み結果の表示で新たなAPI利用は発生しません。

## 実装と限界
Streamlit / Python / Pydantic / OpenAI API。語句・IDF・日本語文字列によるKB検索、出典付き返信案、プログラムによる登録制限、版を指定した担当者承認、重複を防ぐ模擬CRM・タスク登録を実装しています。ベクトルDBや自動学習は使用していません。

実在庫、価格表、注文・配送システムには未接続です。メール送信、外部CRM登録は行いません。複数商品・配送先の完全な構造化登録は未実装です。データはブラウザー接続ごとの一時保存で、再接続・サーバー再起動により消える場合があります。恒久的な業務利用や実在する顧客データの入力には対応していません。

APIキーは任意で、サーバー共用キーは使用しません。入力する場合は問い合わせをOpenAIへ送信し、分析・返信案作成の最大2回を実行します。保存・ダウンロードにはキーを含めません。

## 起動・公開
Python 3.12を使用します。
```
pip install -r requirements.txt
streamlit run public_app.py
```
Streamlit Community Cloudでこのリポジトリと `public_app.py` を指定します。サーバーのSecrets設定は不要です。`.env`、金鑰、個人の履歴ファイルは追加しないでください。

## 検証の読み方
「検証と改善」に3例の問題・修正・残る制約を記載しています。既知の合成例であり、企業導入実績・未見テスト成績・効果の保証ではありません。人の自己申告時間とAPI生成時間は条件が異なるため、削減率として比較していません。

## Source layout
The deploy entrypoint verifies the SHA-256 of `inquiryflow_source.zip`, extracts its readable source into a versioned temporary code directory, and runs its `public_app.py`. This avoids browser upload flattening nested folders. The ZIP contains the `inquiryflow/`, `prompts/`, `data/` directories and a per-file release manifest. Visitor records and API keys are not in this archive. Code is shared read-only; each visitor uses a separate temporary data directory. Download or unpack the ZIP to inspect the full Python source.
