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

I stress-tested the recommender with three normal profiles and two adversarial "edge case" profiles. Here is the terminal output for each:

**Three normal profiles:**

```
============================================================
Profile: High-Energy Pop
Preferences: genre=pop, mood=happy, energy=0.9
------------------------------------------------------------
1. Sunrise City by Neon Echo - Score: 3.92
   Because: genre match (+2.0), mood match (+1.0), energy close (+0.92)
2. Gym Hero by Max Pulse - Score: 2.97
   Because: genre match (+2.0), energy close (+0.97)
3. Rooftop Lights by Indigo Parade - Score: 1.86
   Because: mood match (+1.0), energy close (+0.86)
4. Storm Runner by Voltline - Score: 0.99
   Because: energy close (+0.99)
5. Pulse Horizon by Voltaic - Score: 0.95
   Because: energy close (+0.95)

============================================================
Profile: Chill Lofi
Preferences: genre=lofi, mood=chill, energy=0.35, likes_acoustic=True
------------------------------------------------------------
1. Library Rain by Paper Lanterns - Score: 4.50
   Because: genre match (+2.0), mood match (+1.0), energy close (+1.00), acoustic bonus (+0.5)
2. Midnight Coding by LoRoom - Score: 4.43
   Because: genre match (+2.0), mood match (+1.0), energy close (+0.93), acoustic bonus (+0.5)
3. Focus Flow by LoRoom - Score: 3.45
   Because: genre match (+2.0), energy close (+0.95), acoustic bonus (+0.5)
4. Spacewalk Thoughts by Orbit Bloom - Score: 2.43
   Because: mood match (+1.0), energy close (+0.93), acoustic bonus (+0.5)
5. Coffee Shop Stories by Slow Stereo - Score: 1.48
   Because: energy close (+0.98), acoustic bonus (+0.5)

============================================================
Profile: Deep Intense Rock
Preferences: genre=rock, mood=intense, energy=0.95
------------------------------------------------------------
1. Storm Runner by Voltline - Score: 3.96
   Because: genre match (+2.0), mood match (+1.0), energy close (+0.96)
2. Gym Hero by Max Pulse - Score: 1.98
   Because: mood match (+1.0), energy close (+0.98)
3. Pulse Horizon by Voltaic - Score: 1.00
   Because: energy close (+1.00)
4. Iron Verdict by Ashfall - Score: 0.97
   Because: energy close (+0.97)
5. Sunrise City by Neon Echo - Score: 0.87
   Because: energy close (+0.87)
```

**Two adversarial / edge-case profiles:**

```
============================================================
Profile: Edge: Loud but Sad
Preferences: genre=classical, mood=melancholy, energy=0.95
------------------------------------------------------------
1. Snowfall Sonata by Aria Winters - Score: 3.27
   Because: genre match (+2.0), mood match (+1.0), energy close (+0.27)
2. Pulse Horizon by Voltaic - Score: 1.00
   Because: energy close (+1.00)
3. Gym Hero by Max Pulse - Score: 0.98
   Because: energy close (+0.98)
4. Iron Verdict by Ashfall - Score: 0.97
   Because: energy close (+0.97)
5. Storm Runner by Voltline - Score: 0.96
   Because: energy close (+0.96)

============================================================
Profile: Edge: Unknown Genre
Preferences: genre=reggaeton, mood=happy, energy=0.5
------------------------------------------------------------
1. Rooftop Lights by Indigo Parade - Score: 1.74
   Because: mood match (+1.0), energy close (+0.74)
2. Sunrise City by Neon Echo - Score: 1.68
   Because: mood match (+1.0), energy close (+0.68)
3. Velvet Hours by Sable Rose - Score: 0.98
   Because: energy close (+0.98)
4. Island Time by Palm Riddim - Score: 0.98
   Because: energy close (+0.98)
5. Backroad Memory by Dusty Miles - Score: 0.95
   Because: energy close (+0.95)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

### Weight Shift: doubled energy, halved genre

For my experiment I changed `score_song` so that a genre match was worth +1.0 instead of +2.0 (halved), and the energy score was multiplied by 2.0 instead of 1.0 (doubled). I then re-ran all five profiles and compared them to the original recipe. Afterward I reverted the weights back to the original values.

What I noticed:

- **For the three normal profiles, the top song barely changed.** Sunrise City still won High-Energy Pop, Library Rain still won Chill Lofi, and Storm Runner still won Deep Intense Rock, because those songs already match on genre, mood, AND energy. The scores changed but the *order* mostly did not.
- **The lower ranks got shuffled.** Songs that only matched on energy (like Storm Runner and Pulse Horizon in the pop list) climbed up because energy was now worth up to +2.0 instead of +1.0.
- **The biggest change was in the "Loud but Sad" edge case.** With the original weights, Snowfall Sonata beat the runner-up by a wide margin (3.27 vs 1.00). With the experiment, that gap shrank to almost nothing (2.54 vs 2.00), because rewarding energy so heavily nearly let a loud song overtake the song that actually matched the user's genre and mood.

**My takeaway:** the change made the results *different*, not clearly *more accurate*. Boosting energy made the system pay more attention to "how energetic" and less to "what kind of music," which is the opposite of what I decided mattered most in my design, so I kept the original weights (genre 2.0, mood 1.0, energy up to 1.0).

Other experiment ideas I could still try:

- What happened when I added tempo or valence to the score
- How the system behaves for even more unusual user profiles

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



