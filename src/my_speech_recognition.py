import datetime
import re

import kanjize
import pytz
import requests
import soundfile as sf
import speech_recognition as sr

from config import Config


class SpeechRecognition:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def recognize_speech_from_file(self, file_path):
        """
        音声ファイルから音声を取得

        Args:
            file_path (str): 音声ファイルのパス

        Returns:
            audio: 音声データ
        """
        audio_file = sr.AudioFile(file_path)
        with audio_file as source:
            audio = self.recognizer.record(source)
        return audio

    def recognize_speech_from_mic(self):
        """
        マイクから音声を取得

        Returns:
            audio: 音声データ
        """
        mic = sr.Microphone()
        with mic as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
        return audio

    def create_response(self, audio):
        """
        音声データをテキストに変換

        Args:
            audio: 音声データ

        Returns:
            str: 認識されたテキストまたはエラーメッセージ
        """
        try:
            text = self.recognizer.recognize_google(audio, language="ja-JP")
        except sr.UnknownValueError:
            # 認識できなかった場合のメッセージ
            return "音声を認識できませんでした"
        except sr.RequestError as e:
            # サービスエラー時のメッセージ
            return f"サービスにアクセスできませんでした; {e}"

        return text

    def extract_date(self, text):
        """
        テキストから日付を抽出

        Args:
            text (str): テキスト

        Returns:
            str: 抽出された日付（YYYYMMDD形式）またはNone
        """
        # TODO: ここら辺はもう少し幅を増やしたり曖昧性の対応ができると思う
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        date_pattern = r"(\d{1,2})月(\d{1,2})日|(\d{1,2})日|今日|明日|([一二三四五六七八九十]+)月([一二三四五六七八九十]+)日|([一二三四五六七八九十]+)日"
        match = re.search(date_pattern, text)

        if match:
            if match.group(0) == "今日":
                # 今日の日付を返す
                return today.strftime("%Y%m%d")
            elif match.group(0) == "明日":
                # 明日の日付を返す
                return tomorrow.strftime("%Y%m%d")
            elif match.group(1) and match.group(2):
                month = int(match.group(1))
                day = int(match.group(2))
                year = today.year
                if month < today.month or (
                    month == today.month and day < today.day
                ):
                    # 過去の月日の場合は来年のものとみなす
                    year += 1
                return datetime.date(year, month, day).strftime("%Y%m%d")
            elif match.group(3):
                day = int(match.group(3))
                month = today.month
                year = today.year
                if day < today.day:
                    # 過去の日の場合は来月とみなす
                    month += 1
                    if month > 12:
                        month = 1
                        year += 1
                return datetime.date(year, month, day).strftime("%Y%m%d")
            elif match.group(4) and match.group(5):
                # 漢数字から数値に変換
                month = kanjize.kanji2number(match.group(4))
                day = kanjize.kanji2number(match.group(5))
                year = today.year
                if month < today.month or (
                    month == today.month and day < today.day
                ):
                    # 過去の月日の場合は来年のものとみなす
                    year += 1
                return datetime.date(year, month, day).strftime("%Y%m%d")
            elif match.group(6):
                # 漢数字から数値に変換
                day = kanjize.kanji2number(match.group(6))
                month = today.month
                year = today.year
                if day < today.day:
                    # 過去の日の場合は来月とみなす
                    month += 1
                    if month > 12:
                        month = 1
                        year += 1
                return datetime.date(year, month, day).strftime("%Y%m%d")
        return None

    def get_schedule(self, date):
        """
        指定された日付に基づいてスケジュールを取得

        Args:
            date (str): 日付（YYYYMMDD形式）

        Returns:
            dict: スケジュールのJSONデータ
        """

        # APIからスケジュールを取得
        config = Config()
        response = requests.get(config.api_url, params={"Day": date})
        return response.json()
