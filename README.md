# Blender Poly
[Google Poly](https://poly.google.com/) にあるモデルを選択してインポートするアドオンです。

## 使い方
### API キーの追加
https://developers.google.com/poly/develop/web の "Get an API Key" から API キーを取得します。

Blender Poly アドオンの "Preferences" の "API Key" 欄に先ほどの API キーを入力し、 "Save Settings" ボタンをクリックします。

### 各種情報の読み込み
設定値を適当に選んで "Load" ボタンをクリックすると、必要な情報やサムネイルがダウンロードされます。 **(.obj 形式のデータがあるものだけが対象になります。)**

`Page size:` で指定した数以上に候補がある場合は、続けて "Load" ボタンを押すことで次の候補が読み込まれます。

### モデルのインポート
モデルを選択して "Import" ボタンを押すと、モデルがインポートされます。（マテリアルなどは読み込まれません）

## ライセンス
MIT

# Blender Poly
This is direct import from [Google Poly](https://poly.google.com/) .

## Usage
### Add API Key
Get API key from https://developers.google.com/poly/develop/web

Blender Poly Add-on's "Preferences" "API Key" input API key that get API key.  Click "Save Settings" button.

### Load some information
Input some values and click "Load" button. Downloading important data and thumbnails. **(only include .obj format data)**

### Import model
select model and click "Import" button for important model.(Not loading material)

## License
MIT
