import os
from keras import models
import numpy as np
from typing import Literal

from .utils import min_max_scaling
from .utils.yt_music import Downloader
from .utils.score import Audio

class FeatureExtractor:
    def __init__(self, encoder_path: str, runtime_dir: str = "./data/music/main_runtime"):
        self.encoder = models.load_model(encoder_path) if os.path.isfile(encoder_path) else None
        self.runtime_dir = runtime_dir
        self.is_loaded = os.path.isfile(encoder_path)
    
    def _yt2mp3(self, yt_link):
        if not os.path.exists(self.runtime_dir):
            os.makedirs(self.runtime_dir)
        return Downloader.download(yt_link, self.runtime_dir, True)

    def _mfcc_to_X(self, filepath):
        audio = Audio(filepath=filepath, duration=30)
        _, _, mfcc = audio.get_mfcc(80, segment_size=10)
        mfcc = np.array(mfcc)
        mfcc = mfcc.transpose(2, 1, 0)
        mfcc = np.reshape(mfcc, (130, -1))
        mfcc = np.expand_dims(mfcc, axis=-1)
        mfcc = np.expand_dims(mfcc, axis=0)
        mfcc = np.nan_to_num(mfcc, nan = 0.)
        return mfcc

    def _get_features(self, filepath):
        assert isinstance(self.encoder, models.Model), "self.encoder is not loaded"
        
        mfcc = self._mfcc_to_X(filepath)
        res = self.encoder.predict(mfcc)
        res = res.flatten()
        res = min_max_scaling(res)
        return res
    
    def extract(self, yt_link: str, format: Literal["str", "float32"]="str"):
        if not self.is_loaded: return None
        
        filepath = self._yt2mp3(yt_link)
        if filepath is not None:
            features = self._get_features(filepath)
            os.remove(filepath)
            return features if format == "float32" else ",".join(map(str, features))
        return None

    def rebuild_feature(self, features_str: str):
        return np.array(features_str.split(","), dtype=np.float32)