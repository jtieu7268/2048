# 2048 Game

This features implementations for playing the 2048 game through text-based and graphical interfaces.

The objective of 2048 is to create a tile of the target score, e.g., 2048, by sliding tiles up, left, right, down. Sliding tiles merges tiles with the same value to create a doubled tile.

A player can use the text-based interface to play the game through their terminal or launch the graphical interface.

In either version, the player will select a target score to play to. ```W```, ```A```, ```S```, and ```D``` can be used to slide the tiles up, left, down, and right respectively. The graphical interface also allows the player to use the arrow keys to move the tiles. To quit, press ```Q```. To restart press ```R```.

## Technologies

Built using Python. The implementation for the graphical interface requires the pygame module to be downloaded (version 2.6.0 or later).

## Setting up

1. Clone this repository.

```git clone https://github.com/jtieu7268/2048.git```

2. Install pygame.

```python3 -m pip install -U pygame --user```

3. Run the game.

The text-based version can be played by running ```play_2048.py``` as main.

``` python3 play_2048.py```

The graphical user interface version can be played by running ```play_2048_gui.py``` as main. 

```python3 play_2048_gui.py```

## Features

* Start the game

* Select a target score

* Play the game

* Continue playing, quit or restart
