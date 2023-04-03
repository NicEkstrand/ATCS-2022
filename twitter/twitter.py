from models import *
from database import init_db, db_session
from datetime import datetime

class Twitter:
    def __init__(self, logged_in = False, user = None):
        self.logged_in = logged_in
        self.user = user

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
            username = input("What will your Twitter username be?\n")
            #Checks if username is taken
            matches = False
            results = db_session.query(User)
            for user in results:
                if username == user.username:
                    print("That username already exists, please enter a different one\n")
                    matches = True
                    break
            if not matches:
                good_input = True
        #Asks for password, two step matches, and adds user to database
        new_password = input("What will your password be?\n")
        good_input = False
        while good_input == False:
            if input("\nRepeat your password\n") == new_password:
                print("\nAwesome, welcome to twitter " + username)
                person = User(username, new_password)
                db_session.add(person)
                db_session.commit()
                good_input = True
                self.user = person
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

            #Matches inputs with users database
            target = db_session.query(User).where(User.username == name and User.password == password).first()
            if target != None:
                print("Logged in. Welcome " + name)
                self.user = target
                good_input = True
                self.logged_in = True
            else:
                print("Invalid username or password\n")
    
    def logout(self):
        confirm = input("Are you sure you want to log out?(y/n)\n")
        if confirm == "y":
            print("Logged out")
            self.user = None
            self.logged_in = False
            self.startup()
        #Doesn't need else bc will auto go back to menu

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
        username = input("Who would you like to follow?\n")
        #takes target from user db and answers all possible outcomes
        target = db_session.query(User).where(User.username == username).first()

        if target is None:
            print("This user doesn't exist")
            print("___________________________________________")
        else:
            matches = False
            for user in self.user.following:
                if user.username == target.username:
                    print("You already follow this person")
                    print("___________________________________________")
                    matches = True
            if not matches:
                self.user.following.append(target)
                print("You are now following " + target.username)
                print("___________________________________________")
        db_session.commit()

    def unfollow(self):
        username = input("Who would you like to unfollow?")
        #Takes target from user db and answers all possible outcomes
        target = db_session.query(User).where(User.username == username).first()
        if target is None:
            print("This user doesn't exist")
            print("___________________________________________")
        
        else:
            matches = False
            for user in self.user.following:
                if user.username == target.username:
                    matches = True
                    print("You no longer follow " + target.username)
                    print("___________________________________________")
                    self.user.following.remove(target)
                    db_session.commit()
            if not matches:
                print("You never followed this person")
                print("___________________________________________")
                


    def tweet(self):
        text = input("Tweet something: ")
        included_tags = input("Enter your tags separated by spaces: ")
        #Creates Tweet object and adds to db
        tweet = Tweet(text, datetime.now(), self.user.username)
        db_session.add(tweet)
        db_session.commit()
        #Creates Tag objects and adds to db
        for tag in included_tags.split():
            new_tag = db_session.query(Tag).where(Tag.content == tag).first()
            if new_tag == None:
                new_tag = Tag(tag)
                db_session.add(new_tag)
                db_session.commit()
            db_session.add(TweetTag(tweet.id, new_tag.id))
        db_session.commit()


    def view_my_tweets(self):
        self.print_tweets(self.user.tweets)
            
    

    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        results = db_session.query(Tweet).order_by(Tweet.timestamp.desc()).limit(5)
        for tweet in results:
            print(tweet)
        #self.view_my_tweets(results)

    def search_by_user(self):
        #Finds user in db that matches input
        target = db_session.query(User).where(User.username == input("Enter a username: ")).first()
        if target != None:
            self.print_tweets(target.tweets)
        else:
            print("There is no user with that name")
        

    def search_by_tag(self):
        #Finds user in db that matches input
        target = db_session.query(Tag).where(Tag.content == input("Enter a tag: ")).first()
        if target != None:
            self.print_tweets(target.tweets)
        else:
            print("That tag does not exist")

    """
    Allows the user to select from the 
    ATCS Twitter Menu
    """
    def run(self):
        init_db()

        print("Welcome to ATCS Twitter!")
        self.startup()
        while(self.logged_in):

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
