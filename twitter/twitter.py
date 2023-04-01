from models import *
from database import init_db, db_session
from datetime import datetime

class Twitter:
    """
    The menu to print once a user has logged in
    """
    def print_menu(self):
        print("\nPlease select a menu option:")
        print("1. View Feed")
        print("2. View My Tweets")
        print("3. Search by Tag")
        print("4. Search by User")
        print("5. Tweet")
        print("6. Follow")
        print("7. Unfollow")
        print("0. Logout")
    
    """
    Prints the provided list of tweets.
    """
    def print_tweets(self, tweets):
        for tweet in tweets:
            print("==============================")
            print(tweet)
        print("==============================")

    """
    Should be run at the end of the program
    """
    def end(self):
        print("Thanks for visiting!")
        db_session.remove()
        quit()
    
    """
    Registers a new user. The user
    is guaranteed to be logged in after this function.
    """
    def register_user(self):
        good_input = False
        while good_input == False:
            username = input("What will your Twitter username be?")
            results = db_session.query(User)
            for user in results:
                if username == user.username:
                    print("That username already exists, please enter a different one")
                    continue
            good_input = True

        new_password = input("What will your password be?")
        good_input = False
        while good_input == False:
            if input("\nRepeat your password") == new_password:
                print("\nAwesome, welcome to twitter " + username)
                person = User(username, new_password)
                db_session.add(person)
                db_session.commit()
                good_input = True
            else:
                print("\nDoesn't match")
        
    """
    Logs the user in. The user
    is guaranteed to be logged in after this function.
    """
    def login(self):
        good_input = False
        while good_input == False:
            name = input("Username: ")
            password = input("Password: ")

            results = db_session.query(User)
            for user in results:
                if user.username == name and user.password == password:
                    print("Logged in. Welcome " + name)
                    self.user = user
                    good_input = True
                else:
                     print("Invalid username or password\n")
                        

    
    def logout(self):
        confirm = input("Are you sure you want to log out?(y/n)")
        if confirm == "y":
            print("Logged out")
            self.user = None

    """
    Allows the user to login,  
    register, or exit.
    """
    def startup(self):
        print("Select a menu option\n")
        want = input("0: Log in\n" + "1: Sign up\n" + "2: Exit")

        if want == "0":
            self.login()
        elif want == "1":
            self.register_user()
        else:
            self.end()

        

    def follow(self):
        username = input("Who would you like to follow?")
        target = db_session.query(User).where(User.username == username).first()
        self.user.following.append(target)
        db_session.commit()

    def unfollow(self):
        username = input("Who would you like to unfollow?")
        target = db_session.query(User).where(User.username == username).first()
        self.user.following.delete(target)
        db_session.commit()
    def tweet(self):
        pass
    
    def view_my_tweets(self):
        pass
    

    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        pass

    def search_by_user(self):
        pass

    def search_by_tag(self):
        pass

    """
    Allows the user to select from the 
    ATCS Twitter Menu
    """
    def run(self):
        init_db()

        print("Welcome to ATCS Twitter!")
        self.startup()

        self.print_menu()
        option = int(input(""))

        if option == 1:
            self.view_feed()
        elif option == 2:
            self.view_my_tweets()
        elif option == 3:
            self.search_by_tag()
        elif option == 4:
            self.search_by_user()
        elif option == 5:
            self.tweet()
        elif option == 6:
            self.follow()
        elif option == 7:
            self.unfollow()
        else:
            self.logout()
        
        self.end()
