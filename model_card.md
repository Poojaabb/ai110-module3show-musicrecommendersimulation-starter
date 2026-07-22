# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**Seori 1.0**

---

## 2. Intended Use

Seori suggests songs that match what a listener says they like. The user tells it their favorite genre, the mood they want, the energy level they want, and whether they like acoustic music. Seori then picks the songs from its catalog that best fit those answers and shows the top 5, with a short reason for each pick.

It assumes the user knows what they want and can describe it up front, and it assumes the tags on each song (genre, mood, etc.) are correct. This is a **classroom project for learning**, not a real product. It should not be used for real music apps or real listeners.

**Not intended for:** real recommendation apps, making decisions about people, or any situation where a bad music pick could actually matter.

---

## 3. How the Model Works

Think of it like giving each song a score out of a few points and then sorting from highest to lowest.

For every song, Seori starts at 0 points and adds:

- **+2 points** if the song's genre is the user's favorite genre.
- **+1 point** if the song's mood matches the mood the user wants.
- **Up to +1 point** for energy, based on how close the song's energy is to the energy the user asked for. A perfect match gets close to a full point; a song that is way too calm or way too intense gets almost nothing.
- **+0.5 points** if the user likes acoustic music and the song is very acoustic.

After every song has a score, it sorts them and shows the top 5, plus the reasons that earned the points. I made genre worth the most on purpose, because getting the genre wrong usually ruins the recommendation, while moods like "chill" and "relaxed" are close enough that a mood miss is not as bad. The main change from the starter code was actually writing all of this scoring logic (the starter just returned the first few songs) and adding the acoustic bonus.

---

## 4. Data

The catalog has **18 songs**. Each song has an id, title, artist, genre, mood, and five number features: energy, tempo, valence (how positive it sounds), danceability, and acousticness. The numbers go from 0.0 to 1.0 (except tempo, which is in beats per minute).

I added 8 songs to the 10 that came with the starter, on purpose picking new genres and moods (hip-hop, classical, edm, country, r&b, metal, reggae, folk) to make it more varied. Even so, the dataset is tiny and unbalanced: lofi has 3 songs and pop has 2, but almost every other genre has only 1 song. Lots of real musical taste is missing — there is no k-pop, no metal subgenres, no world music, and no non-English music. So the system can only ever recommend from this small, uneven list.

---

## 5. Strengths

Seori works well when a user's taste is clear and lines up with a genre that has a few songs in the catalog. The **Chill Lofi** profile was the best example: it correctly pulled up quiet, acoustic study-type songs (Library Rain, Midnight Coding) and the scores made sense. The **High-Energy Pop** and **Deep Intense Rock** profiles also returned songs that felt right to me — upbeat pop for one, loud aggressive tracks for the other.

The scoring captures the "genre + mood + energy" idea well, and I think the biggest strength is that every recommendation comes with a **reason** ("genre match (+2.0), energy close (+0.98)"). Even when I disagreed with a pick, I could always see exactly why the system chose it, which made it easy to trust and easy to debug.

---

## 6. Limitations and Bias

The biggest weakness I found during my experiments is a **catalog imbalance that creates a filter bubble**. My dataset of 18 songs has 3 lofi songs and 2 pop songs, but every other genre (rock, metal, country, folk, classical, etc.) has only 1 song. Because a genre match is worth the most points (+2.0), users who like lofi or pop have several songs that can earn that big bonus, so they get rich, relevant top-5 lists. But a user who likes metal or country has only one song in the whole catalog that can ever earn the genre bonus, so the rest of their list gets filled by songs that only matched on energy — meaning fans of underrepresented genres get noticeably worse recommendations than fans of common ones.

A second, smaller bias comes from how I calculate the "energy gap." Since the energy score is just `1 - |song energy - target energy|`, a user with a middle-of-the-road target (like 0.5) ends up scoring fairly close to almost every song, so their energy signal is weak and their list looks muddy. Meanwhile a user with an extreme target (like 0.95) gets much sharper separation between songs. The system also uses exact genre matching, so "indie pop" never counts as a match for a "pop" fan even though they are basically the same, which blocks reasonable cross-genre discovery.

---

## 7. Evaluation

### Profiles I tested

I tested five user profiles: three normal ones — **High-Energy Pop** (pop / happy / 0.9), **Chill Lofi** (lofi / chill / 0.35, likes acoustic), and **Deep Intense Rock** (rock / intense / 0.95) — and two adversarial edge cases — **Loud but Sad** (classical / melancholy / 0.95) and **Unknown Genre** (reggaeton / happy / 0.5). For each one I looked at the top 5 songs and checked whether they made sense for that kind of listener.

### What surprised me

The most surprising result was the **Loud but Sad** profile. This user asked for very high energy (0.95) but also a sad mood and a genre (classical) that is almost always quiet. The system still put "Snowfall Sonata," a soft classical song with energy 0.22, at the top — the exact opposite of the loud song the user asked for. That surprised me and showed that matching genre and mood can completely overpower the energy request. I was also surprised that the **Unknown Genre** profile didn't break anything; since no song is tagged "reggaeton," the system just quietly ranked on mood and energy instead.

### Comparing pairs of profiles

- **High-Energy Pop vs. Chill Lofi:** The pop profile pulled up bright, fast, upbeat songs (Sunrise City, Gym Hero), while the lofi profile shifted all the way to slow, quiet, acoustic songs (Library Rain, Midnight Coding). This makes sense because the two profiles ask for opposite energy levels and opposite genres, so almost none of the same songs appear in both lists.
- **Deep Intense Rock vs. Chill Lofi:** The rock profile favored loud, aggressive tracks (Storm Runner, Iron Verdict) and the lofi profile favored calm study-type music. This is the clearest "opposite ends" pair, and the recommendations correctly went in opposite directions.
- **High-Energy Pop vs. Deep Intense Rock:** These two overlap because both want high energy, so a couple of songs (like Gym Hero and Storm Runner) show up on both lists. The difference is the genre bonus: Gym Hero wins for the pop fan and Storm Runner wins for the rock fan, which is exactly what should happen.
- **Normal profiles vs. the "Loud but Sad" edge case:** For the normal profiles, the #1 song matched on genre, mood, AND energy, so it won by a big margin. For the edge case, the #1 song only matched genre and mood while badly missing energy, so its lead was much smaller — a sign the system is being "tricked" by conflicting preferences.

### Plain-language explanation (for a non-programmer)

Someone might ask: "I just want happy pop — why does the gym workout song 'Gym Hero' keep showing up near the top?" The reason is that my system gives the most points for matching the **genre** (pop) and for having an **energy level** close to what the listener asked for. "Gym Hero" is tagged as pop and is very high energy, so it scores well on two of the three things I measure — even though its mood is "intense," not "happy." My system doesn't understand that a happy person at a coffee shop probably doesn't want a hard workout song; it only sees that the genre and energy line up, so it keeps recommending it.

---

## 8. Future Work (Ideas for Improvement)

If I kept developing Seori, here are three things I would change:

1. **Balance and grow the dataset.** Right now most genres only have one song, which creates a filter bubble. I would add many more songs so every genre has a fair number of options.
2. **Let users pick more than one favorite.** A person could like "rock AND metal" or "happy OR energetic." Allowing a list of favorites, and using near-matches (so "indie pop" counts partly for a "pop" fan), would handle real, mixed taste much better.
3. **Add diversity to the top results.** I would stop the list from showing three nearly identical songs, and maybe let the user set how much energy should matter versus genre, so conflicting profiles (like "loud but sad") don't get tricked as easily.

---

## 9. Personal Reflection

**Biggest learning moment:** I learned that a recommendation is really just a **score plus a sort**. Once I saw that "recommending" is only ranking songs by points, the whole idea stopped feeling like magic. Watching the "Loud but Sad" profile still return a quiet song taught me that the *weights* I choose quietly decide what the system thinks is important, even when it produces a result that feels wrong.

**How AI tools helped, and when I double-checked:** Using an AI coding assistant helped me move fast — brainstorming the scoring recipe, writing the CSV loader, and formatting the terminal output. But I made sure to stay in control of the actual logic. I double-checked the point values, ran the tests, and verified the output by hand for the pop/happy profile before trusting it. When I ran the weight experiment, I checked that the math still made sense instead of just believing the numbers.

**What surprised me:** I was surprised that such a simple algorithm — just adding up a few points — could still "feel" like a real recommendation with reasons attached. It changed how I think about music apps: the big ones are far more advanced, but at the core they are still just scoring and ranking, and their weights and data can create the same kinds of biases I saw in my tiny version.

**What I'd try next:** I'd add more songs, let users express mixed taste, and experiment with using the extra features I already have (valence and danceability) so the recommendations capture more than just genre, mood, and energy.
