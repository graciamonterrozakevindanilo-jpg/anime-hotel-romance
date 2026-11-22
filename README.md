# Anime Hotel Romance — 90s Anime Animatic

This repository prepares a 15-second, 16:9 MP4 animatic from the character-sheet and hotel-background reference images.

## Important limitation
GitHub Actions can run rendering code, but GitHub itself is not an AI video-generation model. This starter workflow creates a camera-motion animatic from still images; it does **not** generate new poses, walking cycles, facial animation, or true hand-drawn cel animation. A fully animated version requires an image-to-video model/API.

## Add the reference images
Upload these exact files into the `assets/` folder:
- `man.png` — man's character sheet
- `hotel.png` — hotel hallway background
- `woman.png` — woman's character sheet

Images attached in ChatGPT are not automatically copied into GitHub.

## Run
1. Add the three images above.
2. Open **Actions → Build 15s animatic → Run workflow**.
3. Download the `anime-hotel-romance-mp4` artifact from the completed run.

## Planned scene
Both adult characters leave separate rooms in the hotel corridor, meet face-to-face, hold eye contact for a couple of seconds, blush, and shyly look away.

## Art direction
Japanese 1990s-inspired 2D anime, traditional cel-shading, hand-inked outlines, warm hotel lighting. Preserve the character designs, faces, hairstyles, proportions, and exact sleepwear from the supplied references.
