import marimo

__generated_with = "0.14.16"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import os
    import glob
    import plotly.express as px
    from scipy.signal import butter, filtfilt, iirnotch, resample
    from scipy.fft import fft, fftfreq
    
    # === データ読み込み関数 ===
    def load_data(filepath: str) -> pd.DataFrame:
        """CSVファイルを読み込み，Pandasデータフレームとして返す．"""
        try:
            df = pd.read_csv(filepath, index_col=0)
            df.index = pd.to_datetime(df.index, unit='ns')
            return df
        except FileNotFoundError:
            return pd.DataFrame()
        except Exception as e:
            return pd.DataFrame()
    
    # === プロット関数 ===
    def plot_data(df: pd.DataFrame, title: str = "Signal Data"):
        """データフレームをインタラクティブなグラフとして描画する．"""
        if df.empty:
            return px.line(title="データがありません")
        
        fig = px.line(df, x=df.index, y=df.columns, title=title)
        fig.update_layout(
            xaxis_title='Time',
            yaxis_title='Value',
            legend_title='Signals'
        )
        return fig
    
    # === 信号処理関数 ===
    def apply_lowpass_filter(data: pd.DataFrame, cutoff: float, fs: float, order: int = 4) -> pd.DataFrame:
        """ローパスフィルタを適用"""
        if data.empty or fs <= 0 or not 0 < cutoff < fs / 2:
            return data.copy()
        
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            return data.copy()
        
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype="low", analog=False)
        
        result = data.copy()
        result[numeric_cols] = data[numeric_cols].apply(lambda col: filtfilt(b, a, col))
        return result
    
    def apply_highpass_filter(data: pd.DataFrame, cutoff: float, fs: float, order: int = 4) -> pd.DataFrame:
        """ハイパスフィルタを適用"""
        if data.empty or fs <= 0 or not 0 < cutoff < fs / 2:
            return data.copy()
        
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            return data.copy()
        
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype="high", analog=False)
        
        result = data.copy()
        result[numeric_cols] = data[numeric_cols].apply(lambda col: filtfilt(b, a, col))
        return result
    
    def apply_notch_filter(data: pd.DataFrame, fs: float, notch_freq: float = 50.0, quality: float = 30) -> pd.DataFrame:
        """ノッチフィルタを適用"""
        if data.empty or fs <= 0 or not 0 < notch_freq < fs / 2:
            return data.copy()
        
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            return data.copy()
        
        b, a = iirnotch(notch_freq, quality, fs)
        
        result = data.copy()
        result[numeric_cols] = data[numeric_cols].apply(lambda col: filtfilt(b, a, col))
        return result
    
    def apply_moving_average(data: pd.DataFrame, window_size: int) -> pd.DataFrame:
        """移動平均を適用"""
        if data.empty or window_size <= 0:
            return data.copy()
        
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            return data.copy()
        
        result = data.copy()
        result[numeric_cols] = data[numeric_cols].rolling(window=window_size, center=True).mean()
        return result
    
    def apply_rectification(data: pd.DataFrame, method: str = "full") -> pd.DataFrame:
        """整流を適用"""
        if data.empty:
            return data.copy()
        
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            return data.copy()
        
        result = data.copy()
        if method == "full":
            result[numeric_cols] = data[numeric_cols].abs()
        elif method == "half":
            result[numeric_cols] = data[numeric_cols].clip(lower=0)
        return result
    
    def apply_rms_envelope(data: pd.DataFrame, window_size: int) -> pd.DataFrame:
        """RMSエンベロープを適用"""
        if data.empty or window_size <= 0:
            return data.copy()
        
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            return data.copy()
        
        result = data.copy()
        result[numeric_cols] = (data[numeric_cols] ** 2).rolling(window=window_size, center=True).mean() ** 0.5
        return result
    
    def apply_resampling(data: pd.DataFrame, target_fs: float, current_fs: float) -> pd.DataFrame:
        """リサンプリングを適用"""
        if data.empty or target_fs <= 0 or current_fs <= 0:
            return data.copy()
        
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            return data.copy()
        
        num_samples = int(len(data) * target_fs / current_fs)
        result = data.copy()
        for col in numeric_cols:
            result[col] = resample(data[col], num_samples)
        return result
    
    def apply_fft(data: pd.DataFrame, fs: float, return_magnitude: bool = True) -> pd.DataFrame:
        """FFTを適用"""
        if data.empty or fs <= 0:
            return data.copy()
        
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            return data.copy()
        
        n = len(data)
        freqs = fftfreq(n, 1/fs)[:n//2]
        
        result_data = {}
        for col in numeric_cols:
            fft_vals = fft(data[col])
            if return_magnitude:
                result_data[col] = 2.0/n * np.abs(fft_vals[:n//2])
            else:
                result_data[col] = fft_vals[:n//2]
        
        result = pd.DataFrame(result_data, index=freqs)
        return result
    
    return (
        apply_fft,
        apply_highpass_filter,
        apply_lowpass_filter,
        apply_moving_average,
        apply_notch_filter,
        apply_rectification,
        apply_rms_envelope,
        apply_resampling,
        glob,
        load_data,
        mo,
        np,
        os,
        pd,
        plot_data,
        px,
    )


@app.cell
def _(glob, mo, os):
    # CSVファイル一覧を取得（WASM対応・デバッグ強化版）
    debug_info = []
    try:
        # marimo.notebook_location()を使用してWASM対応のパス取得
        notebook_location = mo.notebook_location()
        debug_info.append(f"notebook_location: {notebook_location}")
        
        if notebook_location:
            # GitHub Pages環境では、サブディレクトリにデプロイされる可能性があるため
            # 複数のパスパターンを試す
            possible_paths = [
                "public/data/15Subjects-7Gestures",  # 直接パス
                "/public/data/15Subjects-7Gestures", # 絶対パス
            ]
            
            # 実際に存在するファイルの組み合わせを定義
            subjects_gestures = [
                ("S0", ["emg-fistdwn", "emg-fistout", "emg-left", "emg-neut", "emg-opendwn", "emg-openout", "emg-right", "emg-tap", "emg-twodwn", "emg-twout"]),
                ("S1", ["emg-fistdwn", "emg-left", "emg-neut", "emg-opendwn", "emg-right", "emg-tap", "emg-twodwn", "emg-twout"]),
                ("S2", ["emg-fistdwn", "emg-fistout", "emg-left", "emg-neut", "emg-opendwn", "emg-openout", "emg-right", "emg-tap", "emg-twodwn", "emg-twout"])
            ]
            
            csv_files = []
            
            # 各パスパターンを試す
            for base_path in possible_paths:
                if str(notebook_location).startswith('http'):
                    # Web環境の場合、URLとして構築
                    for subject, gestures in subjects_gestures:
                        for gesture in gestures:
                            file_url = f"{notebook_location.rstrip('/')}/{base_path.lstrip('/')}/{subject}/{gesture}-{subject}.csv"
                            csv_files.append(file_url)
                            debug_info.append(f"Generated URL: {file_url}")
                    break
                else:
                    # ローカル環境の場合、パスとして構築
                    for subject, gestures in subjects_gestures:
                        for gesture in gestures:
                            file_path = notebook_location / base_path / subject / f"{gesture}-{subject}.csv"
                            csv_files.append(str(file_path))
                            debug_info.append(f"Generated path: {file_path}")
                    break
                    
            # より多くのファイルを追加（テスト用）
            if len(csv_files) < 10:  # もし少なすぎる場合
                for i in range(4, 15):
                    subject = f"S{i}"
                    for gesture in ["emg-fistdwn", "emg-left", "emg-neut", "emg-opendwn", "emg-right", "emg-tap", "emg-twodwn", "emg-twout"]:
                        if str(notebook_location).startswith('http'):
                            file_url = f"{notebook_location.rstrip('/')}/public/data/15Subjects-7Gestures/{subject}/{gesture}-{subject}.csv"
                            csv_files.append(file_url)
                        else:
                            file_path = notebook_location / "public" / "data" / "15Subjects-7Gestures" / subject / f"{gesture}-{subject}.csv"
                            csv_files.append(str(file_path))
        else:
            # フォールバック: 従来の相対パス
            csv_files = glob.glob("data/15Subjects-7Gestures/*/*.csv")
            debug_info.append("Using fallback glob pattern")
            
    except Exception as e:
        # エラー時のフォールバック
        csv_files = glob.glob("data/15Subjects-7Gestures/*/*.csv")
        debug_info.append(f"Exception occurred: {str(e)}")
        
    debug_info.append(f"Total files found: {len(csv_files)}")
    debug_info.append(f"First few files: {csv_files[:3] if csv_files else 'None'}")
    
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
    
    # デバッグ情報の表示
    debug_content = mo.md(f"""
    ### 🐛 デバッグ情報
    {chr(10).join(debug_info)}
    """)
    
    if not file_options:
        # CSVファイルが見つからない場合のエラーメッセージ
        display_content = mo.vstack([
            mo.md("❌ CSVファイルが見つかりません。データフォルダの場所を確認してください。"),
            debug_content
        ])
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
            file_selector,
            debug_content
        ])
    
    # 常に何かを表示
    display_content

    return file_selector


@app.cell
def _(file_selector, load_data, mo, np, os, pd):
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
