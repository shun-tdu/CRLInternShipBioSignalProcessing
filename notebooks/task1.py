import marimo

__generated_with = "0.14.16"
app = marimo.App(width="medium")


@app.cell
def _():
    # ライブラリのインポート(課題1で作成した関数)
    import marimo as mo
    from modules.data_loader import load_data
    from modules.plotting import plot_data
    return load_data, mo, plot_data


@app.cell
def _(mo):
    mo.md(
        """
    # 課題1 実装確認ノートブック 📝
    このノートブックは、あなたが作成した`load_data`関数と`plot_data`関数が正しく動作するかを確認するためのものです。

    **使い方:**

    1. あなたが課題1で作成したPythonファイル（`load_data`と`plot_data`関数が含まれる）を、このノートブックと同じフォルダに置いてください。

    2. 上のセルにある`from task1_functions import ...`の部分を、あなたのファイル名に合わせて修正してください。

    3. `marimo run check_task1.py` を実行すると、下に結果が表示されます。
    """
    )
    return


@app.cell
def _(load_data, mo):
    # --- 確認用のデータファイルパス ---
    # ここで指定したCSVファイルを読み込みます
    csv_filepath = 'data/15Subjects-7Gestures/S0/emg-fistdwn-S0.csv'

    # 課題1で実装したload_data関数を呼び出します
    df = load_data(csv_filepath)

    mo.md(f"**1. `load_data`関数のテスト**\n\n`{csv_filepath}` を読み込みます...")
    return (df,)


@app.cell
def _(df, mo):
    # 読み込んだデータフレームの中身を確認します
    if not df.empty:
        result = mo.vstack([
        mo.md("✅ データ読み込み成功！"),
        mo.md(f"データ数: {len(df)}行, {len(df.columns)}列"),
        mo.md("--- 先頭5行のプレビュー ---"),
        mo.ui.table(df.head())    
        ])
    else:
        result = mo.md("❌ データの読み込みに失敗しました。`load_data`関数の実装を確認してください。")

    result
    return


@app.cell
def _(df, mo, plot_data):
    mo.md("**2. `plot_data`関数のテスト**\n\n読み込んだデータをグラフ化します...")
    # 課題1で実装したplot_data関数を呼び出します
    mo.ui.plotly(plot_data(df, title="生データプロットの確認"))

    return


if __name__ == "__main__":
    app.run()
