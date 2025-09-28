# Productivity Script

A friendly Python CLI tool built with Typer that helps you maintain focused study sessions by blocking distractions, timing sessions, and logging reflections.

## Features

- **🎯 Interactive Study Mode**: Friendly prompts with rich console output
- **⏱️ Preparation Timer**: 2-minute countdown to help you get into the zone
- **🚫 Website Blocking**: Automatically blocks distracting sites during study sessions
- **📊 Visual Progress**: Beautiful progress bars and timers using Rich
- **📝 Reflection Logging**: Guided post-session questions saved to organized files
- **📁 Subject Organization**: Creates folders and files organized by study subject
- **🔗 Google Tasks Integration**: View your Google Tasks (optional)

## How It Works

1. **Pre-Session**: Interactive prompts ask what subject you're studying, focus area, and session duration
2. **Prep Time**: 2-minute timer with progress bar to prepare and eliminate distractions
3. **Study Session**: Blocks configured websites and runs your timed study session with visual countdown
4. **Reflection**: Guided post-session questions with friendly prompts, saved to organized files
5. **Cleanup**: Automatically unblocks websites when session ends

## Requirements

- **Linux only** (uses `/etc/hosts` file modification)
- Python 3.7+
- `sudo` privileges (required for website blocking)
- `mpv` (optional, for notification sounds)

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Make the bash script executable:
   ```bash
   chmod +x sitesManager.sh
   ```

## Usage

The tool now uses a friendly CLI interface with commands:

### Start a Study Session
```bash
python3 index.py study
```

### View Google Tasks
```bash
python3 index.py tasks
```

### Get Help
```bash
python3 index.py --help
```

### Study Mode Features
When you run the study command, the tool will:
- Ask you what subject you want to focus on
- Ask what specifically you'll work on  
- Ask how long your session should last (in minutes)
- Provide a beautiful preparation timer
- Show progress during your study session
- Guide you through reflection questions

### File Organization

Study reflections are automatically saved to:
```
~/Desktop/study/[subject]/reflection-YYYY-MM-DD.txt
```

## Website Blocking

Currently blocks:
- youtube.com
- www.youtube.com

### How Blocking Works

The tool temporarily modifies your `/etc/hosts` file to redirect blocked sites to `127.0.0.1` (localhost). This is:
- **Temporary**: Sites are unblocked when the session ends
- **Safe**: Only adds/removes specific entries
- **Effective**: Works system-wide for all browsers and applications

### Safety Notes

⚠️ **Important**: This tool requires `sudo` access to modify `/etc/hosts`

- The script only modifies entries for specified websites
- Sites are automatically unblocked when the session ends
- If the script is interrupted, you may need to manually remove blocked entries from `/etc/hosts`

### Manual Unblock (Emergency)

If sites remain blocked after an interrupted session:

1. Open `/etc/hosts` as root:
   ```bash
   sudo nano /etc/hosts
   ```
2. Remove lines containing blocked sites (e.g., lines with `youtube.com`)
3. Save and exit

## Customization

### Adding/Removing Blocked Sites

Edit the `SITES` array in `sitesManager.sh`:

```bash
SITES=(
    "youtube.com"
    "www.youtube.com"
    "reddit.com"
    "twitter.com"
    # Add more sites here
)
```

### Changing Prep Time

Modify line 74 in `index.py`:
```python
prep_time = 2 * 60  # Change 2 to desired minutes
```

## Reflection Questions

After each session, you'll be prompted with:
1. What did you learn today?
2. How would you rate your performance today? (1-5 scale)
3. Why do you think it was like that?
4. What would you do next time?

Responses are automatically saved with timestamps to track your learning progress.

## Troubleshooting

### "Permission denied" errors
- Ensure `sitesManager.sh` is executable: `chmod +x sitesManager.sh`
- Run with `sudo` when prompted

### Sites still blocked after session
- Manually edit `/etc/hosts` to remove blocked entries (see Safety Notes above)

### Script not found
- Ensure you're running from the script directory
- Use absolute path: `python3 /path/to/ritual_script/index.py`

## Future Improvements

- [ ] File naming with sequential numbers (01, 02, 03...)
- [ ] Spotify integration for study music
- [ ] Configuration file for blocked sites
- [ ] Cross-platform support (Windows/macOS)
- [ ] Backup and restore for `/etc/hosts`
- [ ] GUI interface option

## Contributing

Feel free to fork, modify, and submit pull requests. This is a personal productivity tool that could benefit others with similar study habits.

## License

This project is open source. Use and modify as needed for your own productivity needs.

---

**Note**: This tool modifies system files and requires elevated privileges. Review the code before running, especially `sitesManager.sh`, to ensure you're comfortable with the modifications it makes to your system.
