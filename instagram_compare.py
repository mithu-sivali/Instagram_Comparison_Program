#!/usr/bin/env python3
"""Instagram follower comparison tool.

This tool reads Instagram "Download Your Information" JSON export files and compares
followers versus following to find accounts you follow that do not follow you back.

Usage:
    python3 instagram_compare.py

If you prefer, you can also pass the file paths directly:
    python3 instagram_compare.py --followers followers_1.json --following following.json
"""

import argparse
import json
import os
import re
import sys

USERNAME_RE = re.compile(r"^[A-Za-z0-9._]+$")


def is_username_candidate(value):
    """Return True if the string looks like an Instagram username."""
    if not isinstance(value, str):
        return False

    candidate = value.strip()
    return bool(USERNAME_RE.fullmatch(candidate))


def extract_usernames(data, parent_key=None):
    """Recursively find Instagram usernames in exported JSON data."""
    usernames = set()

    if isinstance(data, dict):
        # If this dict explicitly contains a username field, use it.
        for key, value in data.items():
            lower_key = key.lower()
            if lower_key in {"username", "usernames", "handle", "name", "value"}:
                if isinstance(value, str) and is_username_candidate(value):
                    usernames.add(value.strip())

        # If there is a name/value pair where the name is clearly a username label,
        # add the sibling value.
        if "name" in data and "value" in data:
            name_value = data["name"]
            raw_value = data["value"]
            if isinstance(name_value, str) and "user" in name_value.lower():
                if isinstance(raw_value, str) and is_username_candidate(raw_value):
                    usernames.add(raw_value.strip())

        # Recurse into nested fields.
        for value in data.values():
            usernames.update(extract_usernames(value, parent_key=key))

    elif isinstance(data, list):
        for item in data:
            usernames.update(extract_usernames(item, parent_key=parent_key))

    elif isinstance(data, str):
        # If raw text is in a list or value field, accept it if it looks like a username.
        if parent_key and parent_key.lower() in {"followers", "following", "username", "usernames", "value", "name"}:
            if is_username_candidate(data):
                usernames.add(data.strip())
        elif is_username_candidate(data):
            usernames.add(data.strip())

    return usernames


def load_json_file(file_path):
    """Load JSON from a file and normalize its contents."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError as error:
            raise ValueError(f"Invalid JSON in '{file_path}': {error}") from error


def read_user_list(file_path, label):
    """Read a username set from a JSON export file."""
    print(f"Reading {label} file: {file_path}")
    data = load_json_file(file_path)
    usernames = extract_usernames(data)

    if not usernames:
        raise ValueError(
            f"No valid usernames found in {label} file '{file_path}'. "
            "Make sure this is the Instagram export file for followers or following."
        )

    return usernames


def ask_for_file(prompt_text):
    """Prompt the user for a path until a non-empty response is given."""
    while True:
        answer = input(prompt_text).strip()
        if answer:
            return answer
        print("Please enter a valid file path.")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compare Instagram followers and following from official export JSON files."
    )
    parser.add_argument(
        "--followers",
        dest="followers_file",
        help="Path to followers JSON export file, e.g. followers_1.json",
    )
    parser.add_argument(
        "--following",
        dest="following_file",
        help="Path to following JSON export file, e.g. following.json",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    followers_file = args.followers_file or ask_for_file("Enter the path to your followers JSON file: ")
    following_file = args.following_file or ask_for_file("Enter the path to your following JSON file: ")

    try:
        followers = read_user_list(followers_file, "followers")
        following = read_user_list(following_file, "following")
    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")
        sys.exit(1)

    not_following_back = sorted(following - followers, key=str.lower)

    print("\nResults:")
    print(f"  Total following: {len(following)}")
    print(f"  Total followers: {len(followers)}")
    print(f"  Accounts you follow that do not follow you back: {len(not_following_back)}")

    if not_following_back:
        print("\nAccounts (usernames) that do not follow you back:")
        for username in not_following_back:
            print(f"  {username}")

    output_file = "not_following_back.txt"
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("Accounts you follow that do not follow you back:\n")
        file.write(f"Total following: {len(following)}\n")
        file.write(f"Total followers: {len(followers)}\n")
        file.write(f"Not following back: {len(not_following_back)}\n\n")

        for username in not_following_back:
            file.write(username + "\n")

    print(f"\nSaved results to: {output_file}")
    print("Open the text file to review the usernames.")


if __name__ == "__main__":
    main()
