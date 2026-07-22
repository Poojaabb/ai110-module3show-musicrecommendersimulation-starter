"""
Command line runner for the Music Recommender Simulation.

Runs the recommender against several user profiles (three normal ones
plus two adversarial / edge-case ones) so we can stress test the scoring.
"""

# Works both as `python -m src.main` (from the project root) and `python main.py` (from src/).
try:
    from src.recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs


# --- Three distinct "normal" user profiles ---
NORMAL_PROFILES = [
    ("High-Energy Pop", {"genre": "pop", "mood": "happy", "energy": 0.9}),
    ("Chill Lofi", {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True}),
    ("Deep Intense Rock", {"genre": "rock", "mood": "intense", "energy": 0.95}),
]

# --- Adversarial / edge-case profiles: designed to try to "trick" the scoring ---
EDGE_PROFILES = [
    # Conflicting: wants very HIGH energy but a SAD, usually-quiet mood + genre.
    ("Edge: Loud but Sad", {"genre": "classical", "mood": "melancholy", "energy": 0.95}),
    # A genre that does NOT exist anywhere in the catalog.
    ("Edge: Unknown Genre", {"genre": "reggaeton", "mood": "happy", "energy": 0.5}),
]

ALL_PROFILES = NORMAL_PROFILES + EDGE_PROFILES


def run_profile(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print the top k recommendations for a single named profile."""
    prefs_text = ", ".join(f"{key}={value}" for key, value in user_prefs.items())
    print("=" * 60)
    print(f"Profile: {name}")
    print(f"Preferences: {prefs_text}")
    print("-" * 60)

    recommendations = recommend_songs(user_prefs, songs, k=k)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} by {song['artist']} - Score: {score:.2f}")
        print(f"   Because: {explanation}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    for name, user_prefs in ALL_PROFILES:
        run_profile(name, user_prefs, songs, k=5)


if __name__ == "__main__":
    main()
