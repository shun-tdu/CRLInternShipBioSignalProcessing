import pandas as pd

"""
このファイルにはデータ読み込み関連の処理を書きます．
今回はCSVファイルを読み込む処理を書きます．
"""

def load_data(filepath: str) -> pd.DataFrame:
    """
    CSVファイルを読み込み，Pandasデータフレームとして返す．

    :param filepath: CSVファイルのパス
    :return: 読み込まれたデータ，エラー時は空のDFを返す．
    """
    try:
        # CSVを読み込んでデータフレームに変換する
        df = pd.read_csv(filepath, index_col=0)

        # インデックスをナノ秒単位のUnixスタンプとして日付形式に変換
        df.index = pd.to_datetime(df.index, unit='ns')

        print(f"✅ {filepath} を正常に読み込みました。")
        return df
    except FileNotFoundError:
        print(f"❌ エラー: {filepath} が見つかりません。")
        return pd.DataFrame()
    except Exception as e:
        print(f"❌ エラー: データの読み込み中に問題が発生しました - {e}")
        return pd.DataFrame()