# ZEDVoiceBot
A telegram bot written for the legendary group ZED, storing voice ids of various files and allowing for related inline queries in Telegram.

To use the source code, you need to create a bot by contacting [@BotFather](https://t.me/botfather) in Telegram. You also need to restore the database dump to Postgres(for now, might add MySQL later as well).
```bash
psql zedvoice < zedvoice.sql
```
After these two steps, make sure you add your token and DB address to environment variables.
```bash
export TOKEN= <your_token>
export DATABASE_URL= <database_url> # default on localhost would be postgresql://localhost:5432/zedvoice
```
Install the requirements from pip:
```bash
pip install -r requirements.txt
```

And finally run the command using Python (3+):
```bash
python3 commands.py
```
### Features:
- [x] Voice Store and Retrieval
- [x] Query by tags and incomplete name (LIKE queries)
- [ ] Other media type upload, conversion and interval selection support
- [ ] Most sent voices and searchers for any user for personalized use cases.

#### Required Fixes:
- [ ] Seperating upload state machine for each user whereas currently one object for all users.
- [ ] Better edge case coverage for exception handling.
