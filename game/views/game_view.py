from views.sprites.sprites import MapBuilder, ChestBuilder, Finish, PgPlayer
from models.player import Player

import pygame
import pygame.locals

class GameView:
    """ Class that handles displaying the game to the user """

    def __init__(self, player: Player, game_controller, current_map):
        """ Instantiates the GameView class
        
        Args:
            player (Player): The player object for this session 
        """
        self._player = player
        self._game_controller = game_controller

        msg, self._player_name = self._get_intro_display()
        print(msg)

        # Pygame stuff
        pygame.init()
        self._window = pygame.display.set_mode((len(current_map) * 16 * 4, len(current_map[0] * 16 * 4)))
        self._clock = pygame.time.Clock()

        self._map_tiles = MapBuilder.build(current_map)
        self._chests = ChestBuilder.build(current_map)
        self._pg_player = PgPlayer(player)
        self._end = Finish(current_map)

        self._counter = 30
        self._timer_text = pygame.font.SysFont('Consolas', 30)

        pygame.time.set_timer(pygame.USEREVENT, 1000)
    
    def render(self, maze):
        """ Prints the current game view as returned by a private function
        
        Args:
            current_map (2D list): The current map-state 
        """
        running = True
        while running:
            current_map = maze.state

            self._window.fill((0, 0, 0))
            self._clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    self._counter -=1 if self._counter > 0 else 0
                if event.type == pygame.locals.QUIT:
                    raise SystemExit

            self._map_tiles.draw(self._window)
            self._chests.draw(self._window)
            self._chests.update(current_map)
            self._pg_player.update()

            self._window.blit(self._end.image, self._end.rect)
            self._window.blit(self._pg_player.image, self._pg_player.rect)

            self._window.blit(self._timer_text.render(str(self._counter), True, (255, 255, 255)), (5, 5))

            pygame.display.update()

            try:
                self._game_controller.tick(self.process_pygame_inputs())
            except SystemExit:
                running = False

    def render_game_over(self, game_controller):
        """ Prints a game over screen as returned by a private function
        
        Args:
            game_controller (GameController): The GameController for the current session 
        """
        print(self._get_game_over_display(game_controller))
    
    def process_pygame_inputs(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.locals.K_RIGHT]:
            return "d"
        elif keys[pygame.locals.K_LEFT]:
            return "a"
        elif keys[pygame.locals.K_UP]:
            return "w"
        elif keys[pygame.locals.K_DOWN]:
            return "s"
    
    def _get_text_map_display(self, current_map: list):
        """ Returns the current state of the game for the player
        
        Args:
            current_map (2D list): The current map-state 
        """
        character_mapping = {"#": "█", "P": "☻", "I": "♫", "O": "♥", "-": " ", "E": "♦"}
        rows_to_print = list()
        
        # map body
        for y in range(len(current_map[0])):
            row_to_print = "    |"

            for x in range(len(current_map)):
                row_to_print += character_mapping[current_map[x][y]] + (" " if x != len(current_map) - 1 else "")
            
            rows_to_print.append(row_to_print + "|    ")
    
        # header and footer
        rows_to_print.insert(0, "" + "=" * len(rows_to_print[0]))
        rows_to_print.insert(0, "" + f'{f"Points: {self._player.items}/5" : ^{len(rows_to_print[1])}}')
        rows_to_print.insert(0, "\n" + "=" * len(rows_to_print[2]))
        rows_to_print.append("=" * len(rows_to_print[3]))

        # stringify list
        output = ""

        for row in rows_to_print:
            output += row + "\n"
        
        return output.rstrip()

    def _get_game_over_display(self, game_controller):
        """ Returns a game over screen
        
        Args:
            game_controller (GameController): The GameController for the current session 
        """
        uploaded = game_controller.process_score(self._counter, self._player_name)

        text_to_return = f"You collected {self._player.items} out of 5 items {f'with {self._counter} seconds to spare' if self._counter > 0 else f'but weren{chr(39)}t quick enough'}"
        text_to_return += "\n" + f"{'GG, you won!' if game_controller.check_if_gg(self._counter) else 'RIP, you lost...'}"
        text_to_return += ("\n" + "Your score has been uploaded to the leaderboard") if uploaded else ""

        return text_to_return

    def _get_intro_display(self):
        """ Returns an intro screen and gets the player name """
        name = input("Please enter your name: ")
        return (f"Hurry, {name}! Collect all the batteries from the chests and recharge your frozen companion before the time runs out!", name)