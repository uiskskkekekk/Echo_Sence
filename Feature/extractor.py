import os
from keras import models
import numpy as np

from .utils import min_max_scaling
from .utils.yt_music import Downloader
from .utils.score import Audio
import joblib
from sklearn.preprocessing import StandardScaler

class FeatureExtractor:
    def __init__(self, encoder_path: str, scaler_path: str, runtime_dir: str = "./data/music/main_runtime"):
        self.encoder = models.load_model(encoder_path) if os.path.isfile(encoder_path) else None
        self.scaler = joblib.load(scaler_path) if os.path.isfile(scaler_path) else None
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
        scaled_mfcc = self._scaling_data(mfcc)
        scaled_mfcc = np.expand_dims(scaled_mfcc, axis=-1)
        scaled_mfcc = np.expand_dims(scaled_mfcc, axis=0)
        scaled_mfcc = np.nan_to_num(scaled_mfcc, nan = 0.)
        return scaled_mfcc

    def _scaling_data(self, data):
        assert isinstance(self.scaler, StandardScaler)
        return self.scaler.transform(data)
    
    def _get_features(self, filepath):
        assert isinstance(self.encoder, models.Model), "self.encoder is not loaded"
        
        scaled_mfcc = self._mfcc_to_X(filepath)
        res = self.encoder.predict(scaled_mfcc)
        res = res.flatten()
        res = min_max_scaling(res)
        return res
    
    def extract(self, yt_link: str) -> np.ndarray:
        if not self.is_loaded: return None
        
        filepath = self._yt2mp3(yt_link)
        if filepath is not None:
            features = self._get_features(filepath)
            os.remove(filepath)
            return features
        return None
    
    def extract_from_file(self, filepath):
        if filepath is not None:
            features = self._get_features(filepath)
            os.remove(filepath)
            return features
        return None
        

    def rebuild_feature(self, features_str: str):
        return np.array(features_str.split(","), dtype=np.float32)