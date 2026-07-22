import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _prefs_from_user(self, user: UserProfile) -> Dict:
        """Convert a UserProfile into the dict shape score_song() expects."""
        return {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }

    def _song_to_dict(self, song: Song) -> Dict:
        """Pull just the fields the scorer needs out of a Song object."""
        return {
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
            "acousticness": song.acousticness,
        }

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Score every song for this user and return the top k as Song objects."""
        scored = []
        prefs = self._prefs_from_user(user)
        for song in self.songs:
            score, _reasons = score_song(prefs, self._song_to_dict(song))
            scored.append((song, score))
        scored.sort(key=lambda pair: pair[1], reverse=True)
        return [song for song, _score in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable string of why a song matched this user."""
        prefs = self._prefs_from_user(user)
        score, reasons = score_song(prefs, self._song_to_dict(song))
        if not reasons:
            return f"{song.title} scored {score:.2f} with no strong matches."
        return f"{song.title} scored {score:.2f}: " + ", ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Read the songs CSV into a list of dicts, converting numeric columns to numbers."""
    float_fields = {"energy", "valence", "danceability", "acousticness"}
    int_fields = {"id", "tempo_bpm"}
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in float_fields:
                if field in row and row[field] != "":
                    row[field] = float(row[field])
            for field in int_fields:
                if field in row and row[field] != "":
                    row[field] = int(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user prefs; return (score, list of reason strings)."""
    score = 0.0
    reasons: List[str] = []

    # +2.0 for a genre match
    if user_prefs.get("genre") and song.get("genre") == user_prefs["genre"]:
        score += 2.0
        reasons.append("genre match (+2.0)")

    # +1.0 for a mood match
    if user_prefs.get("mood") and song.get("mood") == user_prefs["mood"]:
        score += 1.0
        reasons.append("mood match (+1.0)")

    # up to +1.0 for how close the energy is to the target
    target_energy = user_prefs.get("energy")
    if target_energy is not None and song.get("energy") is not None:
        closeness = 1.0 - abs(song["energy"] - target_energy)
        closeness = max(0.0, closeness)  # never go negative
        points = round(closeness, 2)
        score += points
        reasons.append(f"energy close (+{points:.2f})")

    # +0.5 acoustic bonus, only if the user opted in
    if user_prefs.get("likes_acoustic") and song.get("acousticness", 0) >= 0.6:
        score += 0.5
        reasons.append("acoustic bonus (+0.5)")

    return round(score, 2), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score and rank all songs, returning the top k as (song, score, explanation)."""
    scored: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons) if reasons else "no strong matches"
        scored.append((song, score, explanation))
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
