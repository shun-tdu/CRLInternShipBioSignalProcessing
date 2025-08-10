import marimo

__generated_with = "0.14.16"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import os
    from glob import glob

    from modules.data_loader import load_data
    from modules.plotting import plot_data
    from modules.signal_processing import apply_lowpass_filter, apply_highpass_filter, apply_notch_filter, apply_moving_average,  apply_rms_envelope, apply_rectification, apply_resampling, apply_fft
    return (
        apply_fft,
        apply_highpass_filter,
        apply_lowpass_filter,
        apply_moving_average,
        apply_notch_filter,
        apply_rectification,
        apply_rms_envelope,
        glob,
        load_data,
        mo,
        np,
        os,
        plot_data,
    )


@app.cell
def _(glob, mo, os):
    # CSVファイル一覧を取得（相対パス）
    csv_files = glob("data/15Subjects-7Gestures/*/*.csv")
    csv_files.sort()

    # ファイル選択のための辞書を作成（表示名: パス）
    file_options = {}
    for file_path in csv_files:
        # ファイル名のみを取得して表示用の名前を作成
        basename = os.path.basename(file_path)
        dirname = os.path.basename(os.path.dirname(file_path))
        display_name = f"{dirname}/{basename}"
        file_options[display_name] = file_path
    
    file_selector = None
    display_content = None
    
    if not file_options:
        # CSVファイルが見つからない場合のエラーメッセージ
        display_content = mo.md("❌ CSVファイルが見つかりません。データフォルダの場所を確認してください。")
    else:
        # デフォルトファイルを設定
        default_display = "S0/emg-fistdwn-S0.csv"
        if default_display not in file_options:
            default_display = list(file_options.keys())[0]
        
        # ファイル選択ドロップダウン
        file_selector = mo.ui.dropdown(
            options=file_options,
            value=default_display,
            label="CSVファイルを選択",
            searchable=True
        )
        
        display_content = mo.vstack([
            mo.md("### 📁 ファイル選択"),
            file_selector
        ])
    
    # 常に何かを表示
    display_content

    return file_selector


@app.cell
def _(file_selector, load_data, mo, np, os):
    import pandas as pd
    SAMPLING_RATE = 200 
    
    # file_selectorがNoneの場合（CSVファイルが見つからない場合）の処理
    if file_selector is None:
        raw_data = pd.DataFrame()
        total_duration = 0.0
        info_message = "❌ CSVファイルが見つからないため、データを読み込めません"
    else:
        raw_data = load_data(file_selector.value)

        if not raw_data.empty:
            # 200Hzの時間軸を作成（0秒スタート）
            time_interval = 1.0 / SAMPLING_RATE  # 0.005秒間隔
            raw_data.index = np.arange(len(raw_data)) * time_interval
            total_duration = raw_data.index[-1]

            selected_file_name = os.path.basename(file_selector.value)
            info_message = f"""
            📊 **データ読み込み完了**
            - 選択ファイル: {selected_file_name}
            - サンプル数: {len(raw_data)}
            - 総時間: {total_duration:.2f} 秒
            - サンプリング周波数: {SAMPLING_RATE} Hz
            - 時間間隔: {time_interval:.3f} 秒
            """
        else:
            total_duration = 0.0
            info_message = "❌ データの読み込みに失敗しました"

    mo.md(info_message)

    return SAMPLING_RATE, raw_data, total_duration


@app.cell
def _(mo, total_duration):
    # UIコンポーネントの定義
    # 信号処理のパラメータ
    # ローパスフィルタ
    lowpass_cutoff_input = mo.ui.slider(1.0, 100.0, step=0.1, value=5.0, label="ローパスフィルタのカットオフ周波数 [Hz]")
    # ハイパスフィルタ
    highpass_cutoff_input = mo.ui.slider(1.0, 100.0, step=0.1, value=5.0, label="ハイパスフィルタのカットオフ周波数 [Hz]")
    # ノッチフィルタ
    notch_freq_input = mo.ui.number(1.0, 100.0, step=0.1, value = 50.0, label="ノッチフィルタの周波数 [Hz]")
    # 移動平均
    window_slider = mo.ui.slider(1, 101, step=2, value=21, label="移動平均の窓長")
    # RMSエンベロープ
    rms_window_slider = mo.ui.slider(1, 200, step=1, value=40.0, label="RNSエンベロープの窓長さ")
    # 時間範囲選択
    time_range_slider = mo.ui.range_slider(start=0,
                                           stop=total_duration,
                                           step=0.1,
                                           value=(0, min(5.0, total_duration)),
                                           label=f"表示範囲(秒) -:{total_duration:.2f}s"
                                          )

    # フィルタ選択
    filter_selection = mo.ui.multiselect(
        options=["ローパスフィルタ", 
                 "ハイパスフィルタ",
                 "ノッチフィルタ",
                 "移動平均",
                 "全波整流",
                 "半波整流",
                 "RMSエンベロープ"
                ],
        value=["ローパスフィルタ"],
        label="適用するフィルタを選択"
    )

    mo.vstack([
        mo.md("### 🎛️ フィルタ設定"),
        filter_selection,
        lowpass_cutoff_input,
        highpass_cutoff_input,
        notch_freq_input,
        window_slider,
        rms_window_slider,
        time_range_slider
    ])

    return (
        filter_selection,
        highpass_cutoff_input,
        lowpass_cutoff_input,
        notch_freq_input,
        rms_window_slider,
        time_range_slider,
        window_slider,
    )


@app.cell
def _(
    SAMPLING_RATE,
    apply_fft,
    apply_highpass_filter,
    apply_lowpass_filter,
    apply_moving_average,
    apply_notch_filter,
    apply_rectification,
    apply_rms_envelope,
    filter_selection,
    highpass_cutoff_input,
    lowpass_cutoff_input,
    mo,
    notch_freq_input,
    plot_data,
    raw_data,
    rms_window_slider,
    time_range_slider,
    window_slider,
):
    if raw_data.empty:
        result = mo.md("❌ データがありません")
    else:
        # フィルタ処理
        processed_data = raw_data.copy()

        # 選択されたフィルタを順番に適用
        if "ローパスフィルタ" in filter_selection.value:
            processed_data = apply_lowpass_filter(
                processed_data,
                cutoff=lowpass_cutoff_input.value,
                fs=SAMPLING_RATE
            )
        if "ハイパスフィルタ" in filter_selection.value:
            processed_data = apply_highpass_filter(
                processed_data,
                cutoff=highpass_cutoff_input.value,
                fs=SAMPLING_RATE
            )
        if "ノッチフィルタ" in filter_selection.value:
            processed_data = apply_notch_filter(
                processed_data,
                fs=SAMPLING_RATE,
                notch_freq=notch_freq_input.value,
                quality=30
            )
        if "移動平均" in filter_selection.value:
            processed_data = apply_moving_average(
                processed_data,
                window_slider.value
            )
        if "全波整流" in filter_selection.value:
            processed_data = apply_rectification(
                processed_data,
                method="full"
            )
        if "半波整流" in filter_selection.value:
            processed_data = apply_rectification(
                processed_data,
                method="half"
            )
        if "RMSエンベロープ" in filter_selection.value:
            processed_data = apply_rms_envelope(
                processed_data,
                window_size=int(rms_window_slider.value)
            )

        # 時間範囲でスライス
        start_time, end_time = time_range_slider.value
        time_mask = (processed_data.index >= start_time) & (processed_data.index <= end_time)
        sliced_data = processed_data[time_mask]

        # デバッグ情報
        info_text = f"""
        📈 **処理情報**
        - 適用フィルタ: {', '.join(filter_selection.value) if filter_selection.value else 'なし'}
        - 表示時間範囲: {start_time:.2f}s - {end_time:.2f}s
        - 表示データ点数: {len(sliced_data)} / {len(processed_data)}
        """    

        # プロット作成
        if not sliced_data.empty:
            # 時間領域のプロット
            time_domain_fig = plot_data(
                sliced_data,
                title=f"時間領域: EMG信号 ({start_time:.2f}s - {end_time:.2f}s)"
            )

            # 周波数領域のプロット(FFT)
            fft_data = apply_fft(sliced_data, fs=SAMPLING_RATE, return_magnitude=True)

            # 周波数軸のラベルを更新
            freq_domain_fig = plot_data(
                fft_data,
                title=f"周波数領域: FFT振幅スペクトル ({start_time:.2f}s - {end_time:.2f}s)"
            )

            # X軸のラベルを周波数に変更
            freq_domain_fig.update_layout(
                xaxis_title = '周波数 [Hz]',
                yaxis_title = '振幅'
            )

            # 両方のプロットを縦に並べて表示
            result_time_domain = mo.vstack([
                mo.md("### 🕒 時間領域"),
                mo.ui.plotly(time_domain_fig),
            ])

            result_freq_domain = mo.vstack([
                mo.md("### 📊 周波数領域"),
                mo.ui.plotly(freq_domain_fig)
            ])

            figures = mo.hstack([result_time_domain, result_freq_domain])

            result = mo.vstack([
                mo.md(info_text),
                figures
            ])
        else:
            result = mo.vstack([
                mo.md(info_text),
                mo.md("⚠️ 指定した時間範囲にデータがありません")
            ])
    result

    return


if __name__ == "__main__":
    app.run()
