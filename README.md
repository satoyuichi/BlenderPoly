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

## ライセンス
MIT

# Blender Poly
This add-on is a direct import from [Google Poly](https://poly.google.com/) .

## Usage
### Add API Key
Get API key from https://developers.google.com/poly/develop/web.

Open the "User Preferences" and select "Blender Poly" add-on. Input the API key to "Preferences" and Click "Save Settings" button.

### Load some information
Input some setting values and click "Load" button. Downloading important data and thumbnails. **(only included .obj format data)**

If model count more than input `Page size:`, click "Load" button again to loading next model list.
Click "Head" button go to head the lists.

### Import model
Chose model and click "Import" button.(Not load material etc)

## License
MIT
