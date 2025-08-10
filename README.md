<div align="center">

[![Hugging Face Spaces](https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-yellow)](https://huggingface.co/spaces/YOUR_HF_USERNAME/YOUR_SPACE_ID)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

<!-- プロジェクトタイトル -->
<h1 align="center">
  生体信号インタラクティブ解析ツール
</h1>

<!-- 概要 -->
<p align="center">
  WebブラウザでEMG信号をインタラクティブに解析・可視化できるデモアプリケーションです。<br>
  MarimoとPlotlyで構築されています。
</p>

<!-- Hugging Face Spacesへの誘導 -->
<div align="center">
  <a href="https://shuty-crlinternshipbiosignalprocessing.hf.space">
    <img src="https://huggingface.co/datasets/huggingface/badges/raw/main/open-in-hf-spaces-xl-dark.svg" alt="Open in Hugging Face Spaces">
  </a>
</div>
<br>
<p align="center">
  <img src="images/interactive%20plot_demo.gif" alt="Demo GIF" width="85%">
</p>

---

## 📖 概要

このプロジェクトは、研究室のインターンシップ課題として開発されました。CSV形式のEMG（筋電図）データを読み込み、様々な信号処理フィルタをインタラクティブに適用しながら、時間領域と周波数領域でリアルタイムに結果を可視化することを目的としています。

モジュール単位で実装していき、最終的に本ページのデモアプリケーションを組み上げていく課題です。

実際にプログラムを組みながら信号処理アプリケーションを作成しましょう！

---

## ✨ 主な機能

* **インタラクティブな操作**: スライダーやドロップダウンで、フィルタのパラメータや表示範囲を直感的に変更可能
* **多彩な信号処理**: ローパス、ハイパス、ノッチフィルタ、移動平均、整流、RMSエンベロープなど
* **リアルタイム可視化**: 時間領域の波形と、FFTによる周波数スペクトルを同時に表示
* **インストール不要**: Hugging Face Spaces上で、誰でもすぐにデモを試すことができます

---

## 🛠️ 使用技術


<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas">
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly">
  <img src="https://img.shields.io/badge/marimo-333333?style=for-the-badge&logo=marimo&logoColor=white" alt="Marimo">
  <img src="https://img.shields.io/badge/Hugging%20Face-FFD21E?style=for-the-badge&logo=hugging-face&logoColor=black" alt="Hugging Face">
</p>


---


## 🚀 課題の始め方

このリポジトリは，インタラクティブな生体信号処理アプリケーションを作成するため課題です、最終的にはデモのようなアプリケーションを自分で構築することを目指します。

### 1. **環境構築**
まずは、自分のPCで開発を始めるための準備をします。

### 前提条件
* [Python 3.10](https://www.python.org/) 以上
* [Git](https://git-scm.com/)

### セットアップと実行

1.  **リポジトリをクローン**
    ```bash
    git clone [https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO.git](https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO.git)
    cd YOUR_REPO
    ```

2.  **仮想環境の作成と有効化**
    ```bash
    python -m venv .venv
    source .\.venv\Scripts\activate
    ```
    *(ターミナルの行頭に`(venv)`と表示されれば成功です)*

3.  **依存ライブラリのインストール**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Marimoノートブックの実行**
    ```bash
    marimo run your_notebook_name.py
    ```
    *(`your_notebook_name.py` はあなたのファイル名に置き換えてください)*

---

## 📄 ライセンス

このプロジェクトは [MIT License](LICENSE) の下に公開されています。

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

