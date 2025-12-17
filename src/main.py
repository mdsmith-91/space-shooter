import pygame
import random
import sys
import os
import math

# Initialize pygame
pygame.init()
pygame.mixer.init()

# =============================================================================
# CONSTANTS
# =============================================================================

# Screen dimensions
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
BACKGROUND = (0, 0, 0)
SHIP_COLOR = (100, 200, 255)
SHIP_COCKPIT_COLOR = (50, 180, 255)
SHIP_WING_COLOR = (80, 180, 255)
SHIP_DAMAGE_COLOR = (255, 100, 100)
ASTEROID_COLORS = [(150, 150, 150), (180, 180, 180), (200, 200, 200)]
TEXT_COLOR = (200, 220, 255)
GAME_OVER_COLOR = (255, 100, 100)
PAUSE_COLOR = (255, 255, 100)
STAR_COLORS = [(255, 255, 255), (200, 200, 255), (255, 200, 200)]
LASER_COLOR = (0, 255, 255)
LASER_GLOW_COLOR = (150, 255, 255)
EXPLOSION_COLORS = [(255, 150, 50), (255, 200, 100), (255, 100, 20)]
POWERUP_COLORS = {
    'shield': (100, 255, 100),
    'rapid_fire': (255, 255, 100),
    'spread_shot': (255, 150, 255),
}
SHIELD_COLOR = (100, 255, 100)
HEALTH_COLOR = (255, 100, 100)
COMBO_COLOR = (255, 255, 100)

# Ship settings
SHIP_WIDTH = 40
SHIP_HEIGHT = 30
SHIP_SPEED = 5
SHIP_START_X = WIDTH // 4
SHIP_START_Y = HEIGHT // 2
MAX_LIVES = 3
INVULNERABILITY_FRAMES = 120
DAMAGE_FLASH_FRAMES = 10

# Asteroid settings
ASTEROID_MIN_RADIUS = 20
ASTEROID_MAX_RADIUS = 50
ASTEROID_BASE_SPEED = 5
ASTEROID_SPAWN_FREQUENCY = 60
MAX_ASTEROIDS = 8
DIFFICULTY_INCREASE_INTERVAL = 500  # Every 500 frames

# Laser settings
LASER_WIDTH = 20
LASER_HEIGHT = 6
LASER_BASE_SPEED = 10
LASER_COOLDOWN_FRAMES = 10
RAPID_FIRE_COOLDOWN = 5
SPREAD_SHOT_ANGLE = 15  # degrees

# Power-up settings
POWERUP_SIZE = 20
POWERUP_SPEED = 3
POWERUP_SPAWN_CHANCE = 0.1  # 10% chance per asteroid destroyed
POWERUP_DURATION = 300  # 5 seconds at 60 FPS
SHIELD_DURATION = 600  # 10 seconds

# Star settings
NUM_STARS = 200
STAR_MIN_SIZE = 1
STAR_MAX_SIZE = 3
STAR_MIN_SPEED = 0.1
STAR_MAX_SPEED = 0.5
STAR_MIN_BRIGHTNESS = 150
STAR_MAX_BRIGHTNESS = 255

# Explosion settings
EXPLOSION_MAX_SIZE = 20
EXPLOSION_INITIAL_SIZE = 10

# Combo settings
COMBO_TIMEOUT = 120  # 2 seconds to maintain combo
COMBO_MULTIPLIERS = [1, 2, 3, 5, 8]  # Score multipliers for combo levels

# Screen shake settings
SCREEN_SHAKE_DURATION = 10
SCREEN_SHAKE_INTENSITY = 8

# High score file
HIGH_SCORE_FILE = "high_score.txt"
MAX_NAME_LENGTH = 15


# =============================================================================
# CLASSES
# =============================================================================

class Ship:
    """Player-controlled spaceship."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = SHIP_WIDTH
        self.height = SHIP_HEIGHT
        self.speed = SHIP_SPEED
        self.lives = MAX_LIVES
        self.invulnerable = False
        self.invulnerability_timer = 0
        self.damage_flash_timer = 0
        self.has_shield = False
        self.shield_timer = 0

    def update(self, keys):
        """Update ship position based on keyboard input."""
        if keys[pygame.K_w] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_s] and self.y < HEIGHT - self.height:
            self.y += self.speed
        if keys[pygame.K_a] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_d] and self.x < WIDTH - self.width:
            self.x += self.speed

        # Update timers
        if self.invulnerability_timer > 0:
            self.invulnerability_timer -= 1
            if self.invulnerability_timer == 0:
                self.invulnerable = False

        if self.damage_flash_timer > 0:
            self.damage_flash_timer -= 1

        if self.shield_timer > 0:
            self.shield_timer -= 1
            if self.shield_timer == 0:
                self.has_shield = False

    def draw(self, screen):
        """Draw the ship."""
        # Flickering effect when invulnerable
        if self.invulnerable and pygame.time.get_ticks() % 200 < 100:
            return

        # Choose ship color (red flash when damaged)
        ship_color = SHIP_DAMAGE_COLOR if self.damage_flash_timer > 0 else SHIP_COLOR

        # Main ship body (oriented to point east)
        pygame.draw.polygon(screen, ship_color, [
            (self.x + self.width, self.y),
            (self.x, self.y - self.height // 2),
            (self.x, self.y + self.height // 2)
        ])

        # Ship cockpit
        pygame.draw.circle(screen, SHIP_COCKPIT_COLOR,
                          (self.x + self.width // 4, self.y),
                          self.width // 3)

        # Ship wings
        pygame.draw.polygon(screen, SHIP_WING_COLOR, [
            (self.x + self.width // 2, self.y - self.height),
            (self.x, self.y - self.height // 2),
            (self.x + self.width // 2, self.y)
        ])

        pygame.draw.polygon(screen, SHIP_WING_COLOR, [
            (self.x + self.width // 2, self.y + self.height),
            (self.x, self.y + self.height // 2),
            (self.x + self.width // 2, self.y)
        ])

        # Draw shield if active
        if self.has_shield:
            shield_radius = max(self.width, self.height)
            for i in range(3):
                alpha = 100 - i * 30
                s = pygame.Surface((shield_radius * 2, shield_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*SHIELD_COLOR, alpha),
                                 (shield_radius, shield_radius),
                                 shield_radius - i * 5, 2)
                screen.blit(s, (int(self.x - shield_radius + self.width // 2),
                               int(self.y - shield_radius)))

    def get_center(self):
        """Return the center point of the ship."""
        return (self.x + self.width // 2, self.y)

    def take_damage(self):
        """Handle taking damage."""
        if self.invulnerable:
            return False

        if self.has_shield:
            # Shield absorbs hit
            self.has_shield = False
            self.shield_timer = 0
            return False

        self.lives -= 1
        self.damage_flash_timer = DAMAGE_FLASH_FRAMES
        if self.lives > 0:
            # Grant temporary invulnerability
            self.invulnerable = True
            self.invulnerability_timer = INVULNERABILITY_FRAMES
            return False
        return True  # Game over


class Asteroid:
    """Asteroid obstacle."""

    def __init__(self, x, y, radius, speed_multiplier=1.0):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = ASTEROID_BASE_SPEED * speed_multiplier
        self.points = max(1, int(radius / 10))  # Larger asteroids worth more points

    def update(self):
        """Move asteroid to the left."""
        self.x -= self.speed

    def draw(self, screen):
        """Draw the asteroid with details."""
        # Main asteroid body
        pygame.draw.circle(screen, ASTEROID_COLORS[0], (int(self.x), int(self.y)), self.radius)

        # Add details to make it look realistic
        pygame.draw.circle(screen, ASTEROID_COLORS[1],
                          (int(self.x - self.radius // 3), int(self.y - self.radius // 4)),
                          self.radius // 2)
        pygame.draw.circle(screen, ASTEROID_COLORS[2],
                          (int(self.x + self.radius // 2), int(self.y + self.radius // 3)),
                          self.radius // 3)
        pygame.draw.circle(screen, ASTEROID_COLORS[1],
                          (int(self.x - self.radius // 2), int(self.y + self.radius // 2)),
                          self.radius // 4)

        # Add craters
        pygame.draw.circle(screen, ASTEROID_COLORS[2],
                          (int(self.x - self.radius // 4), int(self.y)),
                          self.radius // 6)
        pygame.draw.circle(screen, ASTEROID_COLORS[2],
                          (int(self.x + self.radius // 3), int(self.y - self.radius // 3)),
                          self.radius // 8)
        pygame.draw.circle(screen, ASTEROID_COLORS[2],
                          (int(self.x - self.radius // 2), int(self.y + self.radius // 4)),
                          self.radius // 5)

    def is_off_screen(self):
        """Check if asteroid is completely off-screen."""
        return self.x < -self.radius

    def collides_with_ship(self, ship):
        """Check collision with ship using circular collision detection."""
        ship_center = ship.get_center()
        distance_squared = (ship_center[0] - self.x) ** 2 + (ship_center[1] - self.y) ** 2
        collision_radius = self.radius + ship.width // 2
        return distance_squared < collision_radius ** 2


class Laser:
    """Laser projectile fired by the ship."""

    def __init__(self, x, y, angle=0):
        self.x = x
        self.y = y
        self.width = LASER_WIDTH
        self.height = LASER_HEIGHT
        self.speed = LASER_BASE_SPEED
        self.angle = angle  # For spread shot
        # Calculate velocity based on angle
        self.vx = self.speed * math.cos(math.radians(angle))
        self.vy = self.speed * math.sin(math.radians(angle))

    def update(self):
        """Move laser."""
        self.x += self.vx
        self.y += self.vy

    def draw(self, screen):
        """Draw the laser with glow effect."""
        pygame.draw.rect(screen, LASER_COLOR,
                        (int(self.x), int(self.y - 3), self.width, self.height))
        pygame.draw.rect(screen, LASER_GLOW_COLOR,
                        (int(self.x), int(self.y - 2), self.width, 4))

    def is_off_screen(self):
        """Check if laser is off-screen."""
        return self.x > WIDTH or self.x < 0 or self.y > HEIGHT or self.y < 0

    def collides_with_asteroid(self, asteroid):
        """Check collision with asteroid using rectangle-circle collision."""
        return (self.x < asteroid.x + asteroid.radius and
                self.x + self.width > asteroid.x - asteroid.radius and
                self.y < asteroid.y + asteroid.radius and
                self.y + self.height > asteroid.y - asteroid.radius)


class PowerUp:
    """Power-up collectible."""

    def __init__(self, x, y, powerup_type):
        self.x = x
        self.y = y
        self.size = POWERUP_SIZE
        self.speed = POWERUP_SPEED
        self.type = powerup_type
        self.color = POWERUP_COLORS.get(powerup_type, (255, 255, 255))

    def update(self):
        """Move power-up to the left."""
        self.x -= self.speed

    def draw(self, screen):
        """Draw the power-up."""
        # Draw rotating square
        angle = pygame.time.get_ticks() / 10
        points = []
        for i in range(4):
            rad = math.radians(angle + i * 90)
            px = self.x + math.cos(rad) * self.size
            py = self.y + math.sin(rad) * self.size
            points.append((px, py))
        pygame.draw.polygon(screen, self.color, points)
        pygame.draw.polygon(screen, (255, 255, 255), points, 2)

        # Draw icon letter
        font = pygame.font.SysFont(None, 20)
        letter = self.type[0].upper()
        text = font.render(letter, True, (0, 0, 0))
        screen.blit(text, (self.x - text.get_width() // 2, self.y - text.get_height() // 2))

    def is_off_screen(self):
        """Check if power-up is off-screen."""
        return self.x < -self.size

    def collides_with_ship(self, ship):
        """Check collision with ship."""
        ship_center = ship.get_center()
        distance_squared = (ship_center[0] - self.x) ** 2 + (ship_center[1] - self.y) ** 2
        collision_radius = self.size + ship.width // 2
        return distance_squared < collision_radius ** 2


class Explosion:
    """Explosion animation effect."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = EXPLOSION_INITIAL_SIZE
        self.max_size = EXPLOSION_MAX_SIZE

    def update(self):
        """Grow the explosion."""
        self.size += 1

    def draw(self, screen):
        """Draw explosion with alpha transparency."""
        for i in range(5):
            radius = int(self.size * (i + 1) / 5)
            alpha = max(0, 255 - self.size * 10 - i * 30)
            if radius > 0 and alpha > 0:
                s = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                color_with_alpha = (*EXPLOSION_COLORS[i % 3], alpha)
                pygame.draw.circle(s, color_with_alpha, (radius, radius), radius)
                screen.blit(s, (int(self.x - radius), int(self.y - radius)))

    def is_finished(self):
        """Check if explosion animation is complete."""
        return self.size >= self.max_size


class Star:
    """Background star for parallax effect."""

    def __init__(self, x, y, size, speed, brightness, color):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.brightness = brightness
        self.color = color

    def update(self, paused=False):
        """Move star to create parallax effect."""
        if not paused:
            self.x -= self.speed
            if self.x < -5:
                self.x = WIDTH + 5
                self.y = random.randint(0, HEIGHT)

    def draw(self, screen):
        """Draw the star."""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)


class Game:
    """Main game controller."""

    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Ship Obstacle Avoidance - Enhanced")
        self.clock = pygame.time.Clock()

        # Fonts
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)

        # Game state
        self.running = True
        self.game_over = False
        self.paused = False
        self.score = 0
        self.high_score = 0
        self.high_score_player = ""
        self.player_name = ""
        self.name_input_active = False

        # Game objects
        self.ship = Ship(SHIP_START_X, SHIP_START_Y)
        self.asteroids = []
        self.lasers = []
        self.explosions = []
        self.stars = []
        self.powerups = []

        # Timers and counters
        self.laser_cooldown = 0
        self.asteroid_spawn_timer = 0
        self.difficulty_timer = 0
        self.difficulty_level = 1.0

        # Combo system
        self.combo = 0
        self.combo_timer = 0

        # Power-up states
        self.rapid_fire_active = False
        self.rapid_fire_timer = 0
        self.spread_shot_active = False
        self.spread_shot_timer = 0

        # Screen shake
        self.screen_shake = 0
        self.shake_offset_x = 0
        self.shake_offset_y = 0

        # Sound effects (would need actual sound files)
        self.sounds_enabled = False
        self.init_sounds()

        # Initialize game
        self.load_high_score()
        self.create_stars()
        self.create_initial_asteroids()

    def init_sounds(self):
        """Initialize sound effects (requires sound files)."""
        try:
            # Placeholder - would need actual .wav or .ogg files
            # self.laser_sound = pygame.mixer.Sound("sounds/laser.wav")
            # self.explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")
            # self.hit_sound = pygame.mixer.Sound("sounds/hit.wav")
            # self.powerup_sound = pygame.mixer.Sound("sounds/powerup.wav")
            # pygame.mixer.music.load("sounds/background.ogg")
            # pygame.mixer.music.play(-1)
            pass
        except:
            self.sounds_enabled = False

    def play_sound(self, sound_name):
        """Play a sound effect."""
        if self.sounds_enabled:
            pass  # Would play actual sounds here

    def load_high_score(self):
        """Load high score from file."""
        if os.path.exists(HIGH_SCORE_FILE):
            try:
                with open(HIGH_SCORE_FILE, "r") as f:
                    content = f.read().strip()
                    if content:
                        parts = content.split(":", 1)
                        if len(parts) == 2:
                            self.high_score = int(parts[0])
                            self.high_score_player = parts[1]
                        else:
                            self.high_score = int(content)
            except:
                self.high_score = 0

    def save_high_score(self):
        """Save high score to file."""
        try:
            with open(HIGH_SCORE_FILE, "w") as f:
                f.write(f"{self.score}:{self.player_name}")
            self.high_score = self.score
            self.high_score_player = self.player_name
        except:
            pass

    def create_stars(self):
        """Create star background."""
        for _ in range(NUM_STARS):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            size = random.randint(STAR_MIN_SIZE, STAR_MAX_SIZE)
            speed = random.uniform(STAR_MIN_SPEED, STAR_MAX_SPEED)
            brightness = random.randint(STAR_MIN_BRIGHTNESS, STAR_MAX_BRIGHTNESS)
            color = random.choice(STAR_COLORS)
            self.stars.append(Star(x, y, size, speed, brightness, color))

    def create_initial_asteroids(self):
        """Create initial set of asteroids."""
        for i in range(5):
            x = WIDTH + i * 300
            y = random.randint(0, HEIGHT - 100)
            radius = random.randint(ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS)
            self.asteroids.append(Asteroid(x, y, radius, self.difficulty_level))

    def reset(self):
        """Reset game state for new game."""
        self.ship = Ship(SHIP_START_X, SHIP_START_Y)
        self.asteroids = []
        self.lasers = []
        self.explosions = []
        self.powerups = []
        self.score = 0
        self.game_over = False
        self.paused = False
        self.player_name = ""
        self.name_input_active = False
        self.laser_cooldown = 0
        self.asteroid_spawn_timer = 0
        self.difficulty_timer = 0
        self.difficulty_level = 1.0
        self.combo = 0
        self.combo_timer = 0
        self.rapid_fire_active = False
        self.rapid_fire_timer = 0
        self.spread_shot_active = False
        self.spread_shot_timer = 0
        self.screen_shake = 0
        self.create_initial_asteroids()

    def handle_events(self):
        """Process pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                # Pause game
                if event.key == pygame.K_p and not self.game_over:
                    self.paused = not self.paused

                # Restart game
                if event.key == pygame.K_r and self.game_over:
                    self.reset()

                # Shoot laser
                elif event.key == pygame.K_SPACE and not self.game_over and not self.paused and self.laser_cooldown == 0:
                    self.shoot_laser()

                # Submit name
                elif event.key == pygame.K_RETURN and self.game_over and self.name_input_active:
                    self.name_input_active = False
                    if self.score > self.high_score:
                        self.save_high_score()

                # Backspace in name entry
                elif event.key == pygame.K_BACKSPACE and self.game_over and self.name_input_active:
                    self.player_name = self.player_name[:-1]

                # Exit game
                elif event.key == pygame.K_ESCAPE and self.game_over:
                    self.running = False

                # Type name
                elif self.game_over and self.name_input_active and len(self.player_name) < MAX_NAME_LENGTH and event.unicode.isprintable():
                    self.player_name += event.unicode

    def shoot_laser(self):
        """Fire laser(s) based on current power-ups."""
        cooldown = RAPID_FIRE_COOLDOWN if self.rapid_fire_active else LASER_COOLDOWN_FRAMES

        if self.spread_shot_active:
            # Shoot 3 lasers in a spread
            for angle in [-SPREAD_SHOT_ANGLE, 0, SPREAD_SHOT_ANGLE]:
                laser = Laser(self.ship.x + self.ship.width, self.ship.y, angle)
                self.lasers.append(laser)
        else:
            # Shoot single laser
            laser = Laser(self.ship.x + self.ship.width, self.ship.y)
            self.lasers.append(laser)

        self.laser_cooldown = cooldown
        self.play_sound('laser')

    def spawn_powerup(self, x, y):
        """Spawn a random power-up."""
        if random.random() < POWERUP_SPAWN_CHANCE:
            powerup_type = random.choice(['shield', 'rapid_fire', 'spread_shot'])
            self.powerups.append(PowerUp(x, y, powerup_type))

    def activate_powerup(self, powerup_type):
        """Activate a power-up effect."""
        if powerup_type == 'shield':
            self.ship.has_shield = True
            self.ship.shield_timer = SHIELD_DURATION
        elif powerup_type == 'rapid_fire':
            self.rapid_fire_active = True
            self.rapid_fire_timer = POWERUP_DURATION
        elif powerup_type == 'spread_shot':
            self.spread_shot_active = True
            self.spread_shot_timer = POWERUP_DURATION
        self.play_sound('powerup')

    def update(self):
        """Update all game objects."""
        if self.game_over:
            # Check if we should activate name input
            if not self.name_input_active and self.score > self.high_score:
                self.name_input_active = True
                self.player_name = ""
            return

        if self.paused:
            return

        # Update difficulty
        self.difficulty_timer += 1
        if self.difficulty_timer % DIFFICULTY_INCREASE_INTERVAL == 0:
            self.difficulty_level = min(3.0, self.difficulty_level + 0.1)

        # Update ship
        keys = pygame.key.get_pressed()
        self.ship.update(keys)

        # Update laser cooldown
        if self.laser_cooldown > 0:
            self.laser_cooldown -= 1

        # Update power-up timers
        if self.rapid_fire_timer > 0:
            self.rapid_fire_timer -= 1
            if self.rapid_fire_timer == 0:
                self.rapid_fire_active = False

        if self.spread_shot_timer > 0:
            self.spread_shot_timer -= 1
            if self.spread_shot_timer == 0:
                self.spread_shot_active = False

        # Update combo timer
        if self.combo_timer > 0:
            self.combo_timer -= 1
            if self.combo_timer == 0:
                self.combo = 0

        # Update lasers
        for laser in self.lasers:
            laser.update()
        self.lasers = [laser for laser in self.lasers if not laser.is_off_screen()]

        # Update asteroids
        for asteroid in self.asteroids:
            asteroid.update()
        self.asteroids = [asteroid for asteroid in self.asteroids if not asteroid.is_off_screen()]

        # Update power-ups
        for powerup in self.powerups:
            powerup.update()
        self.powerups = [powerup for powerup in self.powerups if not powerup.is_off_screen()]

        # Spawn new asteroids
        self.asteroid_spawn_timer += 1
        spawn_freq = max(30, int(ASTEROID_SPAWN_FREQUENCY / self.difficulty_level))
        if len(self.asteroids) < MAX_ASTEROIDS and self.asteroid_spawn_timer >= spawn_freq:
            if random.randint(1, spawn_freq) == 1:
                y = random.randint(0, HEIGHT - 100)
                radius = random.randint(ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS)
                self.asteroids.append(Asteroid(WIDTH, y, radius, self.difficulty_level))
                self.asteroid_spawn_timer = 0

        # Update explosions
        for explosion in self.explosions:
            explosion.update()
        self.explosions = [explosion for explosion in self.explosions if not explosion.is_finished()]

        # Update stars
        for star in self.stars:
            star.update(self.paused)

        # Update screen shake
        if self.screen_shake > 0:
            self.screen_shake -= 1
            self.shake_offset_x = random.randint(-SCREEN_SHAKE_INTENSITY, SCREEN_SHAKE_INTENSITY)
            self.shake_offset_y = random.randint(-SCREEN_SHAKE_INTENSITY, SCREEN_SHAKE_INTENSITY)
        else:
            self.shake_offset_x = 0
            self.shake_offset_y = 0

        # Check collisions
        self.check_collisions()

    def check_collisions(self):
        """Check all collision scenarios."""
        # Laser-asteroid collisions
        lasers_to_remove = []
        asteroids_to_remove = []

        for i, laser in enumerate(self.lasers):
            for j, asteroid in enumerate(self.asteroids):
                if laser.collides_with_asteroid(asteroid):
                    if i not in lasers_to_remove:
                        lasers_to_remove.append(i)
                    if j not in asteroids_to_remove:
                        asteroids_to_remove.append(j)
                        # Create explosion
                        self.explosions.append(Explosion(asteroid.x, asteroid.y))
                        # Update combo
                        self.combo += 1
                        self.combo_timer = COMBO_TIMEOUT
                        # Calculate score with combo multiplier
                        multiplier_index = min(self.combo - 1, len(COMBO_MULTIPLIERS) - 1)
                        multiplier = COMBO_MULTIPLIERS[multiplier_index]
                        self.score += asteroid.points * multiplier
                        # Spawn power-up chance
                        self.spawn_powerup(asteroid.x, asteroid.y)
                        self.play_sound('explosion')

        # Remove collided objects
        self.lasers = [laser for i, laser in enumerate(self.lasers) if i not in lasers_to_remove]
        self.asteroids = [asteroid for i, asteroid in enumerate(self.asteroids) if i not in asteroids_to_remove]

        # Ship-asteroid collisions
        for asteroid in self.asteroids:
            if asteroid.collides_with_ship(self.ship):
                if self.ship.take_damage():
                    self.game_over = True
                else:
                    # Screen shake on hit
                    self.screen_shake = SCREEN_SHAKE_DURATION
                    self.play_sound('hit')
                    # Remove the asteroid
                    self.asteroids.remove(asteroid)
                    self.explosions.append(Explosion(asteroid.x, asteroid.y))
                    # Reset combo
                    self.combo = 0
                    self.combo_timer = 0
                break

        # Ship-powerup collisions
        for powerup in self.powerups:
            if powerup.collides_with_ship(self.ship):
                self.activate_powerup(powerup.type)
                self.powerups.remove(powerup)

    def draw(self):
        """Draw all game objects and UI."""
        # Create offset surface for screen shake
        offset_screen = pygame.Surface((WIDTH, HEIGHT))
        offset_screen.fill(BACKGROUND)

        # Draw stars
        for star in self.stars:
            star.draw(offset_screen)

        # Draw explosions
        for explosion in self.explosions:
            explosion.draw(offset_screen)

        # Draw asteroids
        for asteroid in self.asteroids:
            asteroid.draw(offset_screen)

        # Draw power-ups
        for powerup in self.powerups:
            powerup.draw(offset_screen)

        # Draw lasers
        for laser in self.lasers:
            laser.draw(offset_screen)

        # Draw ship
        self.ship.draw(offset_screen)

        # Draw UI
        self.draw_ui(offset_screen)

        # Draw pause screen
        if self.paused:
            self.draw_pause(offset_screen)

        # Draw game over screen
        if self.game_over:
            self.draw_game_over(offset_screen)

        # Blit offset screen with shake
        self.screen.blit(offset_screen, (self.shake_offset_x, self.shake_offset_y))

        # Update display
        pygame.display.flip()

    def draw_ui(self, screen):
        """Draw score and UI elements."""
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
        screen.blit(score_text, (20, 20))

        # Draw high score
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, TEXT_COLOR)
        screen.blit(high_score_text, (WIDTH - high_score_text.get_width() - 20, 20))

        # Draw high score player name
        if self.high_score_player:
            player_text = self.small_font.render(f"By: {self.high_score_player}", True, TEXT_COLOR)
            screen.blit(player_text, (WIDTH - player_text.get_width() - 20, 50))

        # Draw lives
        lives_text = self.font.render(f"Lives: {self.ship.lives}", True, HEALTH_COLOR)
        screen.blit(lives_text, (20, 60))

        # Draw combo
        if self.combo > 1:
            multiplier_index = min(self.combo - 1, len(COMBO_MULTIPLIERS) - 1)
            multiplier = COMBO_MULTIPLIERS[multiplier_index]
            combo_text = self.font.render(f"COMBO x{multiplier}!", True, COMBO_COLOR)
            screen.blit(combo_text, (WIDTH // 2 - combo_text.get_width() // 2, 20))

        # Draw active power-ups
        y_offset = 100
        if self.rapid_fire_active:
            rf_text = self.small_font.render(f"Rapid Fire: {self.rapid_fire_timer // FPS}s", True, POWERUP_COLORS['rapid_fire'])
            screen.blit(rf_text, (20, y_offset))
            y_offset += 30

        if self.spread_shot_active:
            ss_text = self.small_font.render(f"Spread Shot: {self.spread_shot_timer // FPS}s", True, POWERUP_COLORS['spread_shot'])
            screen.blit(ss_text, (20, y_offset))
            y_offset += 30

        if self.ship.has_shield:
            shield_text = self.small_font.render(f"Shield: {self.ship.shield_timer // FPS}s", True, POWERUP_COLORS['shield'])
            screen.blit(shield_text, (20, y_offset))

        # Draw controls
        controls_text = self.small_font.render("WASD: Move | SPACE: Shoot | P: Pause", True, TEXT_COLOR)
        screen.blit(controls_text, (20, HEIGHT - 40))

    def draw_pause(self, screen):
        """Draw pause overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))

        # Pause text
        pause_text = self.font.render("PAUSED", True, PAUSE_COLOR)
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 50))

        # Instructions
        resume_text = self.small_font.render("Press P to resume", True, TEXT_COLOR)
        screen.blit(resume_text, (WIDTH // 2 - resume_text.get_width() // 2, HEIGHT // 2 + 10))

    def draw_game_over(self, screen):
        """Draw game over screen with name input."""
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # Game over message
        game_over_text = self.font.render("GAME OVER!", True, GAME_OVER_COLOR)
        screen.blit(game_over_text,
                    (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 80))

        # Final score
        final_score_text = self.font.render(f"Final Score: {self.score}", True, TEXT_COLOR)
        screen.blit(final_score_text,
                    (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 - 30))

        # Name input for new high score
        if self.name_input_active:
            prompt_text = self.font.render("New High Score! Enter your name:", True, TEXT_COLOR)
            screen.blit(prompt_text,
                       (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2 + 20))

            # Name input field
            pygame.draw.rect(screen, (50, 50, 100),
                           (WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 40))
            name_display = self.small_font.render(self.player_name, True, TEXT_COLOR)
            screen.blit(name_display, (WIDTH // 2 - 100 + 10, HEIGHT // 2 + 65))

            # Blinking cursor
            if pygame.time.get_ticks() % 1000 < 500:
                cursor_x = WIDTH // 2 - 100 + 10 + name_display.get_width()
                pygame.draw.line(screen, TEXT_COLOR,
                               (cursor_x, HEIGHT // 2 + 65),
                               (cursor_x, HEIGHT // 2 + 95), 2)

            # Instructions
            enter_text = self.small_font.render("Press ENTER to save", True, TEXT_COLOR)
            screen.blit(enter_text,
                       (WIDTH // 2 - enter_text.get_width() // 2, HEIGHT // 2 + 110))
        else:
            # Instructions
            if self.score > self.high_score:
                prompt_text = self.font.render("New High Score!", True, TEXT_COLOR)
                screen.blit(prompt_text,
                           (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2 + 20))
            else:
                restart_text = self.font.render("Press R to restart", True, TEXT_COLOR)
                screen.blit(restart_text,
                           (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))

                # Show high score info
                if self.high_score_player:
                    hs_text = self.small_font.render(
                        f"High Score: {self.high_score} by {self.high_score_player}",
                        True, TEXT_COLOR)
                    screen.blit(hs_text,
                               (WIDTH // 2 - hs_text.get_width() // 2, HEIGHT // 2 + 60))

            # Exit instructions
            exit_text = self.small_font.render("Press ESC to exit", True, TEXT_COLOR)
            screen.blit(exit_text,
                       (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 110))

    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    game = Game()
    game.run()
