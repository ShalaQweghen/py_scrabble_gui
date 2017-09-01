===============================================================================

* Number of Players => You can play the game as 2, 3, or 4 players.

* Making a word => State the starting square of a word using the names of the
  columns and the rows: eg. 'h8', 'b12'. When the player states the starting
  square and the direction ('r' for right or 'd' for down) of a word, the game
  will make a range for it. For example, when the player enters 'h8 r money',
  the game will make the range accordingly as 'h8=M, i8=O, j8=N, k8=E, l8=Y'.
  If one of the squares in the range of the word is occupied, as long as the
  occupying letter is the same as the letter corresponding that square in the
  word, the word will be places on the board.

* Passing => Enter 'pass' when prompted for a move and you will be prompted
  for the letters you wish to change.

* Blank tile => When the player has and wants to use a blank tile (@), it
  should be placed on the same position of the missing letter in the word (eg.
  The word is 'money' but letter 'n' is not on the rack. If the player has a
  blank tile (@), the word can be made as 'mo@ey'). When a blank tile is used,
  the player will be prompted for what letter it is used for. Type the letter
  it substitutes.

* Multiple words => When a word is placed on the word and it makes more than
  one word, the player will get the points for the new word as well. Bonues
  squares are calculated if they are in the range of the new word.

* Saving the game => In order to save the game, enter 'save' and you will be
  prompted to enter a name for your saved game. The game will create a saves
  folder in the game root folder and in the saves file, an obj file named as
  your save game.

* Loading the game => When loading a saved game, the player should enter the
  correct filename for the saved game. Otherwise, a new game will be started.

* Challenge mode => When on challenge mode, if the player enters a word that is
  not in the dictionary, the turn will be passed.

* Time limit => Players can set how long a game will last. After the specified
  time, the game will be over and the player with the most points will win. If
  the time ends while making a word, the word will not count.

* Multiplayer game over a network connection => When picked, a server will fire
  up at port 12345 on your localhost. The player will be prompted about the
  number of the players that will play the game. When another computers (as
  many as specified by the player) on the network run 'python3 join_game.py
  your_ip_address', a game will start. The connecting computers don't need to
  have the whole game script. If a game doesn't start, the firewall might be
  blocking incoming requests. Make sure to make the necessary adjustments.

================================================================================