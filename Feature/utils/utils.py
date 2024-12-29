import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

import librosa
import numpy as np
import os
import ast
import sys

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import pandas as pd

from typing import Literal, Optional, Callable
from scipy.stats import kurtosis, skew
from sklearn.preprocessing import LabelEncoder
from keras.src.models import Model
from keras.src.callbacks import Callback
from sklearn.manifold import TSNE

class AudioFeatures:
    """
    AudioFeatures is a container class for storing various statistical features derived from audio data.

    This class holds common statistical measures such as kurtosis, maximum, mean, median, minimum, skewness, 
    and standard deviation, which are often computed from audio features like MFCCs, chroma, or spectrograms.

    Attributes
    ----------
    kurtosis : Optional[np.ndarray]
        The kurtosis of the audio feature data, describing the "tailedness" of the data distribution.
        
    max : Optional[np.ndarray]
        The maximum value for each feature over time, providing a sense of the peak values in the data.

    mean : Optional[np.ndarray]
        The mean value for each feature, giving a central tendency of the data distribution.

    median : Optional[np.ndarray]
        The median value for each feature, providing a robust measure of central tendency less affected by outliers.

    min : Optional[np.ndarray]
        The minimum value for each feature, representing the smallest observed values.

    skew : Optional[np.ndarray]
        The skewness of the audio feature data, describing the asymmetry of the data distribution.

    std : Optional[np.ndarray]
        The standard deviation for each feature, indicating how much the values fluctuate over time.
    """

    def __init__(
        self,
        kurtosis: Optional[np.ndarray] = None,
        max: Optional[np.ndarray] = None,
        mean: Optional[np.ndarray] = None,
        median: Optional[np.ndarray] = None,
        min: Optional[np.ndarray] = None,
        skew: Optional[np.ndarray] = None,
        std: Optional[np.ndarray] = None
    ):
        self.kurtosis = kurtosis
        self.max = max
        self.mean = mean
        self.median = median
        self.min = min
        self.skew = skew
        self.std = std
        
    def __str__(self):
        df = pd.DataFrame({
            "kutosis": self.kurtosis,
            "max": self.max,
            "mean": self.mean,
            "median": self.median,
            "min": self.min,
            "skew": self.skew,
            "std": self.std
        })
        return df.__str__()

    def __array__(self, dtype=None):
        return self.to_array(dtype=dtype)
    
    def to_array(self, dtype=None):
        return np.array([
            self.kurtosis,
            self.max,
            self.mean,
            self.median,
            self.min,
            self.skew,
            self.std
        ], dtype=dtype)
    
class AudioTools:
    @classmethod
    def get_max(cls, data: np.ndarray, sr=22050, y_axis: Literal["chroma", "mel"] = None, show = True, frame_end = 1000):
        """
        Get row-based max array from the input audio feature matrix.

        This method computes the maximum value for each column (time frame) across the rows (features) 
        in the input 2D audio feature matrix `data`. The result is a binary matrix where the maximum 
        value in each column is marked as 1, and all other values are set to 0.

        Optionally, the method can display the original audio feature matrix, its dB-scaled version, 
        and the binary max array using `librosa`'s visualization tools if `show` is set to True.

        Arguments
        -------
            data (np.ndarray): 
                A 2D array representing the audio feature matrix (e.g., chroma, mel-spectrogram).
            sr (int, optional): _Defaults to 22050._
                The sampling rate of the audio signal. 
            y_axis (Literal['chroma', 'mel'], optional): _Defaults to None._
                The type of y-axis for the display. If 'chroma', the chroma axis will be used. 
                If 'mel', the Mel-frequency axis will be used. 
            show (bool, optional): _Defaults to False._
                If True, the original data, its dB-scaled version, and the max array will be displayed 
                using `librosa.display.specshow`. 
            frame_end (int, optional): _Defaults to 1000._
                The number of frames to display in the visualization. Only the first `frame_end` frames 
                will be shown if `show` is True. 

        Returns
        -------
            max_d (np.ndarray): 
                A 2D binary array of the same shape as `data`, where the maximum value in each column 
                is set to 1, and all other values are set to 0.
        """
        idx = np.argmax(data, axis=0)
        max_d = np.zeros(data.shape)
        max_d[idx, np.arange(data.shape[1])] = 1
        
        if show:
            D = cls.get_db(data)
            fig, ax = plt.subplots(3, 1, sharex=True)
            cls.show(data, frame_end=frame_end, title="original", y_axis=y_axis, ax=ax[0], show=False)
            cls.show(D, frame_end=frame_end, title="dB", y_axis=y_axis, ax=ax[1], show=False)
            cls.show(max_d, frame_end=frame_end, title="max", y_axis=y_axis, ax=ax[2], show=False)
            fig.tight_layout()
            plt.show()
                
        return max_d
    
    @classmethod
    def get_db(cls, data: np.ndarray):
        return librosa.amplitude_to_db(np.abs(data), ref=np.max)
    
    @classmethod
    def show(
        cls, 
        data: np.ndarray, 
        sr: Optional[int] = 22050, 
        title: Optional[str] = "",
        frame_end: Optional[int] = 1000, 
        y_axis: Optional[Literal["chroma", "mel"]] = None, 
        ax: Optional[Axes] = None,
        show: Optional[bool] = True
    ):
        """
        Display a visual representation of the provided audio feature data (such as Mel-spectrogram or Chroma).

        This method visualizes the given 2D audio feature array (e.g., Mel-spectrogram or Chroma) and allows
        customization of the axes, title, and plot display. It can display up to a certain number of frames
        specified by `frame_end`.

        Arguments
        -------
        data (np.ndarray): 
            The 2D array representing the audio feature data to display (e.g., Mel-spectrogram, Chroma).
            
        sr (Optional[int], optional): _Defaults to 22050._
            The sampling rate of the audio. 
            
        title (Optional[str], optional): _Defaults to \"\"._
            The title for the plot. 
            
        frame_end (Optional[int], optional): _Defaults to 1000._
            The number of frames to display from the data. 
        y_axis (Optional[Literal[\"chroma\", \"mel\"]], optional): _Defaults to None._
            The type of y-axis to display. Can be 'chroma' or 'mel'. 
        ax (Optional[axes.Axes], optional): _Defaults to None._
            An optional Matplotlib axes object on which to plot. If None, a new figure and axes will be created. 
        show (Optional[bool], optional): _Defaults to True._
            If True, the plot will be displayed immediately using `plt.show()`. If False, the plot will be created 
            but not shown. 
        """
        if ax is None:
            fig, ax = plt.subplots(1, 1, sharex=True)
        img = librosa.display.specshow(data[:, :frame_end], sr=sr, x_axis="time", y_axis=y_axis, ax=ax)
        plt.colorbar(img, ax=ax)
        ax.set(title=title)
        if show:
            plt.show()
    
    @classmethod
    def get_stats(cls, data: np.ndarray):
        data = data.astype(np.float64)
        return AudioFeatures(
            kurtosis = kurtosis(data, axis=1),
            max = np.max(data, axis=1),
            mean = np.mean(data, axis=1),
            median = np.median(data, axis=1),
            min = np.min(data, axis=1),
            skew = skew(data, axis=1),
            std = np.std(data, axis=1)
        )
        
    @classmethod
    def get_stats_2D(cls, data: np.ndarray):
        data = data.astype(np.float64)
        return AudioFeatures(
            kurtosis = kurtosis(data, axis=2),
            max = np.max(data, axis=2),
            mean = np.mean(data, axis=2),
            median = np.median(data, axis=2),
            min = np.min(data, axis=2),
            skew = skew(data, axis=2),
            std = np.std(data, axis=2)
        )
    
    
    
class FMA:
    def __init__(self):
        self.features = None
        self.echonest = None
        self.genres = None
        self.tracks = None
    
    def load(self, filepath: str):
        filename = os.path.basename(filepath)
        
        if 'features' in filename:
            self.features = pd.read_csv(filepath, index_col=0, header=[0, 1, 2])
            return self.features

        if 'echonest' in filename:
            self.echonest = pd.read_csv(filepath, index_col=0, header=[0, 1, 2])
            return self.echonest

        if 'genres' in filename:
            self.genres = pd.read_csv(filepath, index_col=0)
            return self.genres

        if 'tracks' in filename:
            tracks = pd.read_csv(filepath, index_col=0, header=[0, 1])
            
            # 將 csv 內的字串轉換為正確的資料型態
            COLUMNS = [('track', 'tags'), ('album', 'tags'), ('artist', 'tags'),
                    ('track', 'genres'), ('track', 'genres_all')]
            for column in COLUMNS:
                tracks[column] = tracks[column].map(ast.literal_eval)

            # 將 pd.table 內有關時間的欄位轉換為 datetime
            COLUMNS = [('track', 'date_created'), ('track', 'date_recorded'),
                    ('album', 'date_created'), ('album', 'date_released'),
                    ('artist', 'date_created'), ('artist', 'active_year_begin'),
                    ('artist', 'active_year_end')]
            for column in COLUMNS:
                tracks[column] = pd.to_datetime(tracks[column])

            
            SUBSETS = ('small', 'medium', 'large')
            tracks['set', 'subset'] = tracks['set', 'subset'].astype(
                        pd.CategoricalDtype(categories=SUBSETS, ordered=True))

            COLUMNS = [('track', 'genre_top'), ('track', 'license'),
                    ('album', 'type'), ('album', 'information'),
                    ('artist', 'bio')]
            for column in COLUMNS:
                tracks[column] = tracks[column].astype('category')

            self.tracks = tracks
            
            return self.tracks
    
    def train_data(self, size: Literal['small', 'medium'], feature: Literal['mfcc', 'chroma_cens']='mfcc'):
        size = self.tracks['set', 'subset'] <= size
        
        train = self.tracks['set', 'split'] == 'training'
        val = self.tracks['set', 'split'] == 'validation'
        test = self.tracks['set', 'split'] == 'test'

        X_train = self.features.loc[size & train, feature]
        X_val = self.features.loc[size & val, feature]
        X_test = self.features.loc[size & test, feature]

        Y_train = self.tracks.loc[size & train, ('track', 'genre_top')]
        Y_val = self.tracks.loc[size & val, ('track', 'genre_top')]
        Y_test = self.tracks.loc[size & test, ('track', 'genre_top')]
        
        return (X_train, Y_train), (X_val, Y_val), (X_test, Y_test)
    
    def top_genres(self, size=Literal['small', 'medium'], show=False):
        size = self.tracks['set', 'subset'] <= size
        top_genres = self.tracks.loc[size, ('track', 'genre_top')].unique()
        
        if show:
            print("Genres".ljust(20, " ") + " |  Count")
            print("-"*28)
            for tg in top_genres:
                count = len(self.tracks.loc[size & (self.tracks['track', 'genre_top'] == tg)])
                print(f"{tg.ljust(20, ' ')} | \t{count}")
        
        return top_genres

class CustomProgressBar(Callback):
    def __init__(self, total_epoch: int, name: str):
        self.total_epoch = total_epoch
        self.name = name
        self.count = 1
    
    def on_epoch_begin(self, epoch, logs=None):
        pass
    
    def on_epoch_end(self, epoch, logs=None):
        # 打印簡單的 epoch 進度條
        sys.stdout.write(f'\rEpoch {epoch+1}/{self.total_epoch} - loss: {logs["loss"]:.4f} - val_loss: {logs["val_loss"]:.4f}')
        
    def on_batch_begin(self, batch, logs=None):
        pass
    
    def on_batch_end(self, batch, logs=None):
        pass
    
    def on_train_begin(self, logs=None):
        sys.stdout.write(f'# {self.name}\n')
    
    def on_train_end(self, logs=None):
        pass

class TestModel:
    class ModelSettings:
        def __init__(self, epochs: int=50, batch_size: int=32):
            self.epochs = epochs
            self.batch_size = batch_size
            
            
    def __init__(self, func: Callable, settings: tuple[ModelSettings], name:str="Model"):
        self.model_func = func
        self.settings = settings
        self.name = name
        
    def _draw_loss(self, hist, fig: Figure=None, ax: Axes=None):
        if fig is None or ax is None:
            fig, ax = plt.subplots(1, 2, figsize=(12, 5))
            fig.suptitle('Loss Over Time', fontsize=20)
        
        ax[0].plot(hist.history['loss'], label='Training Loss')
        ax[0].set_xlabel('Epochs')
        ax[0].set_ylabel('Loss')
        ax[0].legend()

        ax[1].plot(hist.history['val_loss'], label='Validation Loss')
        ax[1].set_xlabel('Epochs')
        ax[1].set_ylabel('Loss')
        ax[1].legend()

        plt.tight_layout()
        
    def _show_loss(self, **kwargs):
        self._draw_loss(**kwargs)
        plt.show()
        
    def _draw_tsne(self, X_test, Y_test, encoder: Model, fig: Figure=None, ax: Axes=None, output_shape=20):
        if fig is None or ax is None:
            fig, ax = plt.subplots(1, 1)
            fig.suptitle('2D Visualization of Encoded Features', fontsize=20)
        
        ax.set_box_aspect(1) 
        encoded_features = encoder.predict(X_test)
        tsne = TSNE(n_components=2)
        encoded_2d = tsne.fit_transform(encoded_features.reshape(-1, output_shape))
        
        im = ax.scatter(encoded_2d[:, 0], encoded_2d[:, 1], c=Y_test, cmap='inferno', alpha=1)
        
        norm = Normalize(vmin=np.min(Y_test), vmax=np.max(Y_test))
        sm = ScalarMappable(norm=norm, cmap='inferno')
        sm.set_array([])
        
        fig.colorbar(sm, ax=ax)
        
    def _show_tsne(self, **kwargs):
        Y = kwargs.get("Y_test")
        kwargs["Y_test"] = self.encode_labels(Y)
        self._draw_tsne(**kwargs)
        plt.show()
    
    def encode_labels(self, Y):
        le = LabelEncoder()
        le.fit(Y)
        Y = le.transform(Y)
        return Y
    
    def test(self, x, y, val=None, validation_split=None, X_test=None, Y_test=None, name: str = "Model", output_shape=20):
        
        assert X_test is not None
        assert Y_test is not None
        assert val is not None or validation_split is not None
        
        count = len(self.settings)
        fig_loss, ax_loss = plt.subplots(count, 2, figsize=(6, 3*count))
        fig_tsne, ax_tsne = plt.subplots(1, count, figsize=(6*count, 6))
        
        for ax in ax_loss.flatten():
            ax.set_box_aspect(1)
            
        for ax in ax_tsne.flatten():
            ax.set_box_aspect(1)
            
            
        for i, setting in enumerate(self.settings):
            encoder, autoencoder = self.model_func()
            autoencoder.compile(optimizer='adam', loss='mse')
            if val is not None:
                hist = autoencoder.fit(
                    x, 
                    y, 
                    validation_data=val, 
                    epochs=setting.epochs, 
                    batch_size=setting.batch_size, 
                    verbose=0, 
                    callbacks=[
                        CustomProgressBar(
                            total_epoch=setting.epochs,
                            name = f"{name} - {i+1}"
                        )
                    ]
                )
            elif validation_split is not None:
                hist = autoencoder.fit(
                    x, 
                    y, 
                    validation_split=validation_split, 
                    epochs=setting.epochs, 
                    batch_size=setting.batch_size, 
                    verbose=0, 
                    callbacks=[
                        CustomProgressBar(
                            total_epoch=setting.epochs,
                            name = f"{name} - {i+1}"
                        )
                    ]
                )
            self._draw_loss(hist, fig=fig_loss, ax=ax_loss[i])
            self._draw_tsne(X_test, self.encode_labels(Y_test), encoder=encoder, fig=fig_tsne, ax=ax_tsne[i], output_shape=output_shape)
            
        fig_loss.suptitle('Loss Over Time', fontsize=20)
        fig_tsne.suptitle('2D Visualization of Encoded Features', fontsize=20)
        
        fig_loss.tight_layout()
        fig_tsne.tight_layout()
        plt.show()
            

def min_max_scaling(data: np.ndarray):
    s, b = min(data), max(data)
    return (data - s) / (b - s)