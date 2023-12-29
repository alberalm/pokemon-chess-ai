This project is heavily based on the work of Michael Maranan (x4nth055 on Github) and his worderful tutorial available on https://thepythoncode.com/article/make-a-chess-game-using-pygame-in-python.

The aim of this project is to build a Pokémon Chess environment to train an AI model.

Notation for Pokémon Chess games:

- Every game starts with the types of the pieces with structure "WhitePawnsA-H WhitePiecesA-H BlackPawnsA-H BlackPiecesA-H". For each type, the first two letters are used. For example:
NoFiGrPsIcFiFlGh DaWaGrStFaElBuPo NoFiGrPsIcFiFlGh DaWaGrStFaElBuPoRoDr
- Moves that would be identical in chess use the same notation (except checks, which do not exist here).
- If a move is super-effective and triggers a chain reaction, the secuence of squares the piece travels through is grouped in one, including "x" for every capture and including "+" after every super-effective hit. If the player skips its additional turn, it ends with the "+" For example:
22... cxb5+xa4+a3
- If a move is not very effective, it includes "-" at the end. For example: 14. Bxd5-
- If a not very effective capture is also a pawn promotion, it does not include the "=" or the promoted piece type. For example: 31. gxf8-
- If a move if a critical hit, it includes "\*" after the square, following the same convention as in the super-effective rule. For example:
6... Nxf5*xg3
- If a move misses, it is replaced by "/". For example: 9. /
- If a move does not affect the target, it does not include the targeted square. For example: 11... Rx
- If a move removes at least one king from the game, it ends with "#". For example: 43... Kxe3-# (this would be a draw if the white king was on e3, otherwise it would be a win for white)