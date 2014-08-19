tictac
======

Tic-Tac-Toe CLI with an optimal AI implemented using a rule-baed expert system approach. The rules are based on those included in cognitive scientists Kevin Crowley and Robert S. Siegler's [analysis](http://onlinelibrary.wiley.com/doi/10.1207/s15516709cog1704_3/abstract) of children's strategy in tic-tac-toe. 

A rule-based approach made sense because of the simplistic nature of the 3x3 version of tic-tac-toe. I see a lot of minimax AI implementations for tic-tac-toe being pawned off as 'optimal', which is just not true, unless you add a bunch of heuristics. The rule-based approach allows for genuinely optiomal AI performance. Note that this implementation has only been tested on a 3x3 board. Performance of the AI is probably suboptimal on a bigger board, though my code is flexible enough to be able to handle a bigger board.
