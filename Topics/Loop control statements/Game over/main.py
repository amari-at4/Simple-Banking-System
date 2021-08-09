scores = input().split()

player_score = 0
player_mistakes = 0
for score in scores:
    if score == "C":
        player_score += 1
    elif score == "I":
        player_mistakes += 1
    if player_mistakes == 3:
        print("Game over")
        break
else:
    print("You won")

print(player_score)
