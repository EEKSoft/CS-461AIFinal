# TicTacToe
This is a simple game of TicTacToe used to showcase the MiniMax algorithm. The goal of the game is to get three of your shapes in a row without letting the AI get three of their's in a row.

## How to Run
1.) Download the code and open it with Python 3.10
2.) Choose either X's or O's to be your shape.
  -(Note that X's always go first)
3.) Play your moves trying to get three in a row.

## MiniMax Algorithm
This program uses an algorithm called MiniMax which assigns values to certain outcomes, in this case board states. The algorithm then works to maximize its score by playing moves that would increase it.
Because of the "completeness" of TicTacToe in that all board states can be simulated fairly easily, the algorithm would always play a perfect game in which the player can only either lose or draw. Because of this, we implemented a small factor of randomness that gives the program a more human feel in that it will sometimes make unoptimized moves for the sake of the player being able to have the upper hand.
