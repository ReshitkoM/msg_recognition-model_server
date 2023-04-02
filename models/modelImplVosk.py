import io
import json
import logging
import sys

import wave
from pydub import AudioSegment
from vosk import Model, KaldiRecognizer, SetLogLevel

class ModelImplVosk():

    def __init__(self, modelName) -> None:
        SetLogLevel(0)
        self.model = Model(model_name=modelName)

    def _convert_from_ogg(self, oggAudio):
        song = AudioSegment.from_ogg(oggAudio)
        song = song.set_sample_width(2)
        output = io.BytesIO()
        return song.export(output, format="wav")

    def _preproc(self, data):
        wavAudio = self._convert_from_ogg(io.BytesIO(data))
        wf = wave.open(wavAudio, "rb")
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            raise Exception(f"Audio file must be WAV format mono PCM. Received channels: {wf.getnchannels()}, samplewidth: {wf.getsampwidth()}, comptype:{wf.getcomptype()}.")

        return wf

    def _postproc(self, rec):
        res = json.loads(rec.FinalResult())
        return res["text"]

    def predict(self, oggAudio):
        wav = self._preproc(oggAudio)

        rec = KaldiRecognizer(self.model, wav.getframerate())
        rec.SetWords(True)
        rec.SetPartialWords(True)

        while True:
            data = wav.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                pass
            else:
                pass
            pass

        return self._postproc(rec)