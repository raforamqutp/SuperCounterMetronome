# Super Counter Metronome

Welcome to the **Super Counter Metronome**!
This is a silly little personal project I made to help myself land Super Counters more consistently in a fighting game called *Sparking Zero*. If you're into frame data, reaction windows, and the pain of trying to counter in a 60 FPS environment (with or without lag), this might help you out too.

It's not a polished product, not even indie-dev-tier — just something I threw together a while ago and decided to share. Use it, tweak it, ignore it... totally up to you.

## What Does It Do?

This tool simulates a 60 FPS metronome loop, showing and playing cues during **two specific Super Counter windows**:

* **First window:** Frames 21–28
* **Second window:** Frames 42–49

The idea is that you’ll hear audio cues (and see visual zones) that mimic the timing of when to input your Super Counter. The first cue is a bait — you're supposed to fail that one. The second one is your chance to actually land it.

You can just listen to the audio if you're multitasking — it works fine in the background. Practice muscle memory with the timing, and you'll (maybe) start hitting those counters more consistently. Maybe.

## How It Works

* Frame loop = 60 frames = 1 second.
* Sound plays at frame **21** and again at frame **45**.

  * First sound: intentionally misleading, since the opponent has to hit you too.
  * Second sound: this is your window to hit the Super Counter.
* You can press slightly **before**, **on**, or **after** the second cue and still succeed, assuming you're within that 7-frame window (42–49).
* Works best in a stable environment. If your game’s running at 30 FPS or your internet is held together with duct tape and hope, results may vary.

## Custom Colors

There’s a quick-and-dirty menu that lets you change the colors of the background, bars, and counter zones. It's... not great. I slapped it on at the end and the text inputs are held together with string and duct tape. But hey, if you want to tweak the colors — go wild.

## 🔊 Sound Volume

There’s a slider at the bottom for adjusting the volume of the cue sounds. Handy if you don’t want your speakers exploding every second.

## 🛠️ Requirements (if you plan on modifying it)

* Python 3
* `pygame`
* `pyperclip` (for copy-pasting color codes)

You can install the dependencies with:

```bash
pip install pygame pyperclip
```

## Running It

The releases page has the exe file which you can try on windows, there is no mac support as I don't have a mac and also who plays on a mac.

or alternatively you can just run the Python script:

```bash
python super_counter_metronome.py
```


It'll show an intro screen, let you mess with colors if you want, and then start the metronome.

## ❗ Heads Up

* I *might* be wrong about some frame data or how Super Counters technically activate. This is based on my testing and gameplay feel. Plus the game already had some updates so it might have changed how all this works, haven't played in a while.
* It’s most helpful when you’re practicing in an offline or lag-free environment. Online chaos may still eat your inputs alive.
* This was made for fun. Don’t expect polish, but feel free to fork, hack, or improve it.

## Final Words

If it helps, awesome! If not, well… it was free.
And hey, maybe one day your Super Counters will be **over 9000**. (did you see what I did there? ( ͡° ͜ʖ ͡°) )

Signed,
**Mandarina Studios** (totally made-up)
Good luck out there!