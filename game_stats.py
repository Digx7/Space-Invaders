import shelve


class GameStats():
    """Track statistics for Alien Invasion"""

    def __init__(self, settings):
        """Initialize stats"""
        self.settings = settings
        self.reset_stats()

        self.game_active = False
        self.current_scene = self.settings.scenes["menu"]

        self.scores = [000]
        self.load()
        self.high_score = self.scores[0]

    def reset_stats(self):
        """Initialize stats. Can be reset at runtime"""
        self.lives_left = self.settings.total_lives
        self.current_score = 0
        self.level = 1

    def check_high_score(self):

        self.scores.append(self.current_score)
        self.update_scores()

        # if self.current_score > self.high_score:
        #     self.high_score = self.current_score
        #     return True

    def update_scores(self):
        self.scores.sort(reverse=True)
        self.high_score = self.scores[0]

        self.save()

    def save(self):
        d = shelve.open('score.txt')
        d['score'] = self.scores
        d.close()
        print("Scores Saved")

    def load(self):
        d = shelve.open('score.txt')
        if 'score' in d:
            self.scores = d['score']
            print("Scores Loaded")
        d.close()

    def is_current_scene(self, scene):
        if self.current_scene == self.settings.scenes[scene]:
            return True

    def set_current_scene(self, scene):
        self.current_scene = self.settings.scenes[scene]


