# Command Line Woven Monopoly Game

### Game rules
* In Woven Monopoly, when the dice rolls are set ahead of time, the game is deterministic.There are four players who take turns in the following order:
  * Peter
  * Billy
  * Charlotte
  * Sweedal
* Each player starts with $16
* Everybody starts on GO
* You get $1 when you pass GO (this excludes your starting move)
* If you land on a property, you must buy it
* If you land on an owned property, you must pay rent to the owner
* If the same owner owns all property of the same colour, the rent is doubled
* Once someone is bankrupt, whoever has the most money remaining is the winner
* There are no chance cards, jail or stations
* The board wraps around (i.e. you get to the last space, the next space is the first space)

### Additional assumptions made (on top of the above game rules)
1. Rent is assumed to be the same as property price
2. A player is bankrupt when the money is less than 0 (i.e.if one's money is equal to 0, this player is still be in the game)

### How to run
* Make sure you have Python 3 installed.
* Clone the repo on your device using the command below:

```git clone https://github.com/Momotaro-Yvv/Woven_Monopoly.git```
* To run the version with simple result, run

```python3 main.py board.json rolls.json```
* To run the version with much details and output throughout the process, run 

```python3 main_detailed.py board.json rolls.json```

## License
This project is licensed under the MIT License - see the LICENSE.md file for details

## Contact
If you have any questions or feedback, feel free to contact me at yvonne.tao.melb2022@gmail.com.