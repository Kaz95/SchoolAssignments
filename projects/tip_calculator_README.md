# Tip Calculator

A terminal-based tip calculator, written for a class assignment that
requires the entire submission to be a single .py file using nothing
outside the Python standard library.

## Demo
[![Panera Bread Tip Calculator](https://img.youtube.com/vi/mIr1zzVvDFA/0.jpg)](https://www.youtube.com/watch?v=mIr1zzVvDFA)

## What it does

On launch, it fetches a small bitmap image and a short sound effect from
this repo over HTTP, then:

1. Plays a fade-in/fade-out intro animation of the bitmap directly in the
   terminal, using true-color ANSI escape codes and linear interpolation
   between colors for the fade.
2. Draws a bordered calculator UI for entering a bill amount, choosing or
   entering a tip, and viewing the total.
3. Plays a short sound effect when the calculator is reset, reconstructed
   at runtime from raw audio bytes rather than a bundled sound file.

## Why it looks the way it does

The single-file, standard-library-only constraint is the reason for most
of the less obvious choices here:

- The bitmap and the sound effect are not stored in the file. They're
  hosted in this repo's `assets/generated/` folder and pulled in with
  `urllib.request` at runtime, which is how a single file ends up
  displaying an image and playing audio without bundling either as binary
  data.
- The sound effect is stored as raw PCM bytes rather than a `.wav` file
  (see `toolkit/audio.py` for the extraction step). At runtime, a valid
  WAV container is rebuilt around those bytes in memory with the `wave`
  module before handing it to `winsound`, since the file itself is only
  the raw frame data, not a real WAV.
- Audio plays on a background thread so it doesn't block the calculator
  loop while the sound finishes.
- The bitmap font used to render "PANERA BREAD" in the intro is a small
  hand-built set of 4-bit sprites (`CHARACTER_SPRITES`), drawn using
  Unicode half-block characters to get two rows of resolution per
  terminal cell.
- `EmojiUnicodes` uses a metaclass to lazily decode `\u`-style emoji
  escape sequences on attribute access, since Python won't resolve a
  dynamically built escape sequence into unicode automatically at
  runtime the way it does with a literal.

## Current status

Everything above currently lives inline in `tip_calc.py` itself, including
code that also exists in a more general form under `toolkit/` (the
bordered box drawing, the animation loop, the audio playback). That
duplication is intentional for now, since the class requires a flat
single-file submission and there's no build step yet that assembles one
automatically from the shared modules.

`draw_window` is also still tip-calculator-specific: it draws the exact
layout for this assignment (bill, tip options, total) rather than a
general-purpose box. The plan is to reduce it to a generic bordered box
primitive in `toolkit/canvas.py`, with the tip calculator's specific
layout built on top of that at the project level instead of living inside
the shared drawing code.

## Requirements

- Python 3.7 or later. The file uses `from __future__ import annotations` so
  the `str | int` union type syntax doesn't require 3.10 at runtime.
- Windows only, due to the use of `winsound` for audio playback.
- No third-party packages required to run the submitted file.

## Known limitation

The animation loop redraws every pixel of every frame and sends a new ANSI color code for each, which is fine running 
locally but noticeably slow in constrained or networked environments (for example, some online Python sandboxes). 
A more efficient version would avoid emitting a new ANSI color code for each pixel when consecutive pixels in a row 
share the same color.
