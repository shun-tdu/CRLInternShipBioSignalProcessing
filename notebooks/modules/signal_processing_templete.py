import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt, iirnotch, resample
from scipy.fft import fft, fftfreq

"""
このファイルには信号処理のプログラムを書きます．
今回はデータフレームを受け取り，信号処理を施し，信号処理済みのデータフレームを返す関数を作る形で実装します．
"""

# --- 課題3: 各信号処理関数を実装してみよう！ ---

def apply_lowpass_filter(data: pd.DataFrame, cutoff: float, fs: float, order: int = 4) -> pd.DataFrame:
    """
    データフレームの各列にローパスフィルタを適用します．
    高周波のノイズを取り除き，信号を滑らかにする効果があります．

    ヒント:
    1. `scipy.signal.butter` を使ってフィルタの係数(b, a)を設計します．
       - `btype`引数を "low" に設定します．
    2. `scipy.signal.filtfilt` を使って，設計したフィルタをデータに適用します．
       - これにより，位相のズレなくフィルタリングできます．
    3. データフレームの各列に処理を適用するには，Pandasの`.apply()`メソッドが便利です．
    """
    # === ここに処理を書いてみよう ===
    pass  # この行は実装後に削除してください


def apply_highpass_filter(data: pd.DataFrame, cutoff: float, fs: float, order: int = 4) -> pd.DataFrame:
    """
    データフレームの各列にハイパスフィルタを適用します．
    信号のゆっくりとした変動（ドリフト）を取り除くのに役立ちます．

    ヒント:
    - ローパスフィルタとほとんど同じです！ `butter` 関数の `btype`引数を "high" に変えるだけです．
    """
    # === ここに処理を書いてみよう ===
    pass  # この行は実装後に削除してください


def apply_notch_filter(data: pd.DataFrame, fs: float, notch_freq: float = 50.0, quality: float = 30) -> pd.DataFrame:
    """
    ノッチフィルタで特定の周波数（ここでは電源ノイズの50Hz）を除去します．

    ヒント:
    - `scipy.signal.iirnotch` という，特定の周波数を狙い撃ちするための便利な関数があります．
    - これでフィルタ係数(b, a)を設計し，`filtfilt`で適用します．
    """
    # === ここに処理を書いてみよう ===
    pass  # この行は実装後に削除してください


def apply_moving_average(data: pd.DataFrame, window_size: int) -> pd.DataFrame:
    """
    データフレームの各列に移動平均を適用します．
    簡単なローパスフィルタとして機能し，信号を滑らかにします．

    ヒント:
    - Pandasのデータフレームには，`.rolling()` という素晴らしい機能があります．
    - `.rolling(window=window_size).mean()` のように使うと，指定した窓サイズで移動平均を計算できます．
    """
    # === ここに処理を書いてみよう ===
    pass  # この行は実装後に削除してください


def apply_rectification(data: pd.DataFrame, method: str = "full") -> pd.DataFrame:
    """
    全波整流または半波整流を適用します．
    信号の振幅の大きさを評価する際の前処理として使われます．

    ヒント:
    - 全波整流は，単純に信号の絶対値を取るだけです．Pandasの `.abs()` メソッドが使えます．
    - 半波整流は，負の値をすべて0にします．Pandasの `.clip(lower=0)` メソッドが便利です．
    """
    # === ここに処理を書いてみよう ===
    pass  # この行は実装後に削除してください


def apply_rms_envelope(data: pd.DataFrame, window_size: int) -> pd.DataFrame:
    """
    RMS（二乗平均平方根）エンベロープを計算します．
    筋電図などの活動強度を評価するのによく使われます．

    ヒント:
    - 移動平均の応用です．
    - 1. まず信号を2乗します (`data**2`)．
    - 2. その結果に `.rolling().mean()` を適用します．
    - 3. 最後に平方根を取ります (`np.sqrt(...)` または `...**0.5`)．
    """
    # === ここに処理を書いてみよう ===
    pass  # この行は実装後に削除してください


def apply_resampling(data: pd.DataFrame, original_fs: float, target_fs: float) -> pd.DataFrame:
    """
    データフレームの各列を指定したサンプリング周波数でリサンプリングします．

    ヒント:
    - `scipy.signal.resample` を使います．
    - 新しいデータ点数を計算する必要があります: `新しい点数 = 元の点数 * (目標周波数 / 元の周波数)`
    """
    # === ここに処理を書いてみよう ===
    pass  # この行は実装後に削除してください


def apply_fft(data: pd.DataFrame, fs: float) -> pd.DataFrame:
    """
    FFT（高速フーリエ変換）を適用し，周波数領域のデータフレームを返します．
    信号にどの周波数成分がどれくらい含まれているかを分析できます．

    ヒント:
    - `scipy.fft.fft` でフーリエ変換を計算します．
    - `scipy.fft.fftfreq` で，対応する周波数軸を作成します．
    - 通常，結果の半分だけ（正の周波数）を使い，振幅を計算します (`np.abs(...)`)．
    """
    # === ここに処理を書いてみよう ===
    pass  # この行は実装後に削除してください

