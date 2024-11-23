import argparse
import warnings

from my_speech_recognition import SpeechRecognition
from schedule_formatter import format_schedule
from text_to_speech import TextToSpeech

# すべての警告を無視
warnings.filterwarnings("ignore")


class Main:

    def __init__(self) -> None:
        self.speech_recognition = SpeechRecognition()
        self.text_to_speech = TextToSpeech()

    def process_schedule(self, audio):
        """
        実際の処理

        Args:
            audio: 音声データ
        """
        text = self.speech_recognition.create_response(audio)
        print(text)
        date = self.speech_recognition.extract_date(text)
        if date:
            schedule = self.speech_recognition.get_schedule(date)
            formatted_schedule = format_schedule(date, schedule)
            print(formatted_schedule)
            self.text_to_speech.output_speech(formatted_schedule)
            return
        else:
            print("入力から有効な日付を抽出できませんでした。")
            return

    def main(self, input_type="file", file_path="test.wav"):
        """
        メイン処理\n
        マイク入力orファイル入力で分岐

        Args:
            input_type (str): 入力タイプ（"file"または"mic"）。
            file_path (str): 音声ファイルのパス（input_typeが"file"の場合）。
        """
        if input_type == "file":
            # ファイル入力の場合
            audio = self.speech_recognition.recognize_speech_from_file(
                file_path
            )

            self.process_schedule(audio)

        elif input_type == "mic":
            # 音声入力の場合
            while True:
                command = input(
                    "---メニュー---\n1：音声入力開始\n0：終了\n>>> "
                )
                if command.isdigit() and int(command) == 1:
                    # 音声入力開始
                    print("Recording...")
                    audio = self.speech_recognition.recognize_speech_from_mic()

                    self.process_schedule(audio)

                elif command.isdigit() and int(command) == 0:
                    # 終了
                    break


if __name__ == "__main__":
    main = Main()
    main.main(input_type="mic")
    # main.main(
    #     input_type="file",
    #     file_path="./test_voice/test_tomorrow.wav",
    # )  # 音声ファイル入力の場合
