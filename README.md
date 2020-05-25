# friends_character_assigner
A small application that assigns Friends characters for Friends TV drinking game

To facilitate our Friends TV drinking game with friends, I have built a tool that randomly assigns each player to a Friends character.

https://psycatgames.com/magazine/party-games/friends-tv-show-drinking-game/
https://realpython.com/pyinstaller-python/#preparing-your-project

```
pyinstaller cli.py --add-data assets/friends3.jpg:assets --onefile -w
python friends_generator.py --players jane,jack,jill,julian,jeremy,julia --pick_all
```
