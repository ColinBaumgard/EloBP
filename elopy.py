import pickle

class Elo:
    """
    A class that represents an implementation of the Elo Rating System
    """

    def __init__(self, base_rating=1000, k = 40):
        """
        Runs at initialization of class object.
        @param base_rating - The rating a new player would have
        """
        self.base_rating = base_rating
        self.k = k
        self.scores = {}
        try:
            with open('scores.bp', 'rb') as file:
                self.scores = pickle.load(file)
        except:
            with open('scores.bp', 'wb') as file:
                pickle.dump(self.scores, file)

    def save(self):
        with open('scores.bp', 'wb') as file:
            pickle.dump(self.scores, file)

    def __getPlayerList(self):
        """
        Returns this implementation's player list.
        @return - the list of all player objects in the implementation.
        """
        return self.scores.keys

    def isPlayer(self, name):
        """
        Returns the player in the implementation with the given name.
        @param name - name of the player to return.
        @return - the player with the given name.
        """
        return name in self.scores


    def addPlayer(self, name, rating=None):
        """
        Adds a new player to the implementation.
        @param name - The name to identify a specific player.
        @param rating - The player's rating.
        """
        if rating == None:
            rating = self.base_rating

        self.scores[name] = rating
        self.save()

    def removePlayer(self, name):
        """
        Adds a new player to the implementation.
        @param name - The name to identify a specific player.
        """
        if self.isPlayer(name):
            del self.scores[name]

        self.save()


    def record1v1Match(self, name1, name2, winner=None, draw=False):
        """
        Should be called after a game is played.
        @param name1 - name of the first player.
        @param name2 - name of the second player.
        """

        expected1, expected2 = self.compareRating(self.scores(name1), self.scores(name2))


        if draw:
            score1 = 0.5
            score2 = 0.5
        elif winner == name1:
            score1 = 1.0
            score2 = 0.0
        elif winner == name2:
            score1 = 0.0
            score2 = 1.0
        else:
            raise InputError('One of the names must be the winner or draw must be True')

        newRating1 = self.scores[name1] + self.k * (score1 - expected1)
        newRating2 = self.scores[name2] + self.k * (score2 - expected2)

        if newRating1 < 0:
            newRating1 = 0
            newRating2 = rating2 - rating1

        elif newRating2 < 0:
            newRating2 = 0
            newRating1 = rating1 - rating2

        self.scores[name1] = newRating1
        self.scores[name2] = newRating2

        self.save()


    def recordXvXMatch(self, team1, team2, winner=None, draw=False):
        """
        Should be called after a game is played.
        @param name1 - name of the first player.
        @param name2 - name of the second player.
        """
        score1, score2 = 0, 0


        for name in team1:
            score1 += self.scores[name] 
        score1 = score1/len(team1)

        for name in team2:
            score2 += self.scores[name] 
        score2 = score2/len(team2)
        
        expected1, expected2 = self.compareRating(score1, score2)


        if draw:
            score1 = 0.5
            score2 = 0.5
        elif winner == 0:
            score1 = 1.0
            score2 = 0.0
        elif winner == 1:
            score1 = 0.0
            score2 = 1.0
        else:
            raise InputError('One of the names must be the winner or draw must be True')

        for name in team1:

            self.scores[name] = max(0, self.scores[name] + self.k * (score1 - expected1))           

        
        for name in team2:
            self.scores[name] = max(0, self.scores[name] + self.k * (score2 - expected2))


        self.save()

    def getPlayerRating(self, name):
        """
        Returns the rating of the player with the given name.
        @param name - name of the player.
        @return - the rating of the player with the given name.
        """
        sorted_x = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        classement = 0

        ok = False

        while not ok:
            if sorted_x[classement][0] == name:
                ok = True
            classement += 1

        return int(self.scores[name]), classement

    def getRatingList(self):
        """
        Returns a list of tuples in the form of ({name},{rating})
        @return - the list of tuples
        """
        sorted_x = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_x
    

    def compareRating(self, score1, score2):
        """
        Compares the two ratings of the this player and the opponent.
        @param opponent - the player to compare against.
        @returns - The expected score between the two players.
        """

        scoreA = ( 1+10**( ( score2 - score1 )/400.0 ) ) ** -1
        scoreB = ( 1+10**( ( score1 - score2 )/400.0 ) ) ** -1
        
        return scoreA, scoreB


if __name__ == "__main__":
    elo = Elo()
    elo.addPlayer('Colin')
    elo.addPlayer('Raul')

    print(elo.getRatingList())
    elo.recordMatch('Colin', 'Raul', 'Raul')
    print(elo.getRatingList())