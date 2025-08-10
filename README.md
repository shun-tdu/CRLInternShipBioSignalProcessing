# ⚠️ このリポジトリはインターン課題作成者用です ⚠️

---

# 生体信号解析インターンシップ課題 🔬

このリポジトリは、協調ロボティクス研究室のインターンシップで利用する生体信号解析の課題管理用です。 CSVデータの可視化から、信号処理、インタラクティブなグラフ作成までを実践的に学びます。



---

## 目次
- [使用技術](#-使用技術)
- [環境構築](#-環境構築)
- [実行方法](#-実行方法)
- [課題一覧](#-課題一覧)

---
## 🎉 目標


---

## 🛠️ 使用技術
本プロジェクトでは、以下のライブラリやツールを使用します。
- Python 3.10+
- Pandas
- Matplotlib
- Plotly
- Marimo
- Git / GitHub

---

## 💻 環境構築
このプロジェクトを自分のPCで動かすための手順です。

1.  **リポジトリをクローン**
    ```bash
    git clone [https://github.com/YOUR-ORGANIZATION/intern-bio-signal-analysis.git](https://github.com/YOUR-ORGANIZATION/intern-bio-signal-analysis.git)
    cd intern-bio-signal-analysis
    ```

2.  **Python仮想環境の作成と有効化**
    ```bash
    # Mac / Linux
    python3 -m venv venv
    source venv/bin/activate

    # Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```
    *(ターミナルの行頭に `(venv)` と表示されれば成功です)*

3.  **必要なライブラリのインストール**
    ```bash
    pip install -r requirements.txt
    ```

---

## 🚀 実行方法
各課題のファイルは、プロジェクトのルートディレクトリから以下のコマンドで実行できます。

```bash
# 課題1の実行
python task1.py

# 課題2の実行
python task2.py

# 課題3の実行 (marimo)
marimo run task3.py
```

---

## ✅ 課題一覧
各課題の詳細は、以下のIssueページを確認してください。

- 課題1: CSVデータのグラフ化
- 課題2: 信号処理と特徴量抽出
- 課題3: インタラクティブな可視化

不明点があれば、Slackにて気軽に質問してください。

---

### 課題1
### 目的 生体信号の生値をグラフ化する
### 手順
- CSVを読み取ってデータフレームを返す関数
- データフレームをプロットする関数を作成
- ノートブックから読み出してプロット

### 課題2
### 目的 データフレームに信号処理をしてグラフ化する．
### 手順
-  DFに対して信号処理をする関数を作成
-  LPF, HPF, Notch, 移動平均, RMSエンベロープ, 整流, リサンプリング, FFT
-  信号処理をしたDFをプロット

### 課題3
### 目的 インタラクティブにグラフを表示してみよう
### 手順
- 今まで作った関数をインポートしてmarimoノートブックに統合
- UIベースでフィルターを選べて重ねがけできる
- 好きな窓長さでプロットできる

---

## 🖌️解説事項
### 課題1
- import ~ as ~ 
- 型ヒント
- DocString
- Pandas データフレーム
- try catch except構文
- 相対パスと絶対パス
- CSVファイルとは？

### 課題2
-  scipy
-  周波数領域とFFT
-  サンプリング周波数
-  リサンプリング
-  Low Pass Filter
-  High Pass Filter
-  Notch Filter
-  移動平均
-  RMSエンベロープ
-  全波整流と半波整流

### 課題3
-  marimo
-  plotly

## 🌊🍃Marimo Tips
- MarimoのUI要素は一番外のインデントじゃないと評価されない
