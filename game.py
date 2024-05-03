from settings import *
import time

# PYGAME LOOP
start_ticks = pygame.time.get_ticks()
while True:
    PygameEvents = pygame.event.get()
    keys = pygame.key.get_pressed()
    # Mouse Position
    MousePosition = pygame.mouse.get_pos()

    # QUIT
    for event in PygameEvents:
        if event.type == pygame.QUIT:
            Quit()

    # Time
    MillisecondsPassed = pygame.time.get_ticks() - start_ticks

    # Intro Screen
    if MillisecondsPassed / 1000 < IntroTime - 0.5:
        PygameLogo_rect = PygameLogo.convert_alpha().get_rect()
        PygameLogo_rect.center = PygameLogoPosition
        screen.blit(PygameLogo.convert_alpha(), PygameLogo_rect)

        IntroMazeText_rect = IntroMazeText.get_rect()
        IntroMazeText_rect.midtop = (PygameLogo_rect.midbottom[0] - 20,
                                     PygameLogo_rect.midbottom[1])  # Adjusting the Position of the position of the text
        screen.blit(IntroMazeText, IntroMazeText_rect)

        IntroLoadingBarBackground_rect = IntroLoadingBarBackground.get_rect()
        IntroLoadingBarBackground_rect.midtop = (IntroMazeText_rect.midbottom[0], (IntroMazeText_rect.midbottom[1] + 50))
        screen.blit(IntroLoadingBarBackground, IntroLoadingBarBackground_rect)

        xLength = 480 * MillisecondsPassed / ((IntroTime - 0.5) * 1000)
        IntroLoadingBar = LoadScaledImage("media/images/IntroLoadingBar/IntroLoadingBar.png", scaling_dim=(xLength, 40))
        IntroLoadingBar_rect = IntroLoadingBar.get_rect()
        IntroLoadingBar_rect.midleft = (IntroLoadingBarBackground_rect.midleft[0] + 10, IntroLoadingBarBackground_rect.midleft[1])
        screen.blit(IntroLoadingBar, IntroLoadingBar_rect)
    elif int((MillisecondsPassed / 1000) * 4) / 4 == IntroTime - 0.25:
        screen.fill("Black")
    elif int((MillisecondsPassed / 1000) * 4) / 4 == IntroTime + 0.25:
        main_menu.is_active = True
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(IntroMusicAddress)
            pygame.mixer.music.set_volume(0.25 * int(GamePreferences.MusicState))
            pygame.mixer.music.play(-1)

    # Main Menu
    if main_menu.is_active:
        # Setting the frame rate
        main_menu.BackgroundFrameIndex = (MillisecondsPassed % (
                MainMenuBackgroundFrameTime * len(MainMenuBackground))) // MainMenuBackgroundFrameTime
        # Main Menu Background
        main_menu.BackgroundDisplay(MainMenuBackground[main_menu.BackgroundFrameIndex])
        # Header of the MainMenu
        MainMenuHeaderLogo_rect = MainMenuHeaderLogo.get_rect()
        MainMenuHeaderLogo_rect.center = MainMenuHeaderLogoPosition
        screen.blit(MainMenuHeaderLogo, MainMenuHeaderLogo_rect)
        MainMenuMazeText_rect = MainMenuMazeText.get_rect()
        MainMenuMazeText_rect.midtop = (MainMenuHeaderLogo_rect.midbottom[0] - 10, MainMenuHeaderLogo_rect.midbottom[1] + 20)
        screen.blit(MainMenuMazeText, MainMenuMazeText_rect)
        # Main Menu Buttons
        main_menu.Buttons()
        if MM_Quit.is_Clicked():
            Quit()
        elif MM_Play.is_Clicked():
            main_menu.is_active = False
            time.sleep(ButtonDelay)
            Game.is_active = True
        elif MM_Scores.is_Clicked():
            main_menu.is_active = False
            time.sleep(ButtonDelay)
            Scores.is_active = True
        elif MM_Preferences.is_Clicked():
            main_menu.is_active = False
            time.sleep(ButtonDelay)
            GamePreferences.is_active = True

    # The Game!
    if Game.is_active:
        if Game.LevelScreen:
            # Background Static
            main_menu.BackgroundDisplay(MainMenuBackground[0])
            # Buttons
            GLB_Easy.display()
            GLB_Medium.display()
            GLB_Difficult.display()

            GLB_Level_Back.display()

            # Button Functionality Implementation
            if GLB_Easy.is_Clicked() or GLB_Medium.is_Clicked() or GLB_Difficult.is_Clicked():
                Game.LevelScreen = False
                if GLB_Easy.is_Clicked():
                    Game.Level = 1
                elif GLB_Medium.is_Clicked():
                    Game.Level = 2
                elif GLB_Difficult.is_Clicked():
                    Game.Level = 3
                Game.GameScreen = True
                Game.SetMazeLevel()
                time.sleep(ButtonDelay)
                pygame.mixer.music.stop()
                pygame.mixer.music.load(GameplayMusicAddress)
                pygame.mixer.music.set_volume(0.2 * int(GamePreferences.MusicState))
                pygame.mixer.music.play(-1)
            elif GLB_Level_Back.is_Clicked():
                Game.is_active = False
                main_menu.is_active = True
                time.sleep(BackButtonDelay)
        elif Game.GameScreen:
            screen.fill("Black")

            Game.GamePlay(keys, MillisecondsPassed)

            # Right Background for Displaying Buttons
            screen.blit(GameRightBackground, (screen.get_height() + Game.XShift, 0))

            # StopWatch
            StopWatchButton = MainMenu.MainMenuButton(screen, f"Time Elapsed = {int(Game.StopwatchValue / 1000)}s",
                                                      GameStopwatchFont, GameStopwatchFont, TimeButtonImage,
                                                      StopWatchButtonPos)
            StopWatchButton.display()

            # Change Background Button
            Game_ChangeBackground.display()
            # Back Button
            Game_Back.display()

            # Sound Button
            if GamePreferences.MusicState and not Game_Sound.ButtonRect.collidepoint(MousePosition[0],
                                                                                     MousePosition[1]):
                Game_Sound.display()
            else:
                # Muted Symbol
                screen.blit(SoundControlButtonImageOff.convert_alpha(),
                            SoundControlButtonImageOff.convert_alpha().get_rect(center=GameSoundButtonPos))

            if Game_Sound.is_Clicked():
                GamePreferences.MusicState = not GamePreferences.MusicState
                pygame.mixer.music.set_volume(0.25 * int(GamePreferences.MusicState))
                time.sleep(SoundButtonDelay)
            elif Game_ChangeBackground.is_Clicked():
                Game.ChangeBackground()
                time.sleep(SoundButtonDelay)

            # Back Button Functionality
            if Game_Back.is_Clicked():
                Game.MazeGame = None
                Game.GameScreen = False
                Game.LevelScreen = True
                time.sleep(ButtonDelay)
                pygame.mixer.music.stop()
                pygame.mixer.music.load(IntroMusicAddress)
                pygame.mixer.music.set_volume(0.25 * int(GamePreferences.MusicState))
                pygame.mixer.music.play(-1)

            if Game.GameOverScreen:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(GameOverMusicAddress)
                pygame.mixer.music.set_volume(0.2 * int(GamePreferences.MusicState))
                pygame.mixer.music.play()
        elif Game.GameOverScreen:
            # Background Static
            main_menu.BackgroundDisplay(MainMenuBackground[0])
            Game.GameOverScreenDisplay()
            GameOver_Back.display()

            # StopWatch
            TimeTakenButton = MainMenu.MainMenuButton(screen, f"TIME TAKEN = {int(Game.StopwatchValue / 1000)} SEC",
                                                      ButtonsFontInactive, ButtonsFontInactive, TimeButtonImage,
                                                      TimeTakenButtonPos)
            TimeTakenButton.display()

            # High Score
            Scores.UpdateScore(Game.StopwatchValue / 1000, Game.Level)

            # High Score String

            HighScoreString = ("NEW HIGH SCORE : " + str(int(Game.StopwatchValue / 1000)) + " SEC") if Scores.isUpdated else ("HIGH SCORE: " + Scores.HighScore(Game.Level) + " SEC")

            HighScoreButton = MainMenu.MainMenuButton(screen, HighScoreString, ButtonsFontInactive, ButtonsFontInactive,
                                                      MMButtonsImage, HighScoreButtonPos)
            HighScoreButton.display()

            # Back to Main Menu
            if GameOver_Back.is_Clicked():
                Game.MazeGame = None
                Scores.GameDone = False
                Game.is_active = False
                Game.GameOverScreen = False
                Game.LevelScreen = True
                main_menu.is_active = True
                time.sleep(BackButtonDelay)
                pygame.mixer.music.stop()
                pygame.mixer.music.load(IntroMusicAddress)
                pygame.mixer.music.set_volume(0.25 * int(GamePreferences.MusicState))
                pygame.mixer.music.play(-1)

    # Preferences
    if GamePreferences.is_active:
        # Background Static
        main_menu.BackgroundDisplay(MainMenuBackground[0])

        GP_MusicText.display()
        GP_Back.display()
        if GamePreferences.MusicState and not GP_Sound.ButtonRect.collidepoint(MousePosition[0], MousePosition[1]):
            GP_Sound.display()
        else:
            # Muted Symbol
            screen.blit(SoundControlButtonImageOff.convert_alpha(), SoundControlButtonImageOff.convert_alpha().get_rect(
                center=((WINDOW_DIM[0] / 2 + 300), (WINDOW_DIM[1] / 2 - 100))))

        if GP_Sound.is_Clicked():
            GamePreferences.MusicState = not GamePreferences.MusicState
            pygame.mixer.music.set_volume(0.25 * int(GamePreferences.MusicState))
            time.sleep(SoundButtonDelay)
        elif GP_Back.is_Clicked():
            GamePreferences.is_active = False
            main_menu.is_active = True
            time.sleep(BackButtonDelay)

    # Scores
    if Scores.is_active:
        # Background Static
        main_menu.BackgroundDisplay(MainMenuBackground[0])

        Scores.DisplayHighScores()

        Scores_Back.display()

        if Scores_Back.is_Clicked():
            Scores.is_active = False
            time.sleep(BackButtonDelay)
            main_menu.is_active = True

    pygame.display.update()
