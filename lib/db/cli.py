import sys
import random
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import esrb_rating, game_platform_join, Game, Platform, Genre
from helpers import print_game_info

engine = create_engine('sqlite:///data.db')
Session = sessionmaker(bind=engine)
session = Session()

#Clear Screen
def clear_screen():
    if os.name == 'posix':  # Unix/Linux/MacOS
        os.system('clear')
    elif os.name == 'nt':  # Windows
        os.system('cls')

# Main Menu

    # Render
def render_main_menu():
    print("Welcome to Game Catalog")
    print("Please selct one of the following options")
    print("1. My Games")
    print("2. Edit Games")
    print("3. Exit")

    # Init Main_Menu
def main_menu():
    while True:
        render_main_menu()
        option = input("Please selct one of the following options: ")

        if not option.isdigit():
            print("Invalid Input. Please enter a valid input.")
            continue
    
        option = int(option)

        if option == 1:
            clear_screen()
            my_games()
            break
        elif option == 2:
            clear_screen()
            edit_games()
            break
        elif option == 3:
            print("Goodbye...")
            sys.exit()

        else:
            print("Invalid Input. Please enter a valid input.")

# My Game

    # Render
def render_my_games():
    print("\nMy Games:")
    print("1. View All Games")
    print("2. Search Game By Title")
    print("3. Search Game By Platform")
    print("4. Main Menu")
    print("5. Exit")

    # Init My_Game
def my_games():
    while True:
        render_my_games()
        option = input("Please selct one of the following options: ")

        if not option.isdigit():
            print("Invalid Input. Please enter a valid input.")
            continue
    
        option = int(option)

        if option == 1:
            clear_screen()
            games = session.query(Game).all()
            for game in games:
                print_game_info(game)
            print("complete")   
        elif option == 2:
            clear_screen()
            search_title = input("Enter the game title: ")
            match_games = session.query(Game).filter(Game.title.startswith(search_title)).all()
    
            if match_games:
                for game in match_games:
                    print_game_info(game)
            else:
                print("No games match the search criteria.")

        elif option == 3:
            clear_screen()
            platform_search()
            break
        elif option == 4:
            clear_screen()
            main_menu()
            break
        elif option == 5:
            print("Goodbye...")
            sys.exit()
        else:
            print("Invalid Input. Please enter a valid input.")
   
# Edit Game

    # Render
def render_edit_games():
    print("\nEdit Games")
    print("1. Add A Game")
    print("2. Edit A Game")
    print("3. Delete A Game")
    print("4. Main Menu")
    print("5. Exit")
    
    # Init Edit   
def edit_games():
    while True:
        render_edit_games()
        option = input("Please selct one of the following options: ")

        if not option.isdigit():
            print("Invalid Input. Please enter a valid input.")
            continue
    
        option = int(option)

        if option == 1:
            clear_screen()
            add_game()
            break
        elif option == 2:
            clear_screen()
            modify_game()
            break
        elif option == 3:
            clear_screen()
            delete_game()
            break
        elif option == 4:
            clear_screen()
            main_menu()
            break
        elif option == 5:
            print("Goodbye...")
            sys.exit()
        else:
            print("Invalid Input. Please enter a valid input.")

# Platfrom Search

    # Render
def render_platform_search():
    print("Select a platform option:")
    print("1. PC (Windows)")
    print("2. Web Browser")
    print("3. PC (Windows), Web Browser")
    print("4. Main Menu")
    print("5. Exit")

    #Init Platform Search
def platform_search():

    platform_mapping = {
        "1": ["PC (Windows)"],
        "2": ["Web Browser"],
        "3": ["PC (Windows)", "Web Browser"]
    }

    while True:
        render_platform_search()
        option = input("Choose a Platform: ")

        if option == "4":
            main_menu()
            break
        elif option == "5":
            print("Goodbye...")
            sys.exit()

        platform_name = platform_mapping.get(option)
        if platform_name is not None:
            platforms = [platform_name] if isinstance(platform_name, str) else platform_name

            matching_games = (
                session.query(Game)
                .join(game_platform_join)
                .join(Platform)
                .filter(Platform.name.in_(platforms))
                .all()
            )

            if matching_games:
                for game in matching_games:
                    print_game_info(game)
                    continue
                    
            
        else:
            print("Invalid Input. Please enter a valid input.")
            continue

# Init Add_Game
def add_game():
    # Game Title
    title = input("Enter the title of the game: ")

    # Genre Type
    genre_name = input("Enter the genre of the game: ")
    genre = session.query(Genre).filter(Genre.type == genre_name).first()

    if not genre:
        genre = Genre(type=genre_name)
        session.add(genre)
        session.commit()

    # Select a platform by ID
    selected_platform = None

    while True:
        print("Select a platform")
        platforms = session.query(Platform).all()
        for platform in platforms:
            print(f"{platform.id}. {platform.name}")

        platform_id = int(input("Enter the ID of the platform: "))

        if platform_id in (1, 2, 3):
            selected_platform = session.query(Platform).get(platform_id)
            break
        else:
            print("Invalid Input. Please enter a valid input.")
            continue

    if selected_platform:
        new_game = Game(
            title=title,
            esrb_rating = random.choice(esrb_rating),
            name_platform=selected_platform.name,
            platform_id=selected_platform.id,
            type_genre=genre_name,
            genre_id=genre.id
    )
    
        new_game.platform.append(selected_platform)

        session.add(new_game)
        session.commit()

    
    clear_screen()
    print("Game add successfully.")
    main_menu()

# Init Delete_Game
def delete_game():
    while True:
        search_title = input("Enter game title: ")
    
        matching_games = session.query(Game).filter(Game.title.startswith(search_title)).all()

        if matching_games:
            for game in matching_games:
                print_game_info(game)

            game_id_input = input("Enter game ID: ")

            if not game_id_input.isdigit():
                print("Invalid Input. Please enter a valid input.")
                continue

            game_id_input = int(game_id_input)
            delete_game = session.query(Game).get(game_id_input)

            if delete_game:
                confirm = input(f"Are you sure you want to delete '{delete_game.title}'? (y/n): ").lower()
                if confirm == "y":
                    delete_game.platform.clear()
                    session.delete(delete_game)
                    session.commit()
                    print("Delete Complete")
                else:
                    print("Cancel")
                    main_menu()
                    break
            else:
                print("Invalid Game with provided ID.")
                main_menu()
                break
        else:
            print("No game match the search criteria.")
            continue
        clear_screen()
        print("Game delete successfully.")
        main_menu()
        break

# Init Modify_Game
def modify_game():
    while True:
        search_title = input("Enter game title: ")
    
        matching_games = session.query(Game).filter(Game.title.startswith(search_title)).all()

        if matching_games:
            for game in matching_games:
                print_game_info(game)

            game_id_input = input("Enter game ID: ")

            if not game_id_input.isdigit():
                print("Invalid Input. Please enter a valid input.")
                continue

            game_id_input = int(game_id_input)
            modify_game = session.query(Game).get(game_id_input)

            if modify_game:
                print(f"Modifying information for '{modify_game.title}':")
                new_title = input("Enter new title or leave blank to not change: ")
                new_genre_type = input("Enter new genre or leave blank to not change: ")

                if new_genre_type:
                    new_genre = session.query(Genre).filter(Genre.type == new_genre_type).first()

                    if not new_genre:
                        new_genre = Genre(type = new_genre_type)
                        session.add(new_genre)
                        session.commit()
                        
                    modify_game.genre_id = new_genre.id
                    modify_game.type_genre = new_genre_type
               
                
                if new_title:
                    modify_game.title = new_title
                
                session.commit()
                print("Update Complete")
            
            else:
                print("Invalid Game with provided ID.")
                main_menu()
                break
        else:
            print("No game match the search criteria.")
            continue

        clear_screen()
        print("Game modify successfully.")
        main_menu()
        break
                

if __name__ == "__main__":
    main_menu()