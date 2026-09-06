# Dify Barcode Reader Plugin

Dify標準UIで画像をアップロードし、その画像に含まれるバーコードを読み取るためのTool Pluginです。

想定Workflow:

```text
User Input
  └─ 画像
      ↓
自作 Barcode Reader Plugin
      ↓
barcode
      ↓
Database Plugin
      ↓
SQL Server
```

## 主な出力

- `found`: 読み取り成功/失敗
- `barcode`: 最初に検出したバーコード値
- `format`: EAN13 / Code128 / QRCode など
- `count`: 検出数
- `all_barcodes`: 検出した値の一覧

## Difyでの使い方

1. Workflowアプリを作成
2. User Inputで画像ファイルを1枚受け取る
3. Toolノードに `Read Barcode` を追加
4. `image` にUser Inputの画像変数を接続
5. 後続のIF/ELSEで `found == true` を確認
6. Database Pluginに `barcode` を渡してSQL Serverを検索
7. 取得した注意事項・履歴をEndノード等で表示

## パッケージ

Dify Plugin CLIを使用します。

```bash
dify plugin package . -o barcode_reader-0.0.1.difypkg
```
