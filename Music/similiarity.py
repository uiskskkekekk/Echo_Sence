from Music.models import Music
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class MusicSimilarityComparator:
    def compare(self, target_id: str):
        target_music = Music.objects.filter(music_id=target_id).values().first()
        musics = Music.objects.exclude(music_id=target_id).values()

        print(target_music, musics)

        similarities = []
        target_features = np.array(target_music.get("features"), dtype=np.float32).reshape(1, -1)

        for music in musics:
            features = np.array(music.get("features"), dtype=np.float32).reshape(1, -1)
            similarity = cosine_similarity(target_features, features)[0][0]
            similarities.append((music, similarity))

        top_10_similar = sorted(similarities, key=lambda x: x[1], reverse=True)[:10]

        return [music for music, _ in top_10_similar]