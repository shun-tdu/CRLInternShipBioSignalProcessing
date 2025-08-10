import marimo

__generated_with = "0.14.16"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np

    from modules.data_loader import load_data
    from modules.plotting import plot_data
    from modules.signal_processing import apply_lowpass_filter, apply_moving_average, apply_resampling
    return apply_resampling, load_data, mo, np, plot_data


@app.cell
def _(load_data, mo, np):
    FILE_PATH = "data/15Subjects-7Gestures/S0/emg-fistdwn-S0.csv"
    SAMPLING_RATE = 200

    raw_data = load_data(FILE_PATH)

    if not raw_data.empty:
        # 200Hzの時間軸を作成（0秒スタート）
        time_interval = 1.0 / SAMPLING_RATE  # 0.005秒間隔
        raw_data.index = np.arange(len(raw_data)) * time_interval
        total_duration = raw_data.index[-1]

        info_message = f"""
        📊 **データ読み込み完了**
        - サンプル数: {len(raw_data)}
        - 総時間: {total_duration:.2f} 秒
        - サンプリング周波数: {SAMPLING_RATE} Hz
        - 時間間隔: {time_interval:.3f} 秒
        """
    else:
        total_duration = 0.0
        info_message = "❌ データの読み込みに失敗しました"

    mo.md(info_message)

    return raw_data, total_duration


@app.cell
def _(mo, total_duration):
    # UIコンポーネントの定義
    window_slider = mo.ui.slider(1, 101, step=2, value=21, label="移動平均の窓長")
    cutoff_input = mo.ui.number(1.0, 50.0, step=0.5, value=5.0, label="ローパスフィルタの次数")

    # 時間範囲選択スライダー
    time_range_slider = mo.ui.range_slider(start=0,
                                           stop=total_duration,
                                           step=0.1,
                                           value=(0, min(5.0, total_duration)),
                                           label=f"表示範囲(秒) -:{total_duration:.2f}s"
                                           )

    # フィルタ選択
    filter_selection = mo.ui.multiselect(
        options=["ローパスフィルタ", "移動平均"],
        value=["ローパスフィルタ"],
        label="適用するフィルタを選択"
    )

    mo.vstack([
        mo.md("### 🎛️ フィルタ設定"),
        filter_selection,
        mo.ui.array([window_slider, cutoff_input]),
        time_range_slider
    ])

    return


@app.cell
def _(apply_resampling, mo, plot_data, raw_data):
    if raw_data.empty:
        print("DataFrame is Empty")

    ORIGINA_FS = 200
    TARGET_FS = 100
    resampled_data = apply_resampling(raw_data, ORIGINA_FS, TARGET_FS)

    processed_fig = plot_data(resampled_data)

    plot_widget = mo.ui.plotly(processed_fig)
    plot_widget
    return


if __name__ == "__main__":
    app.run()
