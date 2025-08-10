import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt, iirnotch, resample
from scipy.fft import fft, fftfreq

"""
このファイルには信号処理のプログラムを書きます．
今回はデータフレームを受け取り，信号処理を施し，信号処理済みのデータフフレームを返す関数を作る形で実装します．
今回扱った以外の信号処理を追加したい場合も，入力と出力の型をPandasのデータフレームにすれば問題なく動作します．
"""

def apply_lowpass_filter(
        data: pd.DataFrame,
        cutoff: float,
        fs:float,
        order: int = 4
    ) -> pd.DataFrame:
    """
    データフレームの各列にローパスフィルタを適用し，処理後のデータフレームを返す．

    :param data: 入力データ [-]
    :param cutoff: カットオフ周波数 [Hz]
    :param fs: サンプリング周波数 [Hz]
    :param order: フィルタの次数 [-]
    :return: フィルタ処理後のデータ [-]
    """
    # --- 安全性チェック ---
    if data.empty:
        return data.copy()
    if fs <= 0:
        raise ValueError("サンプリング周波数fsは正の値である必要があります．")
    if not 0 < cutoff < fs / 2:
        raise ValueError("カットオフ周波数cutoffは0とナイキスト周波数(fs/2)の間である必要があります．")
    if not isinstance(order, int) or order <= 0:
        raise ValueError("フィルタの次数orderは正の整数である必要があります．")

    # 数値列のみを処理対象とする
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) == 0:
        return data.copy() # 処理対象の列がない場合はそのまま返す

    # フィルタ設計
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype="low", analog=False)

    # フィルタ適用
    result = data.copy()
    result[numeric_cols] = data[numeric_cols].apply(lambda col: filtfilt(b, a, col))

    return result


def apply_highpass_filter(data: pd.DataFrame, cutoff: float, fs: float, order: int = 4) -> pd.DataFrame:
    """
    データフレームの各列にローパスフィルタを適用し，処理後のデータフレームを返す．

    :param data: 入力データ [-]
    :param cutoff: カットオフ周波数 [Hz]
    :param fs: サンプリング周波数 [Hz]
    :param order: フィルタの次数 [-]
    :return: フィルタ処理後のデータ [-]
    """
    # --- 安全性チェック ---
    if data.empty:
        return data.copy()
    if fs <= 0:
        raise ValueError("サンプリング周波数fsは正の値である必要があります．")
    if not 0 < cutoff < fs / 2:
        raise ValueError("カットオフ周波数cutoffは0とナイキスト周波数(fs/2)の間である必要があります．")
    if not isinstance(order, int) or order <= 0:
        raise ValueError("フィルタの次数orderは正の整数である必要があります．")

    # 数値列のみを処理対象とする
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) == 0:
        return data.copy()

    # フィルタ設計
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype="high", analog=False)

    # フィルタ適用
    result = data.copy()
    result[numeric_cols] = data[numeric_cols].apply(lambda col: filtfilt(b, a, col))

    return result


def apply_notch_filter(data: pd.DataFrame, fs: float, notch_freq: float = 50.0, quality: float = 30) -> pd.DataFrame:
    """
    ノッチフィルタで商用電源ノイズ（50Hz）を除去

    :param data: 入力データ [-]
    :param fs: サンプリング周波数 [Hz]
    :param notch_freq: 除去したい周波数 [Hz]
    :param quality: Q値の鋭さ
    :return: フィルタ処理後のデータ [-]
    """
    # --- 安全性チェック ---
    if data.empty:
        return data.copy()
    if fs <= 0:
        raise ValueError("サンプリング周波数fsは正の値である必要があります．")
    if not 0 < notch_freq < fs / 2:
        raise ValueError("除去したい周波数notch_freqは0とナイキスト周波数(fs/2)の間である必要があります．")
    if quality <= 0:
        raise ValueError("Q値qualityは正の値である必要があります．")

    # 数値列のみを処理対象とする
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) == 0:
        return data.copy()

    # ノッチフィルタの設計
    b, a = iirnotch(notch_freq, quality, fs)

    # フィルタ適用
    result = data.copy()
    result[numeric_cols] = data[numeric_cols].apply(lambda col: filtfilt(b, a, col))

    return result


def apply_moving_average(data: pd.DataFrame, window_size: int) -> pd.DataFrame:
    """
    データフレームの各列に移動平均を適用し，処理後のデータフレームを返す．

    :param data:入力データ [-]
    :param window_size: 移動平均のウィンドウサイズ [-]
    :return: 平滑処理後のデータ [-]
    """
    # --- 安全性チェック ---
    if data.empty:
        return data.copy()
    if not isinstance(window_size, int) or window_size <= 0:
        raise ValueError("ウィンドウサイズwindow_sizeは正の整数である必要があります．")

    # 数値列のみを処理対象とする
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) == 0:
        return data.copy()


    # 移動平均を適用
    result = data.copy()
    result[numeric_cols] = data[numeric_cols].rolling(
        window=window_size,
        center=True,
        min_periods=1
    ).mean()

    return result


def apply_rms_envelope(data: pd.DataFrame, window_size: int) -> pd.DataFrame:
    """
    RMSエンベロープを適用し，処理後のデータフレームを返す．．

    :param data: 入力データ [-]
    :param window_size: 移動RMSのウィンドウサイズ [-]
    :return: RMSエンベロープ [-]
    """
    # --- 安全性チェック ---
    if data.empty:
        return data.copy()
    if not isinstance(window_size, int) or window_size <= 0:
        raise ValueError("ウィンドウサイズwindow_sizeは正の整数である必要があります．")

    # 数値列のみを処理対象とする
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) == 0:
        return data.copy()

    # 移動RMSウィンドウ
    result = data.copy()
    result[numeric_cols] = data[numeric_cols].rolling(window=window_size, center=True, min_periods=1).apply(
        lambda x: np.sqrt(np.mean(x**2)),
        raw=True # 生のNumpy配列をラムダ関数に渡すことで高速化
    )
    return result


def apply_rectification(data: pd.DataFrame, method: str = "full") -> pd.DataFrame:
    """
    全波整流または半波整流を適用し，処理後のデータフレームを返す．

    :param data: 入力データ [-]
    :param method: 整流の方法. "full" (全波) または "half" (半波) [-]
    :return: 整流後のデータ [-]
    """
    # --- 安全性チェック ---
    if data.empty:
        return data.copy()
    if method not in ["full", "half"]:
        raise ValueError("methodは 'full' または 'half' である必要があります．")

    # 数値列のみを処理対象とする
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) == 0:
        return data.copy()

    result = data.copy()
    if method == "full":
        result[numeric_cols] = data[numeric_cols].abs()
    elif method == "half":
        result[numeric_cols] = data[numeric_cols].clip(lower=0)

    return result


def apply_resampling(data: pd.DataFrame, original_fs: float, target_fs: float) -> pd.DataFrame:
    """
    データフレームの各列を指定したサンプリング周波数でリサンプリングし，処理後のデータフレームを返す．
    :param data: 入力データ [-]
    :param original_fs: 元のサンプリング周波数 [Hz]
    :param target_fs: 目標のサンプリング周波数 [Hz]
    :return: リサンプリング処理後のデータ [-]
    """
    # --- 安全性チェック ---
    if data.empty:
        return data.copy()
    if original_fs <= 0 or target_fs <= 0:
        raise ValueError("サンプリング周波数は正の値である必要があります．")

    if original_fs == target_fs:
        return data.copy()

    # 元のサンプル数
    original_length = len(data)

    # 新しいサンプル数
    new_length = int(original_length * target_fs / original_fs)

    # サンプル数が変わらない場合はそのまま返す
    if new_length == original_length:
        return data.copy()

    # 数値列のみを取得
    numeric_columns = data.select_dtypes(include=[np.number]).columns

    # 結果用のデータフレームを作成
    result = pd.DataFrame()

    # 各数値列にリサンプリングを適用
    for col in numeric_columns:
        resampled_signal = resample(data[col].values, new_length)
        result[col] = resampled_signal

    # 数値インデックスを再設定
    new_time_interval = 1.0 / target_fs
    result.index = np.arange(new_length) * new_time_interval

    return result


def apply_fft(data: pd.DataFrame, fs: float, return_magnitude: bool = True) -> pd.DataFrame:
    """
    データフレームの各列にFFTを適用し，周波数領域のデータフレームを返す．

    :param data: 入力データ(時間領域) [-]
    :param fs: サンプリング周波数 [Hz]
    :param return_magnitude: Trueの場合振幅スペクトル，Falseの場合複素数スペクトルを返す [-]
    :return: FFT処理後のデータ(周波数領域) [-]
    """

    # --- 安全性チェック ---
    if data.empty:
        return data.copy()
    if fs <= 0:
        raise ValueError("サンプリング周波数fsは正の値である必要があります．")

    # 数値列のみを取得
    numeric_columns = data.select_dtypes(include=[np.number]).columns

    # 結果用のデータフレームを作成
    result = pd.DataFrame()

    # データ長を取得
    n_samples= len(data)

    # 周波数軸を作成(正の周波数のみ)
    freqs = fftfreq(n_samples, 1 / fs)[:n_samples // 2]

    # 各数値列にFFTを適用
    for col in numeric_columns:
        # FFTを実行
        fft_values = fft(data[col].values)

        # 正の周波数成分のみを取得
        fft_positive = fft_values[:n_samples // 2]

        if return_magnitude:
            # 振幅スペクトルを計算
            magnitude = np.abs(fft_positive)
            magnitude[1:] *= 2 # 直流成分以外を2倍にして片側スペクトルに変換
            result[col] = magnitude
        else:
            # 複素数スペクトルをそのまま返す
            result[col] = fft_positive

    # 周波数軸をインデックスに設定
    result.index = freqs

    return result