import pygame


class HighScores:
    def __init__(self, screen: pygame.Surface, HighScoresFileAddress: str, HighScoresFont: pygame.Font):
        self.is_active = False
        self.screen = screen
        self.File = HighScoresFileAddress
        self.HighScoresFont = HighScoresFont
        self.GameDone = False
        self.isUpdated = False

    def HighScoreUpdate(self, NewScore, Level):
        with open(self.File, 'r') as f:
            scores = f.readlines()

        current_score = int(scores[Level - 1].strip())
        if NewScore < current_score:
            scores[Level - 1] = str(int(NewScore)) + '\n'
            with open(self.File, 'w') as f:
                f.writelines(scores)
            return True

        return False

    def UpdateScore(self, NewScore: int, Level):
        if not self.GameDone:
            self.isUpdated = self.HighScoreUpdate(NewScore, Level)
            self.GameDone = True

    def DisplayHighScores(self):
        with open(self.File, 'r') as f:
            scores = f.readlines()

        LEVEL = ["EASY : ", "MEDIUM : ", "HARD : "]

        for i in range(len(scores)):
            score = self.HighScoresFont.render(LEVEL[i] + str(scores[i].strip() + " SEC"), True, 'WHITE')
            self.screen.blit(score, score.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 100 + (i - 1) * 150)))

    def HighScore(self, Level: int):
        with open(self.File, 'r') as f:
            scores = f.readlines()

        return scores[Level - 1].strip()
