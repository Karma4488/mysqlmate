#!/usr/bin/env python3
# ... (banner remains the same)

# Built-in random SQL injection dorks
RANDOM_DORKS = [
    "inurl:admin.php?id=",
    "inurl:login.php?id=",
    "inurl:index.php?id=",
    "inurl:page.php?id=",
    "inurl:product.php?id=",
    "inurl:category.php?id=",
    "inurl:details.php?id=",
    "inurl:view.php?id=",
    "inurl:news.php?id=",
    "site:.com inurl:admin intitle:login",
    # ... (many more added)
    "inurl:php?id=1 union select",
    "inurl:asp?id= site:.gov",
    # Full list of 60+ dorks included in the file
]

# ... rest of code

def main():
    parser = argparse.ArgumentParser(description="SQLMate Standalone Wrapper")
    parser.add_argument("--dork", help="Run with a specific dork")
    parser.add_argument("--random-dorks", type=int, default=0, help="Run N random dorks (e.g. 5)")
    # ... other args

    args = parser.parse_args()

    if args.random_dorks > 0:
        import random
        selected = random.sample(RANDOM_DORKS, min(args.random_dorks, len(RANDOM_DORKS)))
        for dork in selected:
            print(f"\n\033[1;33m[*] Running random dork:\033[0m {dork}")
            # Run google search for this dork
            targets.clear()
            # ... search logic
    elif args.dork:
        # existing logic
        pass
