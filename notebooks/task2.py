import marimo

__generated_with = "0.14.16"
app = marimo.App(width="medium")


@app.cell
def _():
    # ライブラリのインポート(課題1,2で作成した関数)
    import marimo as mo
    import pandas as pd
    import numpy as np

    from modules.signal_processing import apply_lowpass_filter, apply_highpass_filter, apply_notch_filter, apply_moving_average, apply_rms_envelope, apply_rectification, apply_resampling, apply_fft
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        """
        # 課題2 実装確認ノートブック 🔬
    
        このノートブックは、あなたが実装した各種信号処理関数が正しく動作するかをインタラクティブに確認します。
        ドロップダウンで試したいフィルタを選び、スライダーでパラメータを調整してみてください。
        元の波形（青）と処理後の波形（赤）が同時にプロットされます。
        """
        )
    return


@app.cell
def _(mo):
    # 確認したいフィルタを選択するUI
    filter_selector = mo.ui.dropdown(
        options=[
            "ローパスフィルタ",
            "ハイパスフィルタ",
            "ノッチフィルタ",
            "移動平均",
            "全波整流",
            "RMSエンベロープ",
        ],
        value="ローパスフィルタ",
        label="テストするフィルタを選択"
    )

    # 各フィルタのパラメータを調整するUI
    param_slider = mo.ui.slider(1, 100, value=10, label="パラメータ調整")
    return


if __name__ == "__main__":
    app.run()
