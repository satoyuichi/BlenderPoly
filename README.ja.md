[[English](https://github.com/satoyuichi/BlenderPoly/blob/master/README.md) | Japanese]

# Blender Poly
[Google Poly](https://poly.google.com/) にあるモデルを選択してインポートするアドオンです。

## 使い方
### API キーの追加
https://developers.google.com/poly/develop/web の "Get an API Key" から API キーを取得します。

ユーザー設定を開き、Blender Poly アドオンの "Preferences" の "API Key" 欄に先ほどの API キーを入力し、 "Save Settings" ボタンをクリックします。

### 各種情報の読み込み
設定値を適当に選んで "Load" ボタンをクリックすると、必要な情報やサムネイルがダウンロードされます。 **(.obj 形式のデータがあるものだけが対象になります。)**

`Page size:` で指定した数以上に候補がある場合は、続けて "Next" ボタンを押すことで次の候補が読み込まれます。
"Head" ボタンを押すと最初の候補に戻ります。

### モデルのインポート
モデルを選択して "Import" ボタンを押すと、モデルがインポートされます。（マテリアルなどは読み込まれません）

## ダイレクトインポート
[Google Poly](https://poly.google.com/) の ID から直接インポートをします。

ID をコピーします(例: `https://poly.google.com/view/06erPZAKJ5Z` の `06erPZAKJ5Z` が ID)。コピーした ID を "ID:" 欄にペーストします。 "Direct Import" ボタンをクリックします。**(.obj 形式のデータがあるものだけがインポート出来ます。)**

## ライセンス
MIT
