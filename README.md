# Discord Account Dispensory Bot

<p align="center">
<img height=300 src="Other Files/Illustration.png" alt="Account Dispenser">
</p>

## What does it do?

This discord bot dispenses account information using commands that read files in the ```Accounts``` and ```AccountsFree``` Folder.

This is a zero-fuss bot to setup. No code needs to be edited thanks to automatic account availability updating that is possible by reading the contents of the folders above. You are also able to add new acount types via Discord! This is possible due to the restock command.

---
## How to get started

You may need some Python modules to get this bot up and running, however this is easy to do. All you need can be done via this command

```
git clone https://github.com/ChrisLahd/Account-Dispenser
cd Account-Dispenser
pip install -r requirements.txt
```

After this, you can run the `main.py` file in order to get the bot up and running. If you need a bot token, Here is  [Discord's developer documentaion.]("https://discord.com/developers/docs/intro")

---
## Basic important command functions

| Command | Use |
| ----------- | ----------- |
| Restock | Appends account files |
| addUser | Whitelists the user id you provide |
| addAdmin | Gives the user id you provide admin (Allows for more commands)