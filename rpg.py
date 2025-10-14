import random

print("----Welcome to the Mini RPG Battle----")
player = input('Enter the player name:')
ch = ['STONE','GOBLIN','SKELETON','SHADOW']
enemy = random.choice(ch)
print(f'Your enemy is {enemy}')
player_hp = 100
enemy_hp = 100
defend = False 
mode = ['ATTACK','DEFEND',"HEAL"]

while player_hp > 0 and enemy_hp > 0:
    print(f"Your health:{player_hp} | Enemy health:{enemy_hp}")
    player = random.choice(mode)

    if player == 'ATTACK':
        damage = random.randint(10,30)
        enemy_hp = enemy_hp - damage
        print(f'You attack enemy for {damage} damage!')
    elif player == 'DEFEND':
        defend = True
        print('You defend this turn!')
    elif player == 'HEAL':
        heal = random.randint(10,25)
        player_hp = min(100, player_hp + heal)
        print(f'You healed {heal} health!')
    else:
        print('Invalid choice!Lose this turn')
        continue
#Enemy turn
    if enemy_hp > 0:
        enemy_dmg = random.randint(10,35)
        if defend:
            enemy_dmg = enemy_dmg // 2
            defend = False
            print(f'You defended and reduced enemy damage by half!')
            player_hp = player_hp - enemy_dmg
            print(f'Enemy attacks you for {enemy_dmg} damage!')
    if player_hp < 0:
        player_hp = 0
    if enemy_hp < 0:
        enemy_hp = 0
print('Battle Over')
if player_hp <= 0 and enemy_hp <= 0:
    print("It's a draw. Both you and enemy have fallen")
elif player_hp <= 0:
    print('You were defeated')
else:
    print('You won the battle')
