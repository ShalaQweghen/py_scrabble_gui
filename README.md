# Command-Line Scrabble

Complete with optional challenge mode, time limit and multiplayer over a network connection. You can choose different options from the game interface.

You can also play against computer.

If you don't know how to play Scrabble, click [here](https://en.wikipedia.org/wiki/Scrabble) for rules

Clone the game and enjoy it. If you have any feedbacks, I will very much appreciate.

### Start a game

`cd` into py_scrabble directory and run:
```python
python3 start_game.py
```

In order to get the meanings of the words made during the game and save them in a txt file, run:
```python
python3 start_game.py -d
```

At the end of the game, word meanings will be fetched from the internet if available and a `words.txt` file will be saved in the root directory of the game.

### Number of players

You can play the game as 2, 3, or 4 players.

### Making a word

State the starting square of your word using the names of the columns and the rows: eg. `h8`, `b12`. When you state the starting square and the direction(`r` for right or `d` for down), the game will make a range for it. For example, you want to place the word "money" starting the from the square "h8" to the right side (i.e. `h8 r money`). The game will make the range accordingly as "h8=M, i8=O, j8=N, k8=E, l8=Y". If one of the squares in the range of your word is occupied, as long as the occupying letter is the same as the letter corresponding that square in your word, your word will be placed on the board.

### Passing

Enter `pass` as your starting square and you will be prompted for the letters you wish to change.

### Blank tile

When you have and want to use a blank tile(@), put it in place of the missing letter in your word (eg. You want to make "money" but you don't have a letter "n". If you have a blank tile(@), you can make your word like this: "mo@ey"). When you use a blank tile, you will be asked for what letter it is used for. Type the letter it substitutes.

### Multiple words

When you place your word on the board and make more than one word, you will get the points of those new word. You will only get the bonus squares if they are in the range of your new word. The interface will only display the word that was placed on the word but the points for the extra words will be added to your score.

### Saving the game

In order to save the game, enter 'save' and you will be prompted to enter a name for your saved game. The game will create a saves folder in the game root folder and in the saves file, an obj file named as your save game.

### Loading the game

When loading a saved game, if there is not a saves file or there are no files with the specified name, a new game will be started.

### Challenge mode

When selected, if a player enters a word that is not in the dictionary, his or her turn will be passed.

### Time limit

Players can set how long a game will last in minutes. After the specified time, the game will be over and the player with the most points will win. If the time ends while making a word, the word will not count.

### Multilayer game over a network connection

When selected, a server will fire up at port 12345 on your localhost. The player will be prompted about the number of the players that will play the game. When another computers (as many as specified by the player) on the network run 'python3 join_game.rb your_ip_address', a game will start. The connecting computers don't need to have the whole game script. If a game doesn't start, the firewall might be blocking incoming requests. Make sure to make the necessary adjustments.

### Playing against computer

Computer goes through permutations of letters on its rack and picks the valid move with the most points. A turn for computer takes about 1 minute 20 seconds (on i5 1.6 GHz with 8 GB RAM) depending on the computer.

### Screenshots

![](pics/pic_1.png)
![](pics/pic_2.png)
![](pics/pic_3.png)