import numpy as np
import sounddevice as sd
import torch
from espnet2.bin.tts_inference import Text2Speech
from espnet2.utils.types import str_or_none
from scipy.io.wavfile import write


class TextToSpeech:
    def __init__(self):
        self.text2speech = Text2Speech.from_pretrained(
            model_tag=str_or_none("kan-bayashi/jsut_full_band_vits_prosody"),
            vocoder_tag=str_or_none("none"),
            device="cpu",
            # device="0"
        )

    def output_speech(self, response_text):
        """
        音声出力

        Args:
            response_text (str): 音声に変換するテキスト
        """
        pause = np.zeros(30000, dtype=np.float32)
        sentence_list = response_text.split("<pause>")
        wav_list = []

        for sentence in sentence_list:
            with torch.no_grad():
                result = self.text2speech(sentence)["wav"]
                wav_list.append(
                    np.concatenate([result.view(-1).cpu().numpy(), pause])
                )

        final_wav = np.concatenate(wav_list)
        final_wav = (final_wav * 32767).astype(np.int16)

        # 再生
        sd.play(final_wav, self.text2speech.fs)
        sd.wait()
