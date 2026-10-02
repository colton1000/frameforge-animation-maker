# FrameForge Animation Maker

Welcome to **FrameForge**, a fun animation maker that runs directly in your web browser!

No complicated setup or installation is required. Simply download the latest HTML file, open it in your browser, and start creating animations.

For quick access to the latest build, examples, and sample projects, open the [FrameForge index](index.html).

## Features

Depending on the version you use, FrameForge includes features such as:

- Smooth drawing
- Multiple drawing tools and paint brushes
- Adjustable brush opacity
- Custom background uploads
- Frame-by-frame animation
-  Animation project saving and loading
- MP4 animation exporting
- Custom canvas themes
- 3D animation tools
- Dedicated animation playback
- And much more!

##  Getting Started

Choose the full browser app or the compact Firefox extension:

- For the full editor, open the [latest HTML build](versions/latest/frameforge_update_NEW_v4_credits_hints.html) in a modern browser.
- For a smaller toolbar-based drawing and animation app, install [FrameForge: On the GO!](frameforge_on_the_go_v2_2_fixed_colors/).

## FrameForge: On the GO!

**FrameForge: On the GO!** is a rebuilt, compact 2D version of FrameForge packaged as a Firefox browser extension. It opens from the Firefox toolbar as a popup, so you can sketch and animate without opening the full-size editor. The extension requires Firefox 109 or newer.

### Install in Firefox

This repository contains the extension source for local testing; it is not currently linked to a signed Mozilla Add-ons listing. To load it temporarily:

1. Download or clone this repository to your computer.
2. In Firefox, open `about:debugging#/runtime/this-firefox`.
3. Choose **This Firefox**, then **Load Temporary Add-on…**.
4. Select `manifest.json` inside the [extension folder](frameforge_on_the_go_v2_2_fixed_colors/manifest.json).
5. Use the FrameForge icon in the Firefox toolbar to open the extension.

Temporary add-ons are removed when Firefox restarts. Repeat these steps to load it again. For a regular installation, use a signed release from Mozilla Add-ons when one is available.

### Draw and animate

- Pick Pencil, Marker, or Eraser, then adjust brush size, opacity, and color.
- Draw on the canvas; use Undo, Redo, Clear Frame, and onion skin while working.
- Add blank frames or duplicate existing frames, then use playback controls and FPS to preview the animation.
- Rename the project as you work. The extension automatically saves the current project in the browser's local storage for the extension.
- Use **Export Project** to download a `.json` backup, or **Import Project** to open a project exported by the extension.

The extension is intentionally compact and focused on 2D frame animation. Use the [full FrameForge editor](versions/latest/frameforge_update_NEW_v4_credits_hints.html) for its broader feature set, including 3D tools and the larger workspace.

You can improve one of the included animation projects or create something completely new. Have fun experimenting!

##  Animation Project Files

FrameForge uses `.json` files to save animation projects.

These files may contain information such as:

- Frames
- Drawings
- Colors
- Brush settings
- Opacity
- Backgrounds
- Animation settings

To continue editing a project, click the **Load** button inside FrameForge and select the appropriate `.json` file.

> [!IMPORTANT]
> Any JSON file with **`FOR PLAYBACK`** in its name is intended only for use with `playback_fixed2.html`. It may not load correctly inside the animation editor.

## Repository Layout

The project is organized into easy-to-navigate folders:

- [examples](examples): feature demos and older browser prototypes
- [versions/latest](versions/latest): newest release builds
- [versions/archive](versions/archive): earlier version snapshots
- [addons/animation-creator](addons/animation-creator): optional add-ons and extra tools
- [projects](projects): saved animation project files
- [scripts/utility-scripts](scripts/utility-scripts): utility scripts and organizer helpers

## Latest Version

The newest version is:

###  FrameForge_update_NEW_v4

You can now download **FrameForge_update_NEW_v4**, the latest major version of the animation maker!

FrameForge has grown from a simple browser animation tool into a more advanced creative environment with improved drawing, themes, exporting, backgrounds, and 3D features.
### [Open the newest version](versions/latest/frameforge_update_NEW_v4_credits_hints.html)

An alternate [online-enabled build](versions/latest/frameforge_online.html) is also available in the latest versions folder.

## Previous Versions

Earlier versions added important features and may still be available in the repository.

### [animation_creator_canvas_ui_themes.html](examples/animation_creator_canvas_ui_themes.html)

This version introduced:

- A redesigned canvas interface
- Custom themes
- Additional animation tools
- General improvements and bug fixes

### [animation_creator_smooth_opacity_background.html](examples/animation_creator_smooth_opacity_background.html)

This update introduced:

- Smoother drawing
- Brush opacity controls
- Background image uploads
- Improved drawing behavior

### Other Updates

Additional updates introduced:

- New paint brushes
- MP4 animation exporting
- Improved project loading
- Bug fixes
- More creative tools
- Interface improvements
- Additional fun features

For the newest features and fixes, use the latest available FrameForge version.

## Browser Compatibility

The standalone HTML builds should work in most modern browsers, including:

- Google Chrome
- Microsoft Edge
- Mozilla Firefox
- Opera
- Brave

For the best experience, use an updated browser.

**FrameForge: On the GO!** is a Firefox extension and requires Firefox 109 or newer.

## Repository

Download FrameForge, explore the available versions, and find example animation files here:

### [Open the FrameForge Animation Maker Repository](https://github.com/colton1000/frameforge-animation-maker/tree/main)

## Tips

- Save your animation regularly.
- Keep backup copies of important `.json` project files.
- Use clear filenames so you can easily identify your projects.
- Make sure you use playback-only files with the correct playback HTML.
- Try different brushes, opacity levels, backgrounds, themes, and animation styles.
- Use the latest version for the newest features and bug fixes.

## Thank You!

Thank you for checking out **FrameForge Animation Maker**!

Create your own animations, experiment with the tools, and most importantly, have fun bringing your ideas to life!
