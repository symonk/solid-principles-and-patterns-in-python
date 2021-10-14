# Getting Started with Contributing

Contributing changes or new patterns and principles is straight forward:
 - Fork the repository
 - Create a new branch on your fork: `git checkout -b cool-new-pattern`.
 - Create a virtual environment: `python3 -m venv .venv`.
 - Install dependencies: `pip install -rrequirements.txt`.
 - Activate pre-commit: `pre-commit install`.
 - Apply your changes; `git add <files>`, `git commit -m "<message here>"`.
 - During commit, `pre-commit` will automatically run and lint your files if installed correctly.
 - Push to your fork: `git push`.
 - Open the PR from your fork branch `cool-new-pattern` -> the repository `master` branch (target).