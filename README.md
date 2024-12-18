# TaskControl App

タスク管理システムは、日々のタスクを簡単に記録、管理できるStreamlitベースのWebアプリケーションです。

## 機能

- タスクの追加（日付、タスク名、作業時間）
- タスク一覧の表示
- タスクの完了/未完了の切り替え
- タスクの削除

## インストール方法

1. リポジトリをクローン
```bash
git clone https://github.com/yourusername/taskcontrol.app.git
cd taskcontrol.app
```

2. 必要なパッケージをインストール
```bash
pip install -r requirements.txt
```

## 使用方法

1. アプリケーションを起動
```bash
streamlit run app.py
```

2. ブラウザで自動的に開かれるアプリケーションにアクセス（通常 http://localhost:8501）

## データベース

タスクデータはSQLiteデータベース（tasks.db）に保存されます。データベースは自動的に作成されます。
