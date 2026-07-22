# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.



---

I think apps like Spotify or Youtube Music learn from repeated plays of a certain genre/artists and some may even track what your play at certain time periods in the day or if youtube music has access to google's data, even your location when playing certain music. I think i want my version will try to go off of the user's direct input and answers to certain preference questions at the opening of the recommender. It just compares what they stated they like with the song description.



Song will store title, artist, genre, mood, energy, tempo_bpm, danceability, acousticness, valence and an id and i think each user profile just needs their favorite genre, their main mood they're looking for, their energy and likes_acoustic.

My algorthm recipe is for each song my recommender starts the score at 0 and then adds points based on these rules:

- +2.0 if the song's genre matches the user's favorite genre
- +1.0 if the song's mood matches the user's mood
- +1.0 times (1 - the difference between the song's energy and the user's target energy), so a song gets close to a full point if its energy is almost the same as what the user wants, and close to 0 if it's really far off
- +0.5 if the user likes acoustic songs and the song's acousticness is 0.6 or higher

After every song has a score, I sort them from highest to lowest and return the top K songs, along with a short reason showing which rules gave them points. I made genre worth twice as much as mood because getting the genre wrong usually ruins the recommendation, while moods like chill and relaxed are pretty close to each other anyway.

some biases i expect are

- Because genre is worth +2.0, my system might over-prioritize genre and skip a song that perfectly matches the user's mood and energy just because the genre label is different. For example someone who likes "intense rock" might never get a great metal song even though it's basically what they want.
- The user profile is kind of narrow since they can only pick one favorite genre and one mood, so someone with mixed taste won't be served very well.
- The scoring completely depends on the tags in the CSV, so if a song is labeled wrong it will score wrong, and there's no sense of how good or popular a song actually is.

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
Loaded songs: 18
User profile: genre=pop, mood=happy, energy=0.8

Top recommendations:

1. Sunrise City by Neon Echo - Score: 3.98
   Because: genre match (+2.0), mood match (+1.0), energy close (+0.98)

2. Gym Hero by Max Pulse - Score: 2.87
   Because: genre match (+2.0), energy close (+0.87)

3. Rooftop Lights by Indigo Parade - Score: 1.96
   Because: mood match (+1.0), energy close (+0.96)

4. Concrete Sunrise by Blocktape - Score: 0.98
   Because: energy close (+0.98)

5. Night Drive Loop by Neon Echo - Score: 0.95
   Because: energy close (+0.95)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



