# Gnomies

Gnomies is a specialized CLI utility designed for agentic workflows (like Hermes) that need to "see" the screen. It allows you to search for open windows by title, focus them, and trigger a screenshot, saving the result to a predictable file path.

## Why Gnomies?

On modern GNOME/Wayland systems, screen capture is gated by security portals. Gnomies bridges the gap by:

- **Searching**: Querying active window titles via GNOME D-Bus
- **Focusing**: Bringing the target window to the foreground
- **Capturing**: Using the XDG Portal / `gnome-screenshot` to grab the window without user interaction
- **Predictability**: Moving the capture to a static path for your AI to ingest

## Prerequisites

### Window Calls Extension
Ensure the **Window Calls** GNOME extension is installed and enabled.

### System Dependencies

```bash
sudo apt install gnome-screenshot
```

## Usage

Run the script with a keyword to search for a window title:

```bash
python3 capture.py "Browser"
```

The script will:

1. Find the first window matching "Browser"
2. Focus that window
3. Save the result to `/tmp/hermes_output/hermes_capture.png`

## Hermes Skill Prompt

**Say this to Hermes:**

> "Clone https://github.com/ryanraposo/gnomies to a sensible location and create a skill for the screenshot capture utility."

This will result in Hermes cloning the repo and creating a skill for visual capabilities:

> **Skill:** Screenshot_Tool
>
> **Purpose:** Use this tool when you need to visually analyze an active window to extract information, debug, or verify status.
>
> **Mechanism:** This tool executes `python3 <cloned-repo-path>/capture.py [KEYWORD]`.
>
> **Behavior:**
> 1. Identify the application or window title relevant to the current task.
> 2. Call the tool with the appropriate keyword.
> 3. Once the tool confirms capture, read the image file from `/tmp/hermes_output/hermes_capture.png`.
> 4. Perform visual analysis (OCR or Vision model) on that file.
>
> **Example:** *"I need to check the build status in VSCode."*
> → Call `capture.py "VSCode"` → Analyze result.

## License

MIT