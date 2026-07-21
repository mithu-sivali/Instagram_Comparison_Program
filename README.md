# Instagram Follower Comparison Tool

A safe, macOS-compatible Python script to compare your Instagram "Download Your Information" export data.

## What it does

- Reads your official Instagram export JSON files
- Extracts usernames from `followers_*.json` and `following.json`
- Computes accounts you follow who do not follow you back
- Prints totals and saves the result to `not_following_back.txt`

## Setup

1. Download your Instagram data using the official Instagram "Download Your Information" feature.
2. Choose the JSON format when downloading.
3. Unzip the export archive.
4. Find the exported files for followers and following, such as:
   - `followers_1.json` (or another followers JSON file)
   - `following.json`
5. Copy `instagram_compare.py` into a folder where you want to run it.

## Run the script

Open Terminal and go to the folder containing `instagram_compare.py`:

```bash
cd ~/Documents/PersonalCodingProjects/Instagram_Comparison_Program
python3 instagram_compare.py
```

Or pass file paths directly:

```bash
python3 instagram_compare.py --followers /path/to/followers_1.json --following /path/to/following.json
```

## Output

- Total following count
- Total followers count
- Sorted list of accounts you follow that do not follow you back
- File saved as `not_following_back.txt`

## Error handling

The script handles:

- Missing file paths
- Missing files
- Invalid JSON
- Export files that do not contain usernames

If the export structure changes, the script will report that it could not find valid usernames and prompt you to verify the correct Instagram JSON file.
