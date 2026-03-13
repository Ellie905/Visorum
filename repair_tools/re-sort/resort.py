#!/usr/bin/env python3

# ============================================================
# VISORUM REPAIR TOOL
# Category-focused archive re-sorter
#
# Script location:
# yt-dlp/1_New_Downloads/repair_tools/re-sort/resort.py
#
# Workflow:
# 1. Choose category to inspect
# 2. Iterate videos in that category
# 3. Optionally re-sort videos to another category
# ============================================================

import json
import shutil
from pathlib import Path

# ------------------------------------------------------------
# PATH SETUP
# ------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parents[2]  # yt-dlp root

IGNORE_FOLDERS = {"1_New_Downloads"}

# ------------------------------------------------------------
# CATEGORY DISCOVERY
# ------------------------------------------------------------

def get_categories():
    return sorted([
        p.name for p in ROOT_DIR.iterdir()
        if p.is_dir() and p.name not in IGNORE_FOLDERS
    ])

# ------------------------------------------------------------
# VIDEO ENUMERATION
# ------------------------------------------------------------

def get_videos(category):
    cat_path = ROOT_DIR / category

    if not cat_path.exists():
        return []

    return sorted([p for p in cat_path.iterdir() if p.is_dir()])

# ------------------------------------------------------------
# METADATA EXTRACTION
# ------------------------------------------------------------

def read_metadata(video_path):

    for jf in video_path.glob("*.json"):
        try:
            with open(jf, "r", encoding="utf-8") as f:
                data = json.load(f)

            return data.get("uploader"), data.get("upload_date")

        except Exception:
            continue

    return None, None

# ------------------------------------------------------------
# DISPLAY VIDEO INFO
# ------------------------------------------------------------

def show_video(video_path, category, cur_vid, tot_vid):

    print()
    print("--------------------------------------------------")
    print(f"Current Category: {category}")
    print(f"Video Folder: {video_path.name}")
    print(f"Video {cur_vid} of {tot_vid}")
    print("--------------------------------------------------")

    uploader, upload_date = read_metadata(video_path)

    if uploader or upload_date:
        print(f"Uploader: {uploader}")
        print(f"Upload date: {upload_date}")

    print("\nFiles in folder:")

    for f in sorted(video_path.iterdir()):
        print(f"  {f.name}")

# ------------------------------------------------------------
# CATEGORY MENU
# ------------------------------------------------------------

def show_categories(categories):

    print("\nAvailable categories:")

    for i, cat in enumerate(categories, start=1):
        print(f"{i:2d}. {cat}")

    print(" q. Quit")

# ------------------------------------------------------------
# CATEGORY SELECTION
# ------------------------------------------------------------

def select_category(categories):

    while True:

        show_categories(categories)

        choice = input("\nSelect category to inspect: ").strip().lower()

        if choice == "q":
            return None

        if choice.isdigit():

            num = int(choice)

            if 1 <= num <= len(categories):
                return categories[num - 1]

        print("Invalid selection.")

# ------------------------------------------------------------
# VIDEO ACTION PROMPT
# ------------------------------------------------------------

def video_action():

    print("\n1. Re-sort this video")
    print("2. Keep / next video")
    print("q. Return to category selection")

    while True:

        choice = input("Choice: ").strip().lower()

        if choice in {"1", "2", "q"}:
            return choice

        print("Invalid selection.")

# ------------------------------------------------------------
# TARGET CATEGORY PROMPT
# ------------------------------------------------------------

def choose_target_category(categories):

    while True:

        print("\nMove video to:")

        for i, cat in enumerate(categories, start=1):
            print(f"{i:2d}. {cat}")

        print(" 0. Cancel")

        choice = input("Category #: ").strip()

        if choice == "0":
            return None

        if choice.isdigit():

            num = int(choice)

            if 1 <= num <= len(categories):
                return categories[num - 1]

        print("Invalid selection.")

# ------------------------------------------------------------
# MOVE VIDEO
# ------------------------------------------------------------

def move_video(video_path, target_category):

    target = ROOT_DIR / target_category / video_path.name

    if target.exists():
        print("ERROR: target already exists. Skipping move.")
        return

    shutil.move(str(video_path), str(target))
    print(f"Moved to {target_category}/")

# ------------------------------------------------------------
# CATEGORY WORK LOOP
# ------------------------------------------------------------

def process_category(category, categories):

    videos = get_videos(category)

    if not videos:
        print("\nNo videos in this category.")
        return

    cur_vid = 1
    tot_vid = len(videos)

    for video_path in videos:

        while True:

            show_video(video_path, category, cur_vid, tot_vid)

            action = video_action()

            if action == "2":
                cur_vid += 1
                #continue
                break

            if action == "q":
                return

            target = choose_target_category(get_categories())

            if target is None:
                # stay on same video
                continue

            if target == category:
                print("Already in that category.")
                continue

            move_video(video_path, target)
            cur_vid += 1
            break

# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

def main():

    categories = get_categories()

    if not categories:
        print("No category folders found.")
        return

    while True:

        categories = get_categories()
        category = select_category(categories)

        if category is None:
            print()
            print("--------------------------------------------------")
            print("Exiting safely.")
            print("Don't forget to rerun Step 5 to see your changes\nwithin Visorum GUI.")
            print("--------------------------------------------------")
            return

        process_category(category, categories)


# ------------------------------------------------------------

if __name__ == "__main__":
    main()
