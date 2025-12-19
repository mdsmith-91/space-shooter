import pygame
import random
import sys
import os
import math

# Initialize pygame
pygame.init()


# =============================================================================
# RESOURCE PATH HELPER (for PyInstaller bundled executables)
# =============================================================================

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Running in development mode
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

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
    "shield": (100, 255, 100),
    "rapid_fire": (255, 255, 100),
    "spread_shot": (255, 150, 255),
    "double_damage": (255, 100, 200),
    "magnet": (200, 100, 255),
    "time_slow": (100, 200, 255),
    "nuke": (255, 50, 50),
}
SHIELD_COLOR = (100, 255, 100)
HEALTH_COLOR = (255, 100, 100)
COMBO_COLOR = (255, 255, 100)

# Particle colors
PARTICLE_COLORS = {
    "laser": [(0, 255, 255), (100, 255, 255), (150, 255, 255)],
    "debris": [(150, 150, 150), (180, 180, 180), (120, 120, 120)],
    "engine": [(255, 150, 50), (255, 200, 100), (255, 100, 20)],
    "powerup": [(255, 255, 100), (255, 200, 255), (200, 255, 255)],
    "impact": [(255, 255, 255), (255, 200, 100), (255, 150, 50)],
}

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
POWERUP_DURATION = 420  # 7 seconds at 60 FPS (increased for better value)
SHIELD_DURATION = 600  # 10 seconds
TIME_SLOW_MULTIPLIER = 0.5  # Asteroids move at 50% speed when time slow is active
MAGNET_PULL_SPEED = 3  # Speed at which magnet pulls power-ups toward ship
NUKE_BOSS_DAMAGE = 3  # Damage dealt to boss by nuke power-up

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
BOSS_EXPLOSION_MAX_SIZE = 60
BOSS_EXPLOSION_DURATION = 60  # frames

# Boss settings
BOSS_RADIUS = 80
BOSS_HEALTH = 15
BOSS_SPEED = 2
BOSS_SPAWN_INTERVAL = 2500  # Every 2500 points
BOSS_COLOR = (200, 50, 50)
BOSS_DETAIL_COLOR = (150, 30, 30)
BOSS_GLOW_COLOR = (255, 100, 100)
BOSS_HEALTHBAR_WIDTH = 400
BOSS_HEALTHBAR_HEIGHT = 20
BOSS_WARNING_DURATION = 180  # 3 seconds at 60 FPS

# Combo settings
COMBO_TIMEOUT = 120  # 2 seconds to maintain combo
COMBO_MULTIPLIERS = [1, 2, 3, 5, 8, 10]  # Score multipliers for combo levels

# Particle settings
PARTICLE_LIFETIME = 30  # frames
PARTICLE_MIN_SIZE = 1
PARTICLE_MAX_SIZE = 4
PARTICLE_FADE_RATE = 8  # alpha decrease per frame

# Screen shake settings
SCREEN_SHAKE_DURATION = 10
SCREEN_SHAKE_INTENSITY = 8

# High score file
DATA_DIR = "data"
HIGH_SCORE_FILE = os.path.join(DATA_DIR, "high_score.txt")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.txt")
MAX_NAME_LENGTH = 15

# Score popup settings
SCORE_POPUP_LIFETIME = 60  # 1 second
SCORE_POPUP_RISE_SPEED = -1.5

# Nebula settings
NEBULA_COUNT = 5
NEBULA_MIN_SIZE = 100
NEBULA_MAX_SIZE = 300
NEBULA_COLORS = [(50, 20, 80, 80), (20, 50, 80, 80), (80, 20, 50, 80)]  # RGBA with alpha

# Distortion wave settings
DISTORTION_MAX_RADIUS = 400
DISTORTION_LIFETIME = 60

# UI animation settings
COMBO_PULSE_SPEED = 10
SCAN_LINE_SPEED = 2

# Color theme thresholds
THEME_BLUE_MAX = 1000
THEME_PURPLE_MAX = 5000
THEME_RED_MIN = 5000

# Hexagon shield settings
HEXAGON_RADIUS = 15
HEXAGON_LAYERS = 3

# Laser trail settings
LASER_TRAIL_LENGTH = 5  # Number of trail segments

# Asteroid motion blur settings
MOTION_BLUR_POSITIONS = 3  # Number of ghost images

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
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.y > 0:
            self.y -= self.speed
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.y < HEIGHT - self.height:
            self.y += self.speed
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.x > 0:
            self.x -= self.speed
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.x < WIDTH - self.width:
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
        """Draw the ship with enhanced graphics and details."""
        # Flickering effect when invulnerable
        if self.invulnerable and pygame.time.get_ticks() % 200 < 100:
            return

        # Choose ship color (red flash when damaged)
        is_damaged = self.damage_flash_timer > 0
        base_color = SHIP_DAMAGE_COLOR if is_damaged else SHIP_COLOR

        # Draw ship glow/aura (subtle outer glow)
        glow_surface = pygame.Surface((self.width * 2, self.height * 2), pygame.SRCALPHA)
        glow_radius = max(self.width, self.height) // 2
        for i in range(3):
            alpha = 20 - i * 7
            glow_color = (*base_color, alpha)
            pygame.draw.ellipse(
                glow_surface,
                glow_color,
                (self.width // 2 - glow_radius - i * 3, self.height - glow_radius - i * 3,
                 glow_radius * 2 + i * 6, glow_radius * 2 + i * 6)
            )
        screen.blit(glow_surface, (int(self.x - self.width // 2), int(self.y - self.height)))

        # Draw engine thrusters at the back (left side)
        thruster_width = 8
        thruster_height = 5
        # Top thruster
        pygame.draw.rect(screen, (50, 50, 60),
                        (self.x - 2, self.y - self.height // 2 - 2, thruster_width, thruster_height))
        # Bottom thruster
        pygame.draw.rect(screen, (50, 50, 60),
                        (self.x - 2, self.y + self.height // 2 - 3, thruster_width, thruster_height))

        # Engine glow (animated)
        glow_pulse = (math.sin(pygame.time.get_ticks() / 100) + 1) / 2
        engine_glow = int(100 + glow_pulse * 100)
        engine_color = (100, 150, 255) if not is_damaged else (255, 150, 100)

        # Top engine glow
        for i in range(3):
            alpha = engine_glow - i * 30
            if alpha > 0:
                glow_surf = pygame.Surface((thruster_width + i * 2, thruster_height + i * 2), pygame.SRCALPHA)
                glow_surf.fill((*engine_color, alpha))
                screen.blit(glow_surf, (self.x - 2 - i, self.y - self.height // 2 - 2 - i))

        # Bottom engine glow
        for i in range(3):
            alpha = engine_glow - i * 30
            if alpha > 0:
                glow_surf = pygame.Surface((thruster_width + i * 2, thruster_height + i * 2), pygame.SRCALPHA)
                glow_surf.fill((*engine_color, alpha))
                screen.blit(glow_surf, (self.x - 2 - i, self.y + self.height // 2 - 3 - i))

        # Create gradient layers for main ship body with better shading
        for i in range(4):
            # Calculate gradient color (darker to lighter from bottom to top)
            blend_factor = (i + 1) / 5.0
            gradient_color = tuple(int(c * (0.5 + blend_factor * 0.5)) for c in base_color)

            # Offset each layer slightly for gradient effect
            offset_y = -2 + i * 0.7
            pygame.draw.polygon(
                screen,
                gradient_color,
                [
                    (self.x + self.width, self.y + offset_y),
                    (self.x, self.y - self.height // 2 + offset_y),
                    (self.x, self.y + self.height // 2 + offset_y),
                ],
            )

        # Add panel details (surface segments)
        panel_color = tuple(int(c * 0.7) for c in base_color)
        # Top panel
        pygame.draw.polygon(
            screen,
            panel_color,
            [
                (self.x + self.width * 0.6, self.y - 2),
                (self.x + self.width * 0.3, self.y - self.height // 4),
                (self.x + self.width * 0.5, self.y - self.height // 4),
            ]
        )
        # Bottom panel
        pygame.draw.polygon(
            screen,
            panel_color,
            [
                (self.x + self.width * 0.6, self.y + 2),
                (self.x + self.width * 0.3, self.y + self.height // 4),
                (self.x + self.width * 0.5, self.y + self.height // 4),
            ]
        )

        # Add metallic edge highlights
        highlight_color = (min(255, base_color[0] + 120), min(255, base_color[1] + 120), min(255, base_color[2] + 120))
        # Top edge
        pygame.draw.aalines(
            screen,
            highlight_color,
            False,
            [
                (self.x, self.y - self.height // 2),
                (self.x + self.width, self.y),
            ]
        )
        # Bottom edge (darker)
        shadow_color = tuple(int(c * 0.6) for c in base_color)
        pygame.draw.aalines(
            screen,
            shadow_color,
            False,
            [
                (self.x, self.y + self.height // 2),
                (self.x + self.width, self.y),
            ]
        )

        # Ship wings with gradient and details
        wing_color = SHIP_WING_COLOR if not is_damaged else tuple(int(c * 0.8) for c in SHIP_DAMAGE_COLOR)
        for i in range(2):
            blend = (i + 1) / 3.0
            wing_gradient = tuple(int(c * (0.6 + blend * 0.4)) for c in wing_color)

            # Top wing
            pygame.draw.polygon(
                screen,
                wing_gradient,
                [
                    (self.x + self.width // 2, self.y - self.height + i),
                    (self.x, self.y - self.height // 2 + i),
                    (self.x + self.width // 2, self.y + i),
                ],
            )
            # Wing detail line
            wing_detail_color = tuple(min(255, int(c * 1.2)) for c in wing_gradient)
            pygame.draw.aaline(
                screen,
                wing_detail_color,
                (self.x + self.width // 4, self.y - self.height * 0.75),
                (self.x + self.width // 2, self.y - self.height // 4)
            )

            # Bottom wing
            pygame.draw.polygon(
                screen,
                wing_gradient,
                [
                    (self.x + self.width // 2, self.y + self.height - i),
                    (self.x, self.y + self.height // 2 - i),
                    (self.x + self.width // 2, self.y - i),
                ],
            )
            # Wing detail line
            pygame.draw.aaline(
                screen,
                wing_detail_color,
                (self.x + self.width // 4, self.y + self.height * 0.75),
                (self.x + self.width // 2, self.y + self.height // 4)
            )

        # Ship cockpit with better shading
        cockpit_color = SHIP_COCKPIT_COLOR if not is_damaged else tuple(int(c * 0.9) for c in SHIP_DAMAGE_COLOR)

        # Main cockpit circle
        pygame.draw.circle(
            screen,
            cockpit_color,
            (self.x + self.width // 4, self.y),
            self.width // 3,
        )

        # Cockpit window/glass effect (lighter circle on top)
        window_color = (min(255, cockpit_color[0] + 100), min(255, cockpit_color[1] + 120), min(255, cockpit_color[2] + 150))
        pygame.draw.circle(
            screen,
            window_color,
            (self.x + self.width // 4, self.y - 2),
            self.width // 4,
        )

        # Add specular highlight on cockpit (bright reflection)
        highlight_offset = self.width // 6
        highlight_color = (255, 255, 255)
        pygame.draw.circle(
            screen,
            highlight_color,
            (self.x + self.width // 4 - highlight_offset // 2, self.y - highlight_offset),
            self.width // 8,
        )

        # Add small detail lights (blinking navigation lights)
        blink = pygame.time.get_ticks() % 1000 < 500
        if blink:
            # Top light
            pygame.draw.circle(screen, (100, 255, 100),
                             (self.x + self.width // 2, self.y - self.height // 3), 2)
            # Bottom light
            pygame.draw.circle(screen, (255, 100, 100),
                             (self.x + self.width // 2, self.y + self.height // 3), 2)

        # Weapon ports (where lasers fire from)
        weapon_color = (200, 200, 100) if not is_damaged else (255, 150, 100)
        pygame.draw.circle(screen, weapon_color, (self.x + self.width, self.y), 3)

        # Draw hexagonal shield pattern if active
        if self.has_shield:
            shield_radius = max(self.width, self.height)
            shield_surface = pygame.Surface((shield_radius * 2, shield_radius * 2), pygame.SRCALPHA)
            shield_center = (shield_radius, shield_radius)

            # Draw hexagonal pattern with multiple layers
            for layer in range(HEXAGON_LAYERS):
                layer_radius = shield_radius - layer * (shield_radius // HEXAGON_LAYERS)
                num_hexagons = max(1, 6 - layer * 2)  # Fewer hexagons in inner layers

                for hex_idx in range(num_hexagons):
                    # Position hexagons around the shield
                    angle = (360 / num_hexagons) * hex_idx + pygame.time.get_ticks() / 20
                    hex_x = shield_center[0] + layer_radius * 0.7 * math.cos(math.radians(angle))
                    hex_y = shield_center[1] + layer_radius * 0.7 * math.sin(math.radians(angle))

                    # Draw hexagon
                    hex_points = []
                    for i in range(6):
                        point_angle = angle + i * 60
                        px = hex_x + HEXAGON_RADIUS * math.cos(math.radians(point_angle))
                        py = hex_y + HEXAGON_RADIUS * math.sin(math.radians(point_angle))
                        hex_points.append((int(px), int(py)))

                    # Pulsing alpha effect
                    pulse = (math.sin(pygame.time.get_ticks() / 200.0) + 1) / 2
                    alpha = int((60 + pulse * 40) * (1.0 - layer * 0.2))
                    hex_color = (*SHIELD_COLOR, alpha)

                    pygame.draw.polygon(shield_surface, hex_color, hex_points, 2)

            screen.blit(
                shield_surface,
                (
                    int(self.x - shield_radius + self.width // 2),
                    int(self.y - shield_radius),
                ),
            )

    def get_center(self):
        """Return the center point of the ship."""
        return (self.x + self.width // 2, self.y)

    def take_damage(self):
        """Handle taking damage. Returns (game_over, shield_absorbed) tuple."""
        if self.invulnerable:
            return False, False

        if self.has_shield:
            # Shield absorbs hit
            self.has_shield = False
            self.shield_timer = 0
            return False, True  # Shield absorbed the hit

        self.lives -= 1
        self.damage_flash_timer = DAMAGE_FLASH_FRAMES
        if self.lives > 0:
            # Grant temporary invulnerability
            self.invulnerable = True
            self.invulnerability_timer = INVULNERABILITY_FRAMES
            return False, False
        return True, False  # Game over


class Asteroid:
    """Asteroid obstacle."""

    def __init__(
        self, x, y, radius, speed_multiplier=1.0, velocity_x=None, velocity_y=None
    ):
        self.x = x
        self.y = y
        self.radius = radius
        self.base_speed = ASTEROID_BASE_SPEED * speed_multiplier
        # Allow custom velocity for child asteroids
        self.velocity_x = velocity_x if velocity_x is not None else -self.base_speed
        self.velocity_y = velocity_y if velocity_y is not None else 0
        self.points = max(10, int(radius / 2))  # Large=25pts, Medium=15pts, Small=10pts

        # Determine size category for breaking mechanics
        if radius >= 40:
            self.size_category = "large"
        elif radius >= 25:
            self.size_category = "medium"
        else:
            self.size_category = "small"

        # Rotation
        self.angle = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-2, 2)  # degrees per frame

        # Motion blur tracking
        self.previous_positions = []  # List of (x, y) positions for motion blur

        # Rock type determines color scheme
        rock_types = [
            [(120, 120, 120), (140, 140, 140), (100, 100, 100)],  # Gray stone
            [(140, 130, 110), (160, 150, 130), (120, 110, 90)],   # Brown rock
            [(100, 110, 120), (120, 130, 140), (80, 90, 100)],    # Blue-gray
            [(130, 115, 100), (150, 135, 120), (110, 95, 80)],    # Tan/beige
        ]
        self.colors = random.choice(rock_types)

        # Generate irregular shape (polygon instead of perfect circle)
        self.shape_points = []
        num_points = random.randint(8, 12)
        for i in range(num_points):
            angle_deg = (360 / num_points) * i + random.uniform(-15, 15)
            distance = self.radius * random.uniform(0.8, 1.1)  # Irregular distance
            self.shape_points.append((angle_deg, distance))

        # Generate random crack patterns for visual variety
        self.cracks = []
        num_cracks = random.randint(3, 6)
        for _ in range(num_cracks):
            # Random crack from center to edge
            angle_offset = random.uniform(0, 360)
            start_dist = random.uniform(0, self.radius * 0.4)
            end_dist = random.uniform(self.radius * 0.6, self.radius * 0.95)
            width = random.randint(1, 2)
            self.cracks.append((angle_offset, start_dist, end_dist, width))

        # Generate surface features (craters, ridges)
        self.craters = []
        num_craters = random.randint(3, 6)
        for _ in range(num_craters):
            crater_angle = random.uniform(0, 360)
            crater_dist = random.uniform(0, self.radius * 0.6)
            crater_size = random.uniform(self.radius * 0.1, self.radius * 0.3)
            self.craters.append((crater_angle, crater_dist, crater_size))

        # Some asteroids have mineral sparkles
        self.has_minerals = random.random() < 0.3  # 30% chance
        self.mineral_points = []
        if self.has_minerals:
            num_minerals = random.randint(3, 8)
            for _ in range(num_minerals):
                mineral_angle = random.uniform(0, 360)
                mineral_dist = random.uniform(0, self.radius * 0.8)
                mineral_brightness = random.randint(150, 255)
                self.mineral_points.append((mineral_angle, mineral_dist, mineral_brightness))

    def update(self, time_scale=1.0):
        """Move asteroid with custom velocity.

        Args:
            time_scale: Multiplier for movement speed (default 1.0, 0.5 for time slow)
        """
        # Store current position for motion blur
        self.previous_positions.append((self.x, self.y))
        if len(self.previous_positions) > MOTION_BLUR_POSITIONS:
            self.previous_positions.pop(0)

        self.x += self.velocity_x * time_scale
        self.y += self.velocity_y * time_scale
        self.angle += self.rotation_speed * time_scale
        if self.angle >= 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360

    def _rotate_point(self, offset_x, offset_y):
        """Rotate a point around the asteroid center based on current angle."""
        angle_rad = math.radians(self.angle)
        rotated_x = offset_x * math.cos(angle_rad) - offset_y * math.sin(angle_rad)
        rotated_y = offset_x * math.sin(angle_rad) + offset_y * math.cos(angle_rad)
        return self.x + rotated_x, self.y + rotated_y

    def draw(self, screen):
        """Draw the asteroid with irregular shape, realistic texturing, and details."""
        # Draw motion blur ghost images
        num_ghosts = len(self.previous_positions)
        for i, (ghost_x, ghost_y) in enumerate(self.previous_positions):
            # Calculate fade for ghost (older = more transparent)
            alpha = int(40 * (i + 1) / (num_ghosts + 1))
            ghost_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            ghost_color = (*self.colors[0], alpha)
            pygame.draw.circle(ghost_surface, ghost_color, (self.radius, self.radius), self.radius)
            screen.blit(ghost_surface, (int(ghost_x - self.radius), int(ghost_y - self.radius)))

        # Calculate rotated polygon points for irregular shape
        rotated_points = []
        for angle_deg, distance in self.shape_points:
            total_angle = self.angle + angle_deg
            px = self.x + distance * math.cos(math.radians(total_angle))
            py = self.y + distance * math.sin(math.radians(total_angle))
            rotated_points.append((int(px), int(py)))

        # Draw shadow/dark base layer first
        shadow_color = tuple(int(c * 0.6) for c in self.colors[0])
        pygame.draw.polygon(screen, shadow_color, rotated_points)

        # Draw main irregular asteroid body with custom colors
        pygame.draw.polygon(screen, self.colors[0], rotated_points)

        # Add texture with varied-color patches (simulate rock surface variation)
        num_patches = random.randint(2, 4) if self.radius > 30 else random.randint(1, 2)
        for i in range(num_patches):
            patch_angle = random.uniform(0, 360)
            patch_dist = random.uniform(0, self.radius * 0.5)
            patch_size = random.uniform(self.radius * 0.2, self.radius * 0.4)
            patch_x, patch_y = self._rotate_point(
                math.cos(math.radians(patch_angle)) * patch_dist,
                math.sin(math.radians(patch_angle)) * patch_dist
            )
            # Use middle color for patches
            pygame.draw.circle(
                screen,
                self.colors[1],
                (int(patch_x), int(patch_y)),
                int(patch_size)
            )

        # Draw craters with depth
        for crater_angle, crater_dist, crater_size in self.craters:
            crater_x, crater_y = self._rotate_point(
                math.cos(math.radians(crater_angle)) * crater_dist,
                math.sin(math.radians(crater_angle)) * crater_dist
            )
            # Dark crater base
            pygame.draw.circle(
                screen,
                self.colors[2],
                (int(crater_x), int(crater_y)),
                int(crater_size)
            )
            # Lighter crater rim for depth
            rim_offset_x = crater_size * 0.2
            rim_offset_y = crater_size * 0.2
            pygame.draw.circle(
                screen,
                self.colors[1],
                (int(crater_x - rim_offset_x), int(crater_y - rim_offset_y)),
                int(crater_size * 0.7)
            )

        # Draw cracks with varying width
        for crack_angle, start_dist, end_dist, width in self.cracks:
            start_x, start_y = self._rotate_point(
                math.cos(math.radians(crack_angle)) * start_dist,
                math.sin(math.radians(crack_angle)) * start_dist
            )
            end_x, end_y = self._rotate_point(
                math.cos(math.radians(crack_angle)) * end_dist,
                math.sin(math.radians(crack_angle)) * end_dist
            )
            # Draw crack as very dark line
            crack_color = tuple(int(c * 0.4) for c in self.colors[0])
            pygame.draw.line(
                screen,
                crack_color,
                (int(start_x), int(start_y)),
                (int(end_x), int(end_y)),
                width
            )

        # Add rim lighting effect (as if lit from top-right)
        rim_surface = pygame.Surface((self.radius * 2 + 10, self.radius * 2 + 10), pygame.SRCALPHA)

        # Draw multiple arcs with decreasing alpha for soft glow
        for i in range(3):
            alpha = 70 - i * 20
            thickness = 3 - i
            # Calculate rim light color (brighter version of asteroid color)
            rim_color = (
                min(255, self.colors[0][0] + 120),
                min(255, self.colors[0][1] + 120),
                min(255, self.colors[0][2] + 120),
                alpha
            )

            # Draw arc from 300 to 60 degrees (top-right quadrant)
            pygame.draw.arc(
                rim_surface,
                rim_color,
                (5 - i, 5 - i, self.radius * 2 + i * 2, self.radius * 2 + i * 2),
                math.radians(300),
                math.radians(60),
                thickness
            )

        screen.blit(rim_surface, (int(self.x - self.radius - 5), int(self.y - self.radius - 5)))

        # Draw mineral sparkles if present
        if self.has_minerals:
            sparkle_time = pygame.time.get_ticks()
            for mineral_angle, mineral_dist, brightness in self.mineral_points:
                # Make sparkles twinkle
                twinkle = (math.sin(sparkle_time / 200 + mineral_angle) + 1) / 2
                current_brightness = int(brightness * (0.6 + twinkle * 0.4))

                mineral_x, mineral_y = self._rotate_point(
                    math.cos(math.radians(mineral_angle)) * mineral_dist,
                    math.sin(math.radians(mineral_angle)) * mineral_dist
                )

                # Draw sparkle with glow
                sparkle_color = (current_brightness, current_brightness, min(255, current_brightness + 50))
                for size in range(2, 0, -1):
                    alpha = 255 - (2 - size) * 80
                    sparkle_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                    pygame.draw.circle(sparkle_surf, (*sparkle_color, alpha), (size, size), size)
                    screen.blit(sparkle_surf, (int(mineral_x - size), int(mineral_y - size)))

        # Add outline to irregular shape for definition
        pygame.draw.polygon(screen, tuple(int(c * 0.7) for c in self.colors[0]), rotated_points, 1)

    def is_off_screen(self):
        """Check if asteroid is completely off-screen."""
        return self.x < -self.radius

    def collides_with_ship(self, ship):
        """Check collision with ship using circular collision detection."""
        ship_center = ship.get_center()
        distance_squared = (ship_center[0] - self.x) ** 2 + (
            ship_center[1] - self.y
        ) ** 2
        collision_radius = self.radius + ship.width // 2
        return distance_squared < collision_radius**2

    def can_break(self):
        """Check if asteroid can break into smaller pieces."""
        return self.size_category in ["large", "medium"]

    def create_children(self, difficulty_multiplier=1.0):
        """Create smaller asteroids when this one breaks."""
        children = []
        if not self.can_break():
            return children

        # Determine number of children and their size
        if self.size_category == "large":
            num_children = 3
            child_radius = random.randint(20, 30)
        else:  # medium
            num_children = 2
            child_radius = random.randint(15, 22)

        # Create children with spread velocities
        for i in range(num_children):
            # Add some randomness to velocity for spread effect
            angle = random.uniform(-45, 45)  # degrees
            speed = self.base_speed * random.uniform(0.8, 1.3)

            # Calculate velocity components
            vx = speed * math.cos(math.radians(angle + 180))  # 180 for leftward
            vy = speed * math.sin(math.radians(angle))

            # Slight position offset so they don't stack
            offset_angle = (360 / num_children) * i
            offset_dist = self.radius * 0.5
            child_x = self.x + math.cos(math.radians(offset_angle)) * offset_dist
            child_y = self.y + math.sin(math.radians(offset_angle)) * offset_dist

            child = Asteroid(
                child_x, child_y, child_radius, difficulty_multiplier, vx, vy
            )
            children.append(child)

        return children


class Boss:
    """Boss enemy with health, special movement, and visual effects."""

    def __init__(self, pattern="sine", difficulty_level=1.0):
        # Center position for movement patterns
        self.center_x = WIDTH - 150  # Position on right side of screen
        self.center_y = HEIGHT // 2

        # Start at center position
        self.x = self.center_x
        self.y = self.center_y

        self.radius = BOSS_RADIUS
        # Scale health with difficulty (15 at diff 1.0, up to 45 at diff 3.0)
        base_health = BOSS_HEALTH
        self.max_health = int(base_health * difficulty_level)
        self.health = self.max_health
        self.speed = BOSS_SPEED
        self.points = 500  # Big score for defeating boss

        # Movement pattern
        self.pattern = pattern  # 'sine', 'circle', 'figure8'
        self.time = 0

        # Visual effects
        self.angle = 0
        self.glow_pulse = 0

    def update(self):
        """Update boss position based on movement pattern."""
        self.time += 1
        self.angle += 1
        self.glow_pulse = (self.glow_pulse + 5) % 360

        # Apply movement pattern (removed continuous leftward movement)
        if self.pattern == "sine":
            # Sinusoidal wave - oscillate horizontally and vertically
            amplitude_y = 150
            amplitude_x = 80
            frequency = 0.02
            self.y = self.center_y + amplitude_y * math.sin(self.time * frequency)
            self.x = self.center_x + amplitude_x * math.cos(self.time * frequency * 0.5)

        elif self.pattern == "circle":
            # Circular motion
            radius_movement = 120
            self.x = self.center_x + radius_movement * math.cos(self.time * 0.03)
            self.y = self.center_y + radius_movement * math.sin(self.time * 0.03)

        elif self.pattern == "figure8":
            # Figure-8 pattern
            amplitude = 100
            self.x = self.center_x + amplitude * math.cos(self.time * 0.02)
            self.y = self.center_y + amplitude * math.sin(self.time * 0.04) * math.cos(
                self.time * 0.02
            )

        elif self.pattern == "zigzag":
            # Zigzag pattern - sharp vertical movements
            amplitude = 120
            period = 40  # Frames per direction change
            direction = 1 if (self.time // period) % 2 == 0 else -1
            progress = (self.time % period) / period  # 0.0 to 1.0
            self.y = self.center_y + amplitude * direction * progress
            self.x = self.center_x

        elif self.pattern == "spiral":
            # Spiral outward and inward
            base_radius = 80
            radius_variation = 40 * math.sin(self.time * 0.01)
            radius = base_radius + radius_variation
            angle = self.time * 0.05
            self.x = self.center_x + radius * math.cos(angle)
            self.y = self.center_y + radius * math.sin(angle)

        # Keep within screen bounds
        self.x = max(self.radius, min(WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(HEIGHT - self.radius, self.y))

    def draw(self, screen):
        """Draw the boss with special effects."""
        # Pulsing glow effect
        glow_intensity = int(50 + 30 * math.sin(math.radians(self.glow_pulse)))
        glow_color = (
            min(255, BOSS_GLOW_COLOR[0] + glow_intensity),
            min(255, BOSS_GLOW_COLOR[1] + glow_intensity // 2),
            min(255, BOSS_GLOW_COLOR[2] + glow_intensity // 2),
        )

        # Draw glow rings
        for i in range(3):
            glow_radius = self.radius + 10 + i * 8
            alpha = 80 - i * 25
            s = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                s, (*glow_color, alpha), (glow_radius, glow_radius), glow_radius, 3
            )
            screen.blit(s, (int(self.x - glow_radius), int(self.y - glow_radius)))

        # Main boss body (darker red)
        pygame.draw.circle(screen, BOSS_COLOR, (int(self.x), int(self.y)), self.radius)

        # Rotating details
        for i in range(8):
            detail_angle = self.angle + (i * 45)
            detail_dist = self.radius * 0.7
            detail_x = self.x + detail_dist * math.cos(math.radians(detail_angle))
            detail_y = self.y + detail_dist * math.sin(math.radians(detail_angle))
            pygame.draw.circle(
                screen,
                BOSS_DETAIL_COLOR,
                (int(detail_x), int(detail_y)),
                self.radius // 4,
            )

        # Center core (pulsing)
        core_size = int(self.radius // 3 + 5 * math.sin(math.radians(self.glow_pulse)))
        pygame.draw.circle(screen, glow_color, (int(self.x), int(self.y)), core_size)

        # Energy veins animation - pulsing lines from center to edges
        vein_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        vein_pulse = (math.sin(self.time * 0.1) + 1) / 2  # 0 to 1
        for i in range(6):  # 6 veins
            vein_angle = (self.time * 2 + i * 60) % 360
            vein_length = self.radius * (0.5 + vein_pulse * 0.3)
            start_x = self.radius
            start_y = self.radius
            end_x = self.radius + vein_length * math.cos(math.radians(vein_angle))
            end_y = self.radius + vein_length * math.sin(math.radians(vein_angle))

            vein_alpha = int(120 + vein_pulse * 80)
            vein_color = (255, 100 + int(vein_pulse * 100), 100, vein_alpha)

            pygame.draw.line(
                vein_surface,
                vein_color,
                (int(start_x), int(start_y)),
                (int(end_x), int(end_y)),
                2
            )

        screen.blit(vein_surface, (int(self.x - self.radius), int(self.y - self.radius)))

        # Outer ring
        pygame.draw.circle(
            screen, BOSS_DETAIL_COLOR, (int(self.x), int(self.y)), self.radius, 4
        )

    def take_damage(self, damage=1):
        """Boss takes damage from laser hit."""
        self.health -= damage
        return self.health <= 0  # Returns True if defeated

    def is_off_screen(self):
        """Check if boss has moved off the left side."""
        return self.x < -self.radius

    def collides_with_ship(self, ship):
        """Check collision with ship."""
        ship_center = ship.get_center()
        distance_squared = (ship_center[0] - self.x) ** 2 + (
            ship_center[1] - self.y
        ) ** 2
        collision_radius = self.radius + ship.width // 2
        return distance_squared < collision_radius**2


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
        # Trail segments for fading trail effect
        self.trail_segments = []  # List of (x, y) positions

    def update(self):
        """Move laser."""
        # Store current position for trail
        self.trail_segments.append((self.x, self.y))
        # Keep only last N segments
        if len(self.trail_segments) > LASER_TRAIL_LENGTH:
            self.trail_segments.pop(0)

        self.x += self.vx
        self.y += self.vy

    def draw(self, screen):
        """Draw the laser with glow effect and fading trail."""
        # Draw fading trail segments
        num_segments = len(self.trail_segments)
        for i, (trail_x, trail_y) in enumerate(self.trail_segments):
            # Calculate fade factor (older segments are more faded)
            fade_factor = (i + 1) / (num_segments + 1)
            trail_alpha = int(255 * fade_factor * 0.6)  # Max 60% opacity for trails

            # Create semi-transparent surface for trail segment
            trail_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            trail_color = (*LASER_COLOR, trail_alpha)
            pygame.draw.rect(trail_surface, trail_color, (0, 0, self.width, self.height))
            screen.blit(trail_surface, (int(trail_x), int(trail_y - 3)))

        # Draw main laser body with glow effect
        pygame.draw.rect(
            screen, LASER_COLOR, (int(self.x), int(self.y - 3), self.width, self.height)
        )
        pygame.draw.rect(
            screen, LASER_GLOW_COLOR, (int(self.x), int(self.y - 2), self.width, 4)
        )

    def is_off_screen(self):
        """Check if laser is off-screen."""
        return self.x > WIDTH or self.x < 0 or self.y > HEIGHT or self.y < 0

    def collides_with_asteroid(self, asteroid):
        """Check collision with asteroid using rectangle-circle collision."""
        return (
            self.x < asteroid.x + asteroid.radius
            and self.x + self.width > asteroid.x - asteroid.radius
            and self.y < asteroid.y + asteroid.radius
            and self.y + self.height > asteroid.y - asteroid.radius
        )

    def collides_with_boss(self, boss):
        """Check collision with boss using rectangle-circle collision."""
        return (
            self.x < boss.x + boss.radius
            and self.x + self.width > boss.x - boss.radius
            and self.y < boss.y + boss.radius
            and self.y + self.height > boss.y - boss.radius
        )


class PowerUp:
    """Power-up collectible."""

    def __init__(self, x, y, powerup_type):
        self.x = x
        self.y = y
        self.size = POWERUP_SIZE
        self.speed = POWERUP_SPEED
        self.type = powerup_type
        self.color = POWERUP_COLORS.get(powerup_type, (255, 255, 255))

        # Pre-render text for performance
        font = pygame.font.SysFont(None, 20)
        letter = self.type[0].upper()
        self.letter_text = font.render(letter, True, (0, 0, 0))

    def update(self):
        """Move power-up to the left."""
        self.x -= self.speed

    def draw(self, screen):
        """Draw the power-up with pulsing glow halo."""
        # Calculate pulsing glow effect
        pulse = (math.sin(pygame.time.get_ticks() / 200.0) + 1) / 2  # 0 to 1
        glow_radius = self.size * (1.5 + pulse * 0.5)  # Pulsing between 1.5x and 2x

        # Draw pulsing glow halos
        glow_surface = pygame.Surface((int(glow_radius * 2 + 20), int(glow_radius * 2 + 20)), pygame.SRCALPHA)
        glow_center = (int(glow_radius + 10), int(glow_radius + 10))

        # Multiple layers for soft glow
        for i in range(3):
            alpha = int((60 - i * 20) * (0.5 + pulse * 0.5))
            current_radius = glow_radius - i * 5
            glow_color = (*self.color, alpha)
            pygame.draw.circle(glow_surface, glow_color, glow_center, int(current_radius))

        screen.blit(glow_surface, (int(self.x - glow_radius - 10), int(self.y - glow_radius - 10)))

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

        # Draw icon letter (using pre-rendered text)
        screen.blit(
            self.letter_text,
            (
                self.x - self.letter_text.get_width() // 2,
                self.y - self.letter_text.get_height() // 2,
            ),
        )

    def is_off_screen(self):
        """Check if power-up is off-screen."""
        return self.x < -self.size

    def collides_with_ship(self, ship):
        """Check collision with ship."""
        ship_center = ship.get_center()
        distance_squared = (ship_center[0] - self.x) ** 2 + (
            ship_center[1] - self.y
        ) ** 2
        collision_radius = self.size + ship.width // 2
        return distance_squared < collision_radius**2


class PowerUpManager:
    """Manages all active power-up states and timers."""

    def __init__(self, ship):
        """Initialize the power-up manager.

        Args:
            ship: Reference to the Ship object for shield management
        """
        self.ship = ship
        # Dictionary to store active power-up timers
        self.active_powerups = {
            "rapid_fire": 0,
            "spread_shot": 0,
            "double_damage": 0,
            "magnet": 0,
            "time_slow": 0,
        }

    def update(self):
        """Update all power-up timers and deactivate expired ones."""
        for powerup_type in self.active_powerups:
            if self.active_powerups[powerup_type] > 0:
                self.active_powerups[powerup_type] -= 1

        # Update shield separately (managed by ship)
        if self.ship.shield_timer > 0:
            self.ship.shield_timer -= 1
            if self.ship.shield_timer == 0:
                self.ship.has_shield = False

    def activate(self, powerup_type):
        """Activate a power-up. Stacks duration up to 2x max if already active.

        Args:
            powerup_type: Type of power-up to activate
        """
        if powerup_type == "shield":
            self.ship.has_shield = True
            # Stack duration up to 2x max
            self.ship.shield_timer += SHIELD_DURATION
            self.ship.shield_timer = min(SHIELD_DURATION * 2, self.ship.shield_timer)
        elif powerup_type in self.active_powerups:
            # Stack duration up to 2x max for non-instant power-ups
            self.active_powerups[powerup_type] += POWERUP_DURATION
            self.active_powerups[powerup_type] = min(
                POWERUP_DURATION * 2, self.active_powerups[powerup_type]
            )

    def is_active(self, powerup_type):
        """Check if a power-up is currently active.

        Args:
            powerup_type: Type of power-up to check

        Returns:
            bool: True if active, False otherwise
        """
        if powerup_type == "shield":
            return self.ship.has_shield
        return self.active_powerups.get(powerup_type, 0) > 0

    def get_timer(self, powerup_type):
        """Get remaining timer for a power-up.

        Args:
            powerup_type: Type of power-up

        Returns:
            int: Remaining frames for the power-up
        """
        if powerup_type == "shield":
            return self.ship.shield_timer
        return self.active_powerups.get(powerup_type, 0)


class Explosion:
    """Enhanced explosion animation with smooth gradients and particles."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = EXPLOSION_INITIAL_SIZE
        self.max_size = EXPLOSION_MAX_SIZE
        self.lifetime = 0
        self.max_lifetime = EXPLOSION_MAX_SIZE - EXPLOSION_INITIAL_SIZE

        # Create explosion particles for organic feel
        self.particles = []
        num_particles = random.randint(8, 12)
        for _ in range(num_particles):
            angle = random.uniform(0, 360)
            speed = random.uniform(1.5, 3.5)
            particle = {
                'x': x,
                'y': y,
                'vx': speed * math.cos(math.radians(angle)),
                'vy': speed * math.sin(math.radians(angle)),
                'size': random.randint(2, 4),
                'lifetime': random.randint(10, 20),
                'max_lifetime': 20,
                'color': random.choice(EXPLOSION_COLORS)
            }
            self.particles.append(particle)

    def update(self):
        """Grow the explosion and update particles."""
        self.size += 1.5  # Slightly faster growth
        self.lifetime += 1

        # Update particles
        for particle in self.particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['lifetime'] -= 1
            # Slow down particles over time
            particle['vx'] *= 0.95
            particle['vy'] *= 0.95

    def draw(self, screen):
        """Draw explosion with smooth gradients and particles."""
        progress = self.lifetime / self.max_lifetime

        # Draw main explosion with smooth radial gradient
        # Multiple layers with decreasing opacity for smooth gradient
        num_layers = 8
        for i in range(num_layers):
            layer_progress = (num_layers - i) / num_layers
            radius = int(self.size * layer_progress)

            if radius > 0:
                # Calculate color based on progress and layer
                # Start bright white/yellow, transition to orange/red
                if progress < 0.3:
                    # Early explosion: bright white/yellow core
                    color_idx = 1 if i < 3 else 0
                elif progress < 0.6:
                    # Mid explosion: orange
                    color_idx = 0
                else:
                    # Late explosion: dark red
                    color_idx = 2

                base_color = EXPLOSION_COLORS[color_idx]

                # Add brightness to inner layers
                brightness_boost = int((1.0 - layer_progress) * 100) if i < 4 else 0
                color = tuple(min(255, c + brightness_boost) for c in base_color)

                # Calculate alpha with smooth falloff
                alpha = int(255 * (1.0 - progress) * layer_progress * 0.8)

                if alpha > 0:
                    # Create surface for this layer
                    surf_size = radius * 2 + 4
                    s = pygame.Surface((surf_size, surf_size), pygame.SRCALPHA)

                    # Draw filled circle with alpha
                    color_with_alpha = (*color, alpha)
                    pygame.draw.circle(s, color_with_alpha, (surf_size // 2, surf_size // 2), radius)

                    # Blit to screen
                    screen.blit(s, (int(self.x - surf_size // 2), int(self.y - surf_size // 2)))

        # Draw bright flash at the center for first few frames
        if progress < 0.2:
            flash_alpha = int(255 * (1.0 - progress / 0.2))
            flash_size = max(3, int(self.size * 0.3))
            s = pygame.Surface((flash_size * 2, flash_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (255, 255, 255, flash_alpha), (flash_size, flash_size), flash_size)
            screen.blit(s, (int(self.x - flash_size), int(self.y - flash_size)))

        # Draw explosion particles
        for particle in self.particles:
            if particle['lifetime'] > 0:
                alpha = int(255 * (particle['lifetime'] / particle['max_lifetime']))
                if alpha > 0:
                    size = particle['size']
                    s = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                    color_with_alpha = (*particle['color'], alpha)
                    pygame.draw.circle(s, color_with_alpha, (size, size), size)
                    screen.blit(s, (int(particle['x'] - size), int(particle['y'] - size)))

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
        self.base_brightness = brightness
        self.color = color
        # Twinkling effect
        self.twinkle_offset = random.uniform(0, 360)
        self.twinkle_speed = random.uniform(0.5, 2.0)

    def update(self, paused=False):
        """Move star to create parallax effect."""
        if not paused:
            self.x -= self.speed
            if self.x < -5:
                self.x = WIDTH + 5
                self.y = random.randint(0, HEIGHT)

        # Update twinkling animation
        self.twinkle_offset += self.twinkle_speed
        if self.twinkle_offset >= 360:
            self.twinkle_offset -= 360

        # Calculate brightness variation for twinkling
        twinkle_factor = (math.sin(math.radians(self.twinkle_offset)) + 1) / 2  # 0 to 1
        brightness_variation = int(50 * twinkle_factor)
        self.brightness = min(255, self.base_brightness + brightness_variation)

    def draw(self, screen):
        """Draw the star with twinkling effect."""
        # Update color brightness for twinkling
        twinkle_color = tuple(min(255, int(c * self.brightness / self.base_brightness)) for c in self.color)
        pygame.draw.circle(screen, twinkle_color, (int(self.x), int(self.y)), self.size)


class Particle:
    """Visual particle effect with multiple shapes."""

    def __init__(
        self, x, y, color, velocity_x=0, velocity_y=0, size=None, lifetime=None, shape="circle"
    ):
        self.x = x
        self.y = y
        self.color = color
        self.vx = velocity_x
        self.vy = velocity_y
        self.size = (
            size if size else random.randint(PARTICLE_MIN_SIZE, PARTICLE_MAX_SIZE)
        )
        self.lifetime = lifetime if lifetime else PARTICLE_LIFETIME
        self.max_lifetime = self.lifetime
        self.alpha = 255
        self.shape = shape  # "circle", "star", "square"

    def update(self):
        """Update particle position and fade."""
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        # Fade out over lifetime
        self.alpha = int(255 * (self.lifetime / self.max_lifetime))

    def draw_star(self, surface, center, radius, color_with_alpha):
        """Draw a star shape."""
        points = []
        for i in range(10):  # 5-pointed star = 10 points (5 outer, 5 inner)
            angle = math.radians(i * 36 - 90)  # -90 to start pointing up
            if i % 2 == 0:
                # Outer point
                r = radius
            else:
                # Inner point
                r = radius * 0.4
            px = center[0] + r * math.cos(angle)
            py = center[1] + r * math.sin(angle)
            points.append((px, py))
        pygame.draw.polygon(surface, color_with_alpha, points)

    def draw_square(self, surface, center, size, color_with_alpha):
        """Draw a square shape."""
        half_size = size
        rect = pygame.Rect(
            center[0] - half_size, center[1] - half_size, size * 2, size * 2
        )
        pygame.draw.rect(surface, color_with_alpha, rect)

    def draw(self, screen):
        """Draw particle with transparency based on shape."""
        if self.alpha > 0:
            s = pygame.Surface((self.size * 3, self.size * 3), pygame.SRCALPHA)
            color_with_alpha = (*self.color[:3], self.alpha)
            center = (self.size * 1.5, self.size * 1.5)

            if self.shape == "star":
                self.draw_star(s, center, self.size, color_with_alpha)
            elif self.shape == "square":
                self.draw_square(s, center, self.size, color_with_alpha)
            else:  # circle
                pygame.draw.circle(s, color_with_alpha, (int(center[0]), int(center[1])), self.size)

            screen.blit(s, (int(self.x - self.size * 1.5), int(self.y - self.size * 1.5)))

    def is_dead(self):
        """Check if particle should be removed."""
        return self.lifetime <= 0


class ScorePopup:
    """Floating score text that rises and fades out with smooth rendering."""

    def __init__(self, x, y, score):
        self.x = x
        self.y = y
        self.score = score
        self.lifetime = SCORE_POPUP_LIFETIME
        self.max_lifetime = SCORE_POPUP_LIFETIME
        self.velocity_y = SCORE_POPUP_RISE_SPEED
        self.scale = 0.5  # Start small for pop-in effect

        # Choose font size based on score magnitude
        self.font_size = 28 if score < 100 else 34 if score < 500 else 40
        self.font = pygame.font.SysFont(None, self.font_size, bold=True)
        self.text = f"+{score}"

    def update(self):
        """Update position, scale, and fade."""
        self.y += self.velocity_y
        self.lifetime -= 1

        # Pop-in effect: quickly scale up at start
        progress = 1.0 - (self.lifetime / self.max_lifetime)
        if progress < 0.15:
            # Quick pop-in to full size
            self.scale = 0.5 + (progress / 0.15) * 0.5
        else:
            self.scale = 1.0

    def draw(self, screen):
        """Draw the score popup with outline and smooth fading (no background)."""
        if self.lifetime > 0:
            # Calculate alpha based on lifetime
            alpha = int(255 * (self.lifetime / self.max_lifetime))

            # Calculate current font size with scale
            current_size = int(self.font_size * self.scale)
            if current_size < 10:
                return  # Don't render if too small

            # Create font at current scale
            scaled_font = pygame.font.SysFont(None, current_size, bold=True)

            # Create a transparent surface to draw on
            # First, render text to get size
            temp_text = scaled_font.render(self.text, True, COMBO_COLOR)
            text_width, text_height = temp_text.get_size()

            # Create transparent surface large enough for text + outline
            surf_width = text_width + 4
            surf_height = text_height + 4
            transparent_surface = pygame.Surface((surf_width, surf_height), pygame.SRCALPHA)
            transparent_surface.fill((0, 0, 0, 0))  # Fully transparent background

            # Render outline (dark shadow for contrast)
            outline_color = (0, 0, 0, alpha)  # Include alpha in color
            for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, -1), (-1, 0), (1, 0), (0, 1)]:
                outline_surface = scaled_font.render(self.text, True, (0, 0, 0))
                # Create a copy with alpha
                outline_alpha_surf = pygame.Surface(outline_surface.get_size(), pygame.SRCALPHA)
                outline_alpha_surf.fill((0, 0, 0, 0))
                outline_alpha_surf.blit(outline_surface, (0, 0))
                outline_alpha_surf.set_alpha(alpha)
                transparent_surface.blit(outline_alpha_surf, (2 + dx, 2 + dy))

            # Render main text with alpha
            text_surface = scaled_font.render(self.text, True, COMBO_COLOR)
            text_alpha_surf = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
            text_alpha_surf.fill((0, 0, 0, 0))
            text_alpha_surf.blit(text_surface, (0, 0))
            text_alpha_surf.set_alpha(alpha)
            transparent_surface.blit(text_alpha_surf, (2, 2))

            # Blit the final transparent surface to screen
            final_x = int(self.x - surf_width // 2)
            final_y = int(self.y - surf_height // 2)
            screen.blit(transparent_surface, (final_x, final_y))

    def is_dead(self):
        """Check if popup should be removed."""
        return self.lifetime <= 0


class NebulaCloud:
    """Procedural background nebula cloud for visual depth."""

    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.randint(NEBULA_MIN_SIZE, NEBULA_MAX_SIZE)
        self.color = random.choice(NEBULA_COLORS)
        self.drift_speed = random.uniform(0.05, 0.15)

        # Create multiple layers for depth
        self.layers = []
        num_layers = random.randint(3, 5)
        for i in range(num_layers):
            layer_size = self.size * (1.0 - i * 0.15)
            layer_offset_x = random.uniform(-self.size * 0.3, self.size * 0.3)
            layer_offset_y = random.uniform(-self.size * 0.3, self.size * 0.3)
            layer_alpha = int(self.color[3] * (0.8 - i * 0.15))
            self.layers.append({
                'size': layer_size,
                'offset_x': layer_offset_x,
                'offset_y': layer_offset_y,
                'alpha': layer_alpha
            })

    def update(self):
        """Move nebula slowly to create parallax effect."""
        self.x -= self.drift_speed
        if self.x < -self.size:
            self.x = WIDTH + self.size
            self.y = random.randint(0, HEIGHT)

    def draw(self, screen):
        """Draw the nebula cloud with multiple layers."""
        for layer in self.layers:
            s = pygame.Surface((int(layer['size'] * 2), int(layer['size'] * 2)), pygame.SRCALPHA)
            color_with_alpha = (*self.color[:3], layer['alpha'])
            pygame.draw.circle(
                s,
                color_with_alpha,
                (int(layer['size']), int(layer['size'])),
                int(layer['size'])
            )
            screen.blit(
                s,
                (
                    int(self.x + layer['offset_x'] - layer['size']),
                    int(self.y + layer['offset_y'] - layer['size'])
                )
            )


class DistortionWave:
    """Screen-wide ripple effect for dramatic events."""

    def __init__(self, x, y, max_radius=DISTORTION_MAX_RADIUS):
        self.x = x
        self.y = y
        self.radius = 0
        self.max_radius = max_radius
        self.lifetime = DISTORTION_LIFETIME
        self.max_lifetime = DISTORTION_LIFETIME

    def update(self):
        """Expand the wave outward."""
        self.lifetime -= 1
        # Radius grows quickly at first, then slows
        progress = 1.0 - (self.lifetime / self.max_lifetime)
        self.radius = self.max_radius * (progress ** 0.7)

    def draw(self, screen):
        """Draw concentric rings with varying alpha."""
        if self.lifetime > 0:
            # Draw 3 rings at different offsets
            for i in range(3):
                ring_radius = int(self.radius - i * 20)
                if ring_radius > 0:
                    alpha = int(100 * (self.lifetime / self.max_lifetime) * (1.0 - i * 0.3))
                    if alpha > 0:
                        s = pygame.Surface((ring_radius * 2, ring_radius * 2), pygame.SRCALPHA)
                        color_with_alpha = (150, 200, 255, alpha)
                        pygame.draw.circle(
                            s,
                            color_with_alpha,
                            (ring_radius, ring_radius),
                            ring_radius,
                            3
                        )
                        screen.blit(
                            s,
                            (int(self.x - ring_radius), int(self.y - ring_radius))
                        )

    def is_finished(self):
        """Check if wave animation is complete."""
        return self.lifetime <= 0


class Game:
    """Main game controller."""

    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Ship Obstacle Avoidance - Enhanced")
        self.clock = pygame.time.Clock()

        # Fonts
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)
        self.title_font = pygame.font.SysFont(None, 72)
        self.large_font = pygame.font.SysFont(None, 48)

        # Game state
        self.running = True
        self.game_state = "menu"  # "menu", "playing", "game_over", "highscores", "options"
        self.game_over = False
        self.paused = False
        self.score = 0
        self.high_scores = []  # List of (score, name) tuples
        self.player_name = ""
        self.name_input_active = False

        # Audio settings
        self.volume = 1.0  # 0.0 to 1.0 (0% to 100%)
        self.muted = False

        # Menu state
        self.menu_options = ["Play", "Highscores", "Options", "Exit"]
        self.menu_selected = 0
        self.pause_options = ["Resume", "Options", "Main Menu"]
        self.pause_selected = 0
        self.options_selected = 0  # For options menu navigation
        self.previous_state = None  # Track where we came from

        # Game objects
        self.ship = Ship(SHIP_START_X, SHIP_START_Y)
        self.asteroids = []
        self.lasers = []
        self.explosions = []
        self.stars = []
        self.powerups = []
        self.particles = []
        self.boss = None
        self.boss_warning = False
        self.boss_warning_timer = 0
        self.last_boss_spawn_score = 0

        # Timers and counters
        self.laser_cooldown = 0
        self.asteroid_spawn_timer = 0
        self.difficulty_level = 1.0

        # Combo system
        self.combo = 0
        self.combo_timer = 0

        # Power-up manager
        self.powerup_manager = PowerUpManager(self.ship)

        # Screen shake
        self.screen_shake = 0
        self.shake_offset_x = 0
        self.shake_offset_y = 0

        # New visual systems
        self.score_popups = []
        self.nebula_clouds = []
        self.distortion_waves = []

        # UI animation tracking
        self.previous_combo = 0
        self.previous_lives = MAX_LIVES
        self.scan_line_offset = 0

        # Color theme based on score
        self.theme_color = (100, 200, 255)  # Default blue

        # Pre-render vignette surface for performance
        self.vignette_surface = self._create_vignette()

        # Sound effects
        self.sounds_enabled = False
        self.sounds = {}
        self.init_sounds()

        # Initialize game
        self.ensure_data_directory()
        self.load_high_score()
        self.load_settings()
        self.apply_volume()
        self.create_stars()
        self.create_initial_asteroids()
        self.create_nebula_clouds()

    def _create_vignette(self):
        """Create vignette surface for screen edges darkening effect."""
        vignette = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        center_x, center_y = WIDTH // 2, HEIGHT // 2
        max_distance = math.sqrt(center_x**2 + center_y**2)

        # Create radial gradient from center to edges
        for y in range(HEIGHT):
            for x in range(WIDTH):
                distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                alpha = int(120 * (distance / max_distance) ** 2)
                vignette.set_at((x, y), (0, 0, 0, min(alpha, 180)))

        return vignette

    def create_nebula_clouds(self):
        """Create background nebula clouds."""
        for _ in range(NEBULA_COUNT):
            self.nebula_clouds.append(NebulaCloud())

    def ensure_data_directory(self):
        """Ensure the data directory exists."""
        if not os.path.exists(DATA_DIR):
            try:
                os.makedirs(DATA_DIR)
                print(f"✅ Created data directory: {DATA_DIR}")
            except OSError as e:
                print(f"⚠️  Could not create data directory: {e}")

    def init_sounds(self):
        """Initialize sound effects (requires sound files)."""
        sound_files = {
            "laser": "sounds/laser.wav",
            "explosion": "sounds/explosion.wav",
            "explosion_big": "sounds/explosion_big.wav",
            "hit": "sounds/hit.wav",
            "powerup": "sounds/powerup.wav",
            "shield": "sounds/shield.wav",
            "boss_warning": "sounds/boss_warning.wav",
        }

        loaded_count = 0
        for sound_name, sound_path in sound_files.items():
            try:
                # Use resource_path to find sounds in both dev and bundled .exe
                full_path = resource_path(sound_path)
                self.sounds[sound_name] = pygame.mixer.Sound(full_path)
                loaded_count += 1
            except (FileNotFoundError, pygame.error):
                # Sound file not found, skip it
                self.sounds[sound_name] = None

        # Enable sounds if at least some loaded
        if loaded_count > 0:
            self.sounds_enabled = True
            print(f"✅ Loaded {loaded_count}/{len(sound_files)} sound effects")

            # Try to load background music
            try:
                # Use resource_path to find music in both dev and bundled .exe
                music_path = resource_path("sounds/music.wav")
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(1.0)  # Will be adjusted by apply_volume()
                pygame.mixer.music.play(-1)  # Loop forever
                print("✅ Background music loaded")
            except (FileNotFoundError, pygame.error):
                pass  # Music file not found, continue without it
        else:
            print("ℹ️  No sound files found. Game will run silently.")

    def play_sound(self, sound_name):
        """Play a sound effect."""
        if self.sounds_enabled and sound_name in self.sounds:
            sound = self.sounds[sound_name]
            if sound:
                sound.play()

    def load_high_score(self):
        """Load top 10 high scores from file."""
        self.high_scores = []
        if os.path.exists(HIGH_SCORE_FILE):
            try:
                with open(HIGH_SCORE_FILE, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            parts = line.split(":", 1)
                            if len(parts) == 2:
                                score = int(parts[0])
                                name = parts[1]
                                self.high_scores.append((score, name))
            except (FileNotFoundError, ValueError, IOError):
                pass

        # Sort by score descending and keep top 10
        self.high_scores.sort(reverse=True, key=lambda x: x[0])
        self.high_scores = self.high_scores[:10]

    def save_high_score(self):
        """Save high score to file and update top 10."""
        # Add new score
        self.high_scores.append((self.score, self.player_name))

        # Sort by score descending and keep top 10
        self.high_scores.sort(reverse=True, key=lambda x: x[0])
        self.high_scores = self.high_scores[:10]

        # Save to file
        try:
            with open(HIGH_SCORE_FILE, "w") as f:
                for score, name in self.high_scores:
                    # Sanitize name to prevent file corruption
                    safe_name = name.replace(':', '').replace('\n', '').replace('\r', '')[:MAX_NAME_LENGTH]
                    f.write(f"{score}:{safe_name}\n")
        except (IOError, OSError):
            pass

    def is_high_score(self):
        """Check if current score qualifies for top 10."""
        if len(self.high_scores) < 10:
            return True
        return self.score > self.high_scores[-1][0]

    def load_settings(self):
        """Load audio settings from file."""
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            parts = line.split(":", 1)
                            if len(parts) == 2:
                                key, value = parts
                                if key == "volume":
                                    self.volume = float(value)
                                elif key == "muted":
                                    self.muted = value.lower() == "true"
            except (FileNotFoundError, ValueError, IOError):
                pass

    def save_settings(self):
        """Save audio settings to file."""
        try:
            with open(SETTINGS_FILE, "w") as f:
                f.write(f"volume:{self.volume}\n")
                f.write(f"muted:{self.muted}\n")
        except (IOError, OSError):
            pass

    def apply_volume(self):
        """Apply current volume and mute settings to music and sounds."""
        effective_volume = 0.0 if self.muted else self.volume

        # Apply to music (set volume regardless of whether music is playing)
        pygame.mixer.music.set_volume(effective_volume)

        # Apply to all sound effects
        for sound_name, sound in self.sounds.items():
            if sound:
                sound.set_volume(effective_volume)

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
        self.particles = []
        self.boss = None
        self.boss_warning = False
        self.boss_warning_timer = 0
        self.last_boss_spawn_score = 0
        self.score = 0
        self.game_over = False
        self.paused = False
        self.player_name = ""
        self.name_input_active = False
        self.laser_cooldown = 0
        self.asteroid_spawn_timer = 0
        self.difficulty_level = 1.0
        self.combo = 0
        self.combo_timer = 0
        self.powerup_manager = PowerUpManager(self.ship)  # Reset power-up manager
        self.screen_shake = 0
        # Reset new visual systems
        self.score_popups = []
        self.distortion_waves = []
        self.previous_combo = 0
        self.previous_lives = MAX_LIVES
        self.scan_line_offset = 0
        self.theme_color = (100, 200, 255)
        self.create_initial_asteroids()

    def handle_events(self):
        """Process pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                # Menu navigation
                if self.game_state == "menu":
                    if event.key in [pygame.K_w, pygame.K_UP]:
                        self.menu_selected = (self.menu_selected - 1) % len(
                            self.menu_options
                        )
                    elif event.key in [pygame.K_s, pygame.K_DOWN]:
                        self.menu_selected = (self.menu_selected + 1) % len(
                            self.menu_options
                        )
                    elif event.key == pygame.K_RETURN:
                        self.handle_menu_selection()

                # Highscores screen
                elif self.game_state == "highscores":
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        self.game_state = "menu"

                # Options screen
                elif self.game_state == "options":
                    if event.key in [pygame.K_w, pygame.K_UP]:
                        self.options_selected = (self.options_selected - 1) % 2  # 2 options: volume and mute
                    elif event.key in [pygame.K_s, pygame.K_DOWN]:
                        self.options_selected = (self.options_selected + 1) % 2
                    elif event.key in [pygame.K_a, pygame.K_LEFT]:
                        # Decrease volume or toggle mute
                        if self.options_selected == 0:  # Volume slider
                            self.volume = max(0.0, self.volume - 0.1)
                            self.apply_volume()
                            self.save_settings()
                        elif self.options_selected == 1:  # Mute toggle
                            self.muted = not self.muted
                            self.apply_volume()
                            self.save_settings()
                    elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                        # Increase volume or toggle mute
                        if self.options_selected == 0:  # Volume slider
                            self.volume = min(1.0, self.volume + 0.1)
                            self.apply_volume()
                            self.save_settings()
                        elif self.options_selected == 1:  # Mute toggle
                            self.muted = not self.muted
                            self.apply_volume()
                            self.save_settings()
                    elif event.key == pygame.K_RETURN:
                        # Toggle mute on enter for mute option
                        if self.options_selected == 1:
                            self.muted = not self.muted
                            self.apply_volume()
                            self.save_settings()
                    elif event.key == pygame.K_ESCAPE:
                        # Return to previous state
                        if self.previous_state == "menu":
                            self.game_state = "menu"
                        elif self.previous_state == "pause":
                            self.game_state = "playing"
                            self.paused = True
                        else:
                            self.game_state = "menu"

                # Playing game
                elif self.game_state == "playing":
                    # Pause menu navigation
                    if self.paused and not self.game_over:
                        if event.key in [pygame.K_w, pygame.K_UP]:
                            self.pause_selected = (self.pause_selected - 1) % len(
                                self.pause_options
                            )
                        elif event.key in [pygame.K_s, pygame.K_DOWN]:
                            self.pause_selected = (self.pause_selected + 1) % len(
                                self.pause_options
                            )
                        elif event.key == pygame.K_RETURN:
                            self.handle_pause_selection()
                        elif event.key == pygame.K_ESCAPE:
                            self.paused = False
                            self.pause_selected = 0
                    # Pause game
                    elif event.key == pygame.K_ESCAPE and not self.game_over:
                        self.paused = True
                        self.pause_selected = 0

                    # Shoot laser
                    elif (
                        event.key == pygame.K_SPACE
                        and not self.game_over
                        and not self.paused
                        and self.laser_cooldown == 0
                    ):
                        self.shoot_laser()

                    # Restart game
                    elif event.key == pygame.K_r and self.game_over:
                        self.reset()

                    # Exit to menu
                    elif event.key == pygame.K_ESCAPE and self.game_over:
                        self.game_state = "menu"
                        self.game_over = False

                # Game over - name input
                elif self.game_state == "game_over":
                    # Submit name
                    if event.key == pygame.K_RETURN and self.name_input_active:
                        self.name_input_active = False
                        if self.is_high_score():
                            self.save_high_score()

                    # Backspace in name entry
                    elif event.key == pygame.K_BACKSPACE and self.name_input_active:
                        self.player_name = self.player_name[:-1]

                    # Exit to menu
                    elif event.key == pygame.K_ESCAPE:
                        self.game_state = "menu"
                        self.game_over = False
                        self.name_input_active = False

                    # Restart game
                    elif event.key == pygame.K_r and not self.name_input_active:
                        self.game_state = "playing"
                        self.reset()

                    # Type name
                    elif (
                        self.name_input_active
                        and len(self.player_name) < MAX_NAME_LENGTH
                        and event.unicode.isprintable()
                        and event.unicode not in ['\n', '\r', ':']  # Reject invalid chars
                    ):
                        self.player_name += event.unicode

    def handle_menu_selection(self):
        """Handle menu option selection."""
        selected = self.menu_options[self.menu_selected]

        if selected == "Play":
            self.game_state = "playing"
            self.reset()
        elif selected == "Highscores":
            self.game_state = "highscores"
        elif selected == "Options":
            self.previous_state = "menu"
            self.game_state = "options"
            self.options_selected = 0
        elif selected == "Exit":
            self.running = False

    def handle_pause_selection(self):
        """Handle pause menu option selection."""
        selected = self.pause_options[self.pause_selected]

        if selected == "Resume":
            self.paused = False
            self.pause_selected = 0
        elif selected == "Options":
            self.previous_state = "pause"
            self.game_state = "options"
            self.options_selected = 0
        elif selected == "Main Menu":
            self.paused = False
            self.pause_selected = 0
            self.game_state = "menu"
            self.game_over = False

    def shoot_laser(self):
        """Fire laser(s) based on current power-ups."""
        cooldown = (
            RAPID_FIRE_COOLDOWN if self.powerup_manager.is_active("rapid_fire") else LASER_COOLDOWN_FRAMES
        )

        if self.powerup_manager.is_active("spread_shot"):
            # Shoot 3 lasers in a spread
            for angle in [-SPREAD_SHOT_ANGLE, 0, SPREAD_SHOT_ANGLE]:
                laser = Laser(self.ship.x + self.ship.width, self.ship.y, angle)
                self.lasers.append(laser)
        else:
            # Shoot single laser
            laser = Laser(self.ship.x + self.ship.width, self.ship.y)
            self.lasers.append(laser)

        self.laser_cooldown = cooldown
        self.play_sound("laser")

    def spawn_powerup(self, x, y):
        """Spawn a random power-up."""
        if random.random() < POWERUP_SPAWN_CHANCE:
            powerup_types = [
                "shield",
                "rapid_fire",
                "spread_shot",
                "double_damage",
                "magnet",
                "time_slow",
                "nuke",
            ]
            # Weight the power-ups (nuke is rarer)
            weights = [1.5, 1.5, 1.5, 1.2, 1.2, 1.0, 0.3]
            powerup_type = random.choices(powerup_types, weights=weights)[0]
            self.powerups.append(PowerUp(x, y, powerup_type))

    def activate_powerup(self, powerup_type):
        """Activate a power-up effect. Stacks duration if already active."""
        if powerup_type == "nuke":
            # Create massive distortion wave from ship center
            ship_center = self.ship.get_center()
            self.distortion_waves.append(DistortionWave(ship_center[0], ship_center[1], max_radius=600))

            # Instant effect - destroy all asteroids with combo multiplier
            for asteroid in self.asteroids:
                self.explosions.append(Explosion(asteroid.x, asteroid.y))
                self.create_debris_particles(
                    asteroid.x, asteroid.y, count=int(asteroid.radius / 2)
                )
                # Apply combo multiplier to nuke points
                multiplier_index = min(self.combo - 1, len(COMBO_MULTIPLIERS) - 1)
                multiplier = COMBO_MULTIPLIERS[multiplier_index] if self.combo > 0 else 1
                self.score += asteroid.points * multiplier
            self.asteroids = []
            # Damage boss heavily if present
            if self.boss:
                nuke_damage = NUKE_BOSS_DAMAGE
                if self.boss.take_damage(nuke_damage):
                    # Boss defeated by nuke!
                    self.create_impact_particles(self.boss.x, self.boss.y)
                    self.create_debris_particles(self.boss.x, self.boss.y, count=50)
                    # Big explosion
                    for _ in range(5):
                        offset_x = random.uniform(-30, 30)
                        offset_y = random.uniform(-30, 30)
                        self.explosions.append(
                            Explosion(self.boss.x + offset_x, self.boss.y + offset_y)
                        )
                    self.score += self.boss.points
                    # Drop guaranteed power-up
                    powerup_types = [
                        "shield",
                        "rapid_fire",
                        "spread_shot",
                        "double_damage",
                        "magnet",
                        "time_slow",
                    ]
                    powerup_type_drop = random.choice(powerup_types)
                    self.powerups.append(
                        PowerUp(self.boss.x, self.boss.y, powerup_type_drop)
                    )
                    self.play_sound("explosion_big")
                    self.boss = None
                    # Update last boss spawn score to prevent immediate re-spawn
                    self.last_boss_spawn_score = self.score
                else:
                    # Just damaged, create impact
                    self.create_impact_particles(self.boss.x, self.boss.y)
            self.screen_shake = SCREEN_SHAKE_DURATION * 2
        else:
            # All other power-ups handled by manager
            self.powerup_manager.activate(powerup_type)
        self.play_sound("powerup")

    def create_laser_particles(self, x, y):
        """Create particles for laser trail."""
        for _ in range(2):
            color = random.choice(PARTICLE_COLORS["laser"])
            vx = random.uniform(-1, 1)
            vy = random.uniform(-1, 1)
            self.particles.append(Particle(x, y, color, vx, vy, size=2, lifetime=15))

    def create_debris_particles(self, x, y, count=10):
        """Create debris particles when asteroid breaks."""
        for _ in range(count):
            color = random.choice(PARTICLE_COLORS["debris"])
            angle = random.uniform(0, 360)
            speed = random.uniform(1, 4)
            vx = speed * math.cos(math.radians(angle))
            vy = speed * math.sin(math.radians(angle))
            size = random.randint(2, 4)
            self.particles.append(Particle(x, y, color, vx, vy, size, lifetime=40))

    def create_engine_particles(self, x, y):
        """Create engine thrust particles behind ship."""
        for _ in range(2):
            color = random.choice(PARTICLE_COLORS["engine"])
            vx = random.uniform(-3, -1)
            vy = random.uniform(-0.5, 0.5)
            size = random.randint(2, 3)
            self.particles.append(Particle(x, y, color, vx, vy, size, lifetime=10))

    def create_powerup_particles(self, x, y):
        """Create sparkle particles around power-ups."""
        angle = random.uniform(0, 360)
        speed = random.uniform(0.5, 1.5)
        vx = speed * math.cos(math.radians(angle))
        vy = speed * math.sin(math.radians(angle))
        color = random.choice(PARTICLE_COLORS["powerup"])
        self.particles.append(Particle(x, y, color, vx, vy, size=2, lifetime=20))

    def create_impact_particles(self, x, y):
        """Create impact particles when laser hits asteroid."""
        for _ in range(5):
            color = random.choice(PARTICLE_COLORS["impact"])
            angle = random.uniform(0, 360)
            speed = random.uniform(2, 5)
            vx = speed * math.cos(math.radians(angle))
            vy = speed * math.sin(math.radians(angle))
            self.particles.append(Particle(x, y, color, vx, vy, size=3, lifetime=15))

    def update(self):
        """Update all game objects."""
        # Only update if in playing state
        if self.game_state != "playing":
            return

        if self.game_over:
            # Transition to game_over state
            self.game_state = "game_over"
            if self.is_high_score():
                self.name_input_active = True
                self.player_name = ""
            return

        if self.paused:
            return

        # Update difficulty based on score milestones
        score_milestones = [0, 400, 1000, 2000, 3500, 5500, 8000, 11000, 15000, 20000,
                           26000, 33000, 41000, 50000, 60000, 71000, 83000, 90000, 95000, 98000, 100000]
        for i, milestone in enumerate(score_milestones):
            if self.score >= milestone:
                # Difficulty increases by 0.1 per milestone, caps at 3.0x at 100,000 points
                target_difficulty = 1.0 + (i * 0.1)
                self.difficulty_level = min(3.0, target_difficulty)

        # Check for boss spawn
        if self.boss is None and not self.boss_warning:
            # Spawn boss every BOSS_SPAWN_INTERVAL points
            if (
                self.score >= BOSS_SPAWN_INTERVAL
                and self.score - self.last_boss_spawn_score >= BOSS_SPAWN_INTERVAL
            ):
                self.boss_warning = True
                self.boss_warning_timer = BOSS_WARNING_DURATION
                self.last_boss_spawn_score = self.score
                self.play_sound("boss_warning")

        # Update boss warning
        if self.boss_warning:
            self.boss_warning_timer -= 1
            if self.boss_warning_timer <= 0:
                self.boss_warning = False
                # Spawn the boss with current difficulty
                patterns = ["sine", "circle", "figure8", "zigzag", "spiral"]
                pattern = random.choice(patterns)
                self.boss = Boss(pattern, self.difficulty_level)
                # Create distortion wave at boss spawn
                self.distortion_waves.append(DistortionWave(self.boss.x, self.boss.y))

        # Update ship
        keys = pygame.key.get_pressed()
        self.ship.update(keys)

        # Create engine particles when moving
        if (
            keys[pygame.K_w]
            or keys[pygame.K_s]
            or keys[pygame.K_a]
            or keys[pygame.K_d]
            or keys[pygame.K_UP]
            or keys[pygame.K_DOWN]
            or keys[pygame.K_LEFT]
            or keys[pygame.K_RIGHT]
        ):
            self.create_engine_particles(self.ship.x, self.ship.y)

        # Update laser cooldown
        if self.laser_cooldown > 0:
            self.laser_cooldown -= 1

        # Update power-up timers using manager
        self.powerup_manager.update()

        # Update combo timer
        if self.combo_timer > 0:
            self.combo_timer -= 1
            if self.combo_timer == 0:
                self.combo = 0

        # Update lasers
        for laser in self.lasers:
            laser.update()
            # Create laser trail particles (50% chance to reduce particle count)
            if random.random() < 0.5:
                self.create_laser_particles(laser.x, laser.y)
        self.lasers = [laser for laser in self.lasers if not laser.is_off_screen()]

        # Update asteroids
        time_scale = TIME_SLOW_MULTIPLIER if self.powerup_manager.is_active("time_slow") else 1.0
        for asteroid in self.asteroids:
            asteroid.update(time_scale)
        self.asteroids = [
            asteroid for asteroid in self.asteroids if not asteroid.is_off_screen()
        ]

        # Update boss
        if self.boss:
            self.boss.update()
            # Boss now stays on screen until defeated - no off-screen removal

        # Update power-ups
        for powerup in self.powerups:
            powerup.update()
            # Magnet effect - pull power-ups towards ship
            if self.powerup_manager.is_active("magnet"):
                ship_center = self.ship.get_center()
                dx = ship_center[0] - powerup.x
                dy = ship_center[1] - powerup.y
                distance = math.sqrt(dx**2 + dy**2)
                if distance > 0:
                    # Pull towards ship
                    powerup.x += (dx / distance) * MAGNET_PULL_SPEED
                    powerup.y += (dy / distance) * MAGNET_PULL_SPEED
            # Create sparkle particles around power-ups
            if random.random() < 0.3:  # 30% chance each frame
                self.create_powerup_particles(powerup.x, powerup.y)
        self.powerups = [
            powerup for powerup in self.powerups if not powerup.is_off_screen()
        ]

        # Spawn new asteroids
        self.asteroid_spawn_timer += 1
        spawn_freq = max(30, int(ASTEROID_SPAWN_FREQUENCY / self.difficulty_level))
        if (
            len(self.asteroids) < MAX_ASTEROIDS
            and self.asteroid_spawn_timer >= spawn_freq
        ):
            y = random.randint(0, HEIGHT - 100)
            radius = random.randint(ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS)
            self.asteroids.append(Asteroid(WIDTH, y, radius, self.difficulty_level))
            self.asteroid_spawn_timer = 0

        # Update explosions
        for explosion in self.explosions:
            explosion.update()
        self.explosions = [
            explosion for explosion in self.explosions if not explosion.is_finished()
        ]

        # Update stars
        for star in self.stars:
            star.update(self.paused)

        # Update particles
        for particle in self.particles:
            particle.update()
        self.particles = [
            particle for particle in self.particles if not particle.is_dead()
        ]

        # Update screen shake
        if self.screen_shake > 0:
            self.screen_shake -= 1
            self.shake_offset_x = random.randint(
                -SCREEN_SHAKE_INTENSITY, SCREEN_SHAKE_INTENSITY
            )
            self.shake_offset_y = random.randint(
                -SCREEN_SHAKE_INTENSITY, SCREEN_SHAKE_INTENSITY
            )
        else:
            self.shake_offset_x = 0
            self.shake_offset_y = 0

        # Update new visual systems
        for popup in self.score_popups:
            popup.update()
        self.score_popups = [p for p in self.score_popups if not p.is_dead()]

        for cloud in self.nebula_clouds:
            cloud.update()

        for wave in self.distortion_waves:
            wave.update()
        self.distortion_waves = [w for w in self.distortion_waves if not w.is_finished()]

        # Update scan line animation
        self.scan_line_offset = (self.scan_line_offset + SCAN_LINE_SPEED) % HEIGHT

        # Update theme color based on score
        if self.score < THEME_BLUE_MAX:
            self.theme_color = (100, 200, 255)  # Blue
        elif self.score < THEME_PURPLE_MAX:
            self.theme_color = (150, 100, 255)  # Purple
        else:
            self.theme_color = (255, 100, 150)  # Red/Pink

        # Check collisions
        self.check_collisions()

    def check_collisions(self):
        """Check all collision scenarios."""
        # Laser-asteroid collisions
        lasers_to_remove = []
        asteroids_to_remove = []

        asteroids_to_add = []  # For child asteroids

        for i, laser in enumerate(self.lasers):
            # Early exit: skip lasers already marked for removal (performance optimization)
            if i in lasers_to_remove:
                continue

            for j, asteroid in enumerate(self.asteroids):
                if laser.collides_with_asteroid(asteroid):
                    if i not in lasers_to_remove:
                        lasers_to_remove.append(i)
                    if j not in asteroids_to_remove:
                        asteroids_to_remove.append(j)
                        # Create explosion
                        self.explosions.append(Explosion(asteroid.x, asteroid.y))
                        # Create impact and debris particles
                        self.create_impact_particles(asteroid.x, asteroid.y)
                        self.create_debris_particles(
                            asteroid.x, asteroid.y, count=int(asteroid.radius / 3)
                        )
                        # Update combo
                        self.combo += 1
                        self.combo_timer = COMBO_TIMEOUT
                        # Calculate score with combo multiplier
                        multiplier_index = min(
                            self.combo - 1, len(COMBO_MULTIPLIERS) - 1
                        )
                        multiplier = COMBO_MULTIPLIERS[multiplier_index]
                        points = asteroid.points * multiplier
                        # Double damage doubles the points
                        if self.powerup_manager.is_active("double_damage"):
                            points *= 2
                        self.score += points
                        # Create score popup
                        self.score_popups.append(ScorePopup(asteroid.x, asteroid.y, int(points)))
                        # Break asteroid into smaller pieces if applicable
                        if asteroid.can_break():
                            children = asteroid.create_children(self.difficulty_level)
                            asteroids_to_add.extend(children)
                        # Spawn power-up chance
                        self.spawn_powerup(asteroid.x, asteroid.y)
                        self.play_sound("explosion")

        # Remove collided objects
        self.lasers = [
            laser for i, laser in enumerate(self.lasers) if i not in lasers_to_remove
        ]
        self.asteroids = [
            asteroid
            for i, asteroid in enumerate(self.asteroids)
            if i not in asteroids_to_remove
        ]

        # Add child asteroids from breaking (respect MAX_ASTEROIDS limit)
        available_slots = MAX_ASTEROIDS - len(self.asteroids)
        if available_slots > 0:
            self.asteroids.extend(asteroids_to_add[:available_slots])

        # Boss-laser collisions
        if self.boss:
            lasers_to_remove_boss = []
            for i, laser in enumerate(self.lasers):
                # Early exit: skip lasers already marked for removal
                if i in lasers_to_remove_boss:
                    continue

                if laser.collides_with_boss(self.boss):
                    if i not in lasers_to_remove_boss:
                        lasers_to_remove_boss.append(i)
                        # Update combo
                        self.combo += 1
                        self.combo_timer = COMBO_TIMEOUT
                        # Boss takes damage (double if power-up active)
                        damage = 2 if self.powerup_manager.is_active("double_damage") else 1
                        if self.boss.take_damage(damage):
                            # Boss defeated!
                            self.create_impact_particles(self.boss.x, self.boss.y)
                            self.create_debris_particles(
                                self.boss.x, self.boss.y, count=50
                            )
                            # Big explosion
                            for _ in range(5):
                                offset_x = random.uniform(-30, 30)
                                offset_y = random.uniform(-30, 30)
                                self.explosions.append(
                                    Explosion(
                                        self.boss.x + offset_x, self.boss.y + offset_y
                                    )
                                )
                            # Score points with combo multiplier
                            multiplier_index = min(
                                self.combo - 1, len(COMBO_MULTIPLIERS) - 1
                            )
                            multiplier = COMBO_MULTIPLIERS[multiplier_index]
                            self.score += self.boss.points * multiplier
                            # Drop guaranteed power-up
                            powerup_types = [
                                "shield",
                                "rapid_fire",
                                "spread_shot",
                                "double_damage",
                                "magnet",
                                "time_slow",
                            ]
                            powerup_type = random.choice(powerup_types)
                            self.powerups.append(
                                PowerUp(self.boss.x, self.boss.y, powerup_type)
                            )
                            # Huge screen shake
                            self.screen_shake = SCREEN_SHAKE_DURATION * 3
                            # Play big explosion sound
                            self.play_sound("explosion_big")
                            self.boss = None
                            # Update last boss spawn score to prevent immediate re-spawn
                            self.last_boss_spawn_score = self.score
                            # Exit loop - no more boss to hit
                            break
                        else:
                            # Just hit, create impact
                            self.create_impact_particles(self.boss.x, self.boss.y)
                            self.screen_shake = SCREEN_SHAKE_DURATION // 2
            # Remove lasers that hit boss
            self.lasers = [
                laser for i, laser in enumerate(self.lasers) if i not in lasers_to_remove_boss
            ]

        # Ship-asteroid collisions
        asteroid_to_remove = None
        for asteroid in self.asteroids:
            if asteroid.collides_with_ship(self.ship):
                # Take damage and check if shield absorbed it
                game_over, shield_absorbed = self.ship.take_damage()
                if game_over:
                    self.game_over = True
                else:
                    # Screen shake on hit
                    self.screen_shake = SCREEN_SHAKE_DURATION
                    # Play appropriate sound (shield break or hit)
                    if shield_absorbed:
                        self.play_sound("shield")
                    else:
                        self.play_sound("hit")
                    # Create explosion and debris particles
                    self.explosions.append(Explosion(asteroid.x, asteroid.y))
                    self.create_debris_particles(
                        asteroid.x, asteroid.y, count=int(asteroid.radius / 2)
                    )
                    # Break asteroid if applicable (even on ship collision)
                    if asteroid.can_break():
                        children = asteroid.create_children(self.difficulty_level)
                        # Add children after removing parent (respect MAX_ASTEROIDS limit)
                        available_slots = MAX_ASTEROIDS - len(self.asteroids)
                        for child in children[:available_slots]:
                            self.asteroids.append(child)
                    # Mark asteroid for removal (don't remove during iteration)
                    asteroid_to_remove = asteroid
                    # Reset combo
                    self.combo = 0
                    self.combo_timer = 0
                break

        # Remove asteroid after iteration
        if asteroid_to_remove:
            self.asteroids.remove(asteroid_to_remove)

        # Ship-boss collisions
        if self.boss and self.boss.collides_with_ship(self.ship):
            game_over, shield_absorbed = self.ship.take_damage()
            if game_over:
                self.game_over = True
            else:
                # Screen shake on hit
                self.screen_shake = SCREEN_SHAKE_DURATION * 2
                # Play appropriate sound (shield break or hit)
                if shield_absorbed:
                    self.play_sound("shield")
                else:
                    self.play_sound("hit")
                # Reset combo
                self.combo = 0
                self.combo_timer = 0

        # Ship-powerup collisions
        powerups_to_remove = []
        for i, powerup in enumerate(self.powerups):
            if powerup.collides_with_ship(self.ship):
                self.activate_powerup(powerup.type)
                powerups_to_remove.append(i)
        # Remove collected power-ups
        self.powerups = [
            powerup for i, powerup in enumerate(self.powerups) if i not in powerups_to_remove
        ]

    def draw(self):
        """Draw all game objects and UI based on game state."""
        if self.game_state == "menu":
            self.draw_menu()
        elif self.game_state == "highscores":
            self.draw_highscores()
        elif self.game_state == "options":
            self.draw_options()
        elif self.game_state == "playing":
            self.draw_game()
        elif self.game_state == "game_over":
            self.draw_game()  # Show game in background
            self.draw_game_over_screen()

        # Update display
        pygame.display.flip()

    def draw_game(self):
        """Draw the actual game (playing state)."""
        # Create offset surface for screen shake
        offset_screen = pygame.Surface((WIDTH, HEIGHT))
        offset_screen.fill(BACKGROUND)

        # Draw nebula clouds in background
        for cloud in self.nebula_clouds:
            cloud.draw(offset_screen)

        # Draw stars
        for star in self.stars:
            star.draw(offset_screen)

        # Draw particles
        for particle in self.particles:
            particle.draw(offset_screen)

        # Draw explosions
        for explosion in self.explosions:
            explosion.draw(offset_screen)

        # Draw asteroids
        for asteroid in self.asteroids:
            asteroid.draw(offset_screen)

        # Draw boss
        if self.boss:
            self.boss.draw(offset_screen)

        # Draw power-ups
        for powerup in self.powerups:
            powerup.draw(offset_screen)

        # Draw lasers
        for laser in self.lasers:
            laser.draw(offset_screen)

        # Draw ship
        self.ship.draw(offset_screen)

        # Draw score popups
        for popup in self.score_popups:
            popup.draw(offset_screen)

        # Draw distortion waves
        for wave in self.distortion_waves:
            wave.draw(offset_screen)

        # Draw UI
        self.draw_ui(offset_screen)

        # Draw pause screen
        if self.paused:
            self.draw_pause(offset_screen)

        # Apply vignette effect
        offset_screen.blit(self.vignette_surface, (0, 0))

        # Apply chromatic aberration during screen shake
        if self.screen_shake > 0:
            # Create chromatic aberration by offsetting RGB channels
            aberration_intensity = 3
            # Create separate surfaces for each channel
            red_surface = pygame.Surface((WIDTH, HEIGHT))
            red_surface.fill((0, 0, 0))
            red_surface.blit(offset_screen, (aberration_intensity, 0))

            green_surface = pygame.Surface((WIDTH, HEIGHT))
            green_surface.fill((0, 0, 0))
            green_surface.blit(offset_screen, (0, 0))

            blue_surface = pygame.Surface((WIDTH, HEIGHT))
            blue_surface.fill((0, 0, 0))
            blue_surface.blit(offset_screen, (-aberration_intensity, 0))

            # Extract and combine channels (simplified chromatic effect)
            # Just use additive blending for the effect
            offset_screen.blit(red_surface, (0, 0), special_flags=pygame.BLEND_RGB_ADD)

        # Add boss fight red tint overlay
        if self.boss is not None:
            tint_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            tint_alpha = 30  # Subtle red tint
            tint_surface.fill((255, 50, 50, tint_alpha))
            offset_screen.blit(tint_surface, (0, 0))

        # Blit offset screen with shake
        self.screen.blit(offset_screen, (self.shake_offset_x, self.shake_offset_y))

    def draw_menu(self):
        """Draw the main menu."""
        self.screen.fill(BACKGROUND)

        # Draw animated stars in background
        for star in self.stars:
            star.update(paused=False)
            star.draw(self.screen)

        # Draw title
        title_text = self.title_font.render("SPACE SHOOTER", True, TEXT_COLOR)
        self.screen.blit(
            title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4)
        )

        # Draw subtitle
        subtitle_text = self.small_font.render(
            "Blast Asteroids • Collect Power-Ups • Battle Bosses", True, TEXT_COLOR
        )
        self.screen.blit(
            subtitle_text, (WIDTH // 2 - subtitle_text.get_width() // 2, HEIGHT // 4 + 80)
        )

        # Draw menu options
        menu_start_y = HEIGHT // 2 - 20
        for i, option in enumerate(self.menu_options):
            # Highlight selected option
            if i == self.menu_selected:
                color = COMBO_COLOR
                text = self.large_font.render(f"> {option} <", True, color)
            else:
                color = TEXT_COLOR
                text = self.font.render(option, True, color)

            text_x = WIDTH // 2 - text.get_width() // 2
            text_y = menu_start_y + i * 60
            self.screen.blit(text, (text_x, text_y))

        # Draw controls hint
        controls_text = self.small_font.render(
            "W/S or Up/Down Arrow Keys to navigate • ENTER to select", True, TEXT_COLOR
        )
        self.screen.blit(
            controls_text,
            (WIDTH // 2 - controls_text.get_width() // 2, HEIGHT - 60),
        )

    def draw_highscores(self):
        """Draw the highscores screen."""
        self.screen.fill(BACKGROUND)

        # Draw animated stars in background
        for star in self.stars:
            star.update(paused=False)
            star.draw(self.screen)

        # Draw title
        title_text = self.title_font.render("HIGH SCORES", True, COMBO_COLOR)
        self.screen.blit(
            title_text, (WIDTH // 2 - title_text.get_width() // 2, 50)
        )

        # Draw high scores
        start_y = 150
        if len(self.high_scores) == 0:
            no_scores_text = self.font.render(
                "No high scores yet!", True, TEXT_COLOR
            )
            self.screen.blit(
                no_scores_text,
                (WIDTH // 2 - no_scores_text.get_width() // 2, start_y + 100),
            )
        else:
            for i, (score, name) in enumerate(self.high_scores):
                # Rank
                rank_text = self.font.render(f"{i + 1}.", True, TEXT_COLOR)
                # Name
                name_text = self.font.render(name, True, TEXT_COLOR)
                # Score
                score_text = self.font.render(str(score), True, COMBO_COLOR)

                y_pos = start_y + i * 40
                self.screen.blit(rank_text, (WIDTH // 4 - 30, y_pos))
                self.screen.blit(name_text, (WIDTH // 4, y_pos))
                self.screen.blit(score_text, (WIDTH // 2 + 100, y_pos))

        # Draw back hint
        back_text = self.small_font.render(
            "Press ENTER or ESC to return", True, TEXT_COLOR
        )
        self.screen.blit(
            back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT - 60)
        )

    def draw_options(self):
        """Draw the options screen."""
        self.screen.fill(BACKGROUND)

        # Draw animated stars in background
        for star in self.stars:
            star.update(paused=False)
            star.draw(self.screen)

        # Draw title
        title_text = self.title_font.render("OPTIONS", True, TEXT_COLOR)
        self.screen.blit(
            title_text, (WIDTH // 2 - title_text.get_width() // 2, 50)
        )

        # Options start position
        start_y = 200

        # Volume slider
        volume_label = self.font.render("Volume", True, TEXT_COLOR)
        if self.options_selected == 0:
            volume_label = self.large_font.render("> Volume <", True, COMBO_COLOR)
        self.screen.blit(
            volume_label, (WIDTH // 2 - volume_label.get_width() // 2, start_y)
        )

        # Draw volume slider
        slider_y = start_y + 60
        slider_x = WIDTH // 2 - 150
        slider_width = 300
        slider_height = 20

        # Slider background
        pygame.draw.rect(
            self.screen, (50, 50, 50), (slider_x, slider_y, slider_width, slider_height)
        )

        # Slider fill
        fill_width = int(slider_width * self.volume)
        pygame.draw.rect(
            self.screen, COMBO_COLOR, (slider_x, slider_y, fill_width, slider_height)
        )

        # Slider border
        pygame.draw.rect(
            self.screen, TEXT_COLOR, (slider_x, slider_y, slider_width, slider_height), 2
        )

        # Volume percentage
        volume_percent = int(self.volume * 100)
        volume_text = self.font.render(f"{volume_percent}%", True, TEXT_COLOR)
        self.screen.blit(
            volume_text, (WIDTH // 2 - volume_text.get_width() // 2, slider_y + 30)
        )

        # Mute toggle
        mute_y = start_y + 150
        mute_status = "ON" if self.muted else "OFF"
        mute_color = GAME_OVER_COLOR if self.muted else POWERUP_COLORS["shield"]

        if self.options_selected == 1:
            mute_label = self.large_font.render(f"> Mute: {mute_status} <", True, COMBO_COLOR)
        else:
            mute_label = self.font.render(f"Mute: {mute_status}", True, mute_color)

        self.screen.blit(
            mute_label, (WIDTH // 2 - mute_label.get_width() // 2, mute_y)
        )

        # Instructions
        controls_text = self.small_font.render(
            "W/S or Up/Down Arrow Keys: Navigate • A/D or Left/Right Arrow Keys: Adjust • ENTER: Toggle Mute", True, TEXT_COLOR
        )
        self.screen.blit(
            controls_text, (WIDTH // 2 - controls_text.get_width() // 2, HEIGHT - 100)
        )

        back_text = self.small_font.render(
            "Press ESC to return", True, TEXT_COLOR
        )
        self.screen.blit(
            back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT - 60)
        )

    def draw_game_over_screen(self):
        """Draw game over overlay on top of game."""
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # Game over message
        game_over_text = self.font.render("GAME OVER!", True, GAME_OVER_COLOR)
        self.screen.blit(
            game_over_text,
            (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 80),
        )

        # Final score
        final_score_text = self.font.render(
            f"Final Score: {self.score}", True, TEXT_COLOR
        )
        self.screen.blit(
            final_score_text,
            (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 - 30),
        )

        # Name input for new high score
        if self.name_input_active:
            prompt_text = self.font.render(
                "New High Score! Enter your name:", True, TEXT_COLOR
            )
            self.screen.blit(
                prompt_text,
                (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2 + 20),
            )

            # Name input field
            pygame.draw.rect(
                self.screen, (50, 50, 100), (WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 40)
            )
            name_display = self.small_font.render(self.player_name, True, TEXT_COLOR)
            self.screen.blit(name_display, (WIDTH // 2 - 100 + 10, HEIGHT // 2 + 65))

            # Blinking cursor
            if pygame.time.get_ticks() % 1000 < 500:
                cursor_x = WIDTH // 2 - 100 + 10 + name_display.get_width()
                pygame.draw.line(
                    self.screen,
                    TEXT_COLOR,
                    (cursor_x, HEIGHT // 2 + 65),
                    (cursor_x, HEIGHT // 2 + 95),
                    2,
                )

            # Instructions
            enter_text = self.small_font.render("Press ENTER to save", True, TEXT_COLOR)
            self.screen.blit(
                enter_text,
                (WIDTH // 2 - enter_text.get_width() // 2, HEIGHT // 2 + 110),
            )
        else:
            # Instructions
            restart_text = self.font.render("Press R to restart", True, TEXT_COLOR)
            self.screen.blit(
                restart_text,
                (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20),
            )

            # Exit to menu hint
            menu_text = self.small_font.render("Press ESC for menu", True, TEXT_COLOR)
            self.screen.blit(
                menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 + 60)
            )

    def draw_ui(self, screen):
        """Draw score and UI elements with enhancements."""
        # Draw holographic scan lines
        scan_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for i in range(0, HEIGHT, 4):
            scan_y = (i + self.scan_line_offset) % HEIGHT
            alpha = 20
            pygame.draw.line(scan_surface, (self.theme_color[0], self.theme_color[1], self.theme_color[2], alpha),
                           (0, scan_y), (WIDTH, scan_y), 1)
        screen.blit(scan_surface, (0, 0))

        # Draw score with theme color
        score_text = self.font.render(f"Score: {self.score}", True, self.theme_color)
        screen.blit(score_text, (20, 20))

        # Draw high score (top score from leaderboard)
        if self.high_scores:
            high_score, high_score_player = self.high_scores[0]
            high_score_text = self.font.render(
                f"High Score: {high_score}", True, TEXT_COLOR
            )
            screen.blit(high_score_text, (WIDTH - high_score_text.get_width() - 20, 20))

            # Draw high score player name
            player_text = self.small_font.render(
                f"By: {high_score_player}", True, TEXT_COLOR
            )
            screen.blit(player_text, (WIDTH - player_text.get_width() - 20, 50))

        # Draw lives with pulse when low
        lives_color = HEALTH_COLOR
        if self.ship.lives == 1:
            # Pulse health bar when low
            pulse = (math.sin(pygame.time.get_ticks() / 100.0) + 1) / 2
            lives_color = (255, int(100 + pulse * 155), int(100 + pulse * 155))
        lives_text = self.font.render(f"Lives: {self.ship.lives}", True, lives_color)
        screen.blit(lives_text, (20, 60))

        # Draw difficulty multiplier
        difficulty_text = self.small_font.render(
            f"Speed: {self.difficulty_level:.1f}x", True, (255, 200, 100)
        )
        screen.blit(difficulty_text, (20, 90))

        # Draw combo with scale pulse and screen edge glow
        if self.combo > 1:
            multiplier_index = min(self.combo - 1, len(COMBO_MULTIPLIERS) - 1)
            multiplier = COMBO_MULTIPLIERS[multiplier_index]

            # Scale pulse when combo increases
            scale_factor = 1.0
            if self.combo > self.previous_combo:
                # Pulse effect on combo increase
                scale_factor = 1.0 + 0.3 * math.exp(-COMBO_PULSE_SPEED * (self.combo - self.previous_combo))
                self.previous_combo = self.combo

            combo_font_size = int(36 * scale_factor)
            combo_font = pygame.font.SysFont(None, combo_font_size)
            combo_text = combo_font.render(f"COMBO x{multiplier}!", True, COMBO_COLOR)
            screen.blit(combo_text, (WIDTH // 2 - combo_text.get_width() // 2, 20))

            # Screen edge glow for high combos
            if self.combo >= 3:
                edge_alpha = int(50 + 30 * (self.combo / len(COMBO_MULTIPLIERS)))
                edge_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                # Top and bottom edges
                for i in range(10):
                    alpha = max(0, min(255, int(edge_alpha * (1.0 - i / 10.0))))
                    pygame.draw.rect(edge_surface, (255, 255, 100, alpha), (0, i * 2, WIDTH, 2))
                    pygame.draw.rect(edge_surface, (255, 255, 100, alpha), (0, HEIGHT - i * 2, WIDTH, 2))
                screen.blit(edge_surface, (0, 0))

        # Draw active power-ups with progress bars
        y_offset = 120
        powerup_bar_width = 150
        powerup_bar_height = 8

        # Helper function to draw power-up with progress bar
        def draw_powerup_with_bar(name, timer, max_timer, color, y_pos):
            # Text
            text = self.small_font.render(
                f"{name}: {timer // FPS}s", True, color
            )
            screen.blit(text, (20, y_pos))

            # Progress bar background
            bar_x = 20
            bar_y = y_pos + 20
            pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, powerup_bar_width, powerup_bar_height))

            # Progress bar fill
            progress = timer / max_timer
            fill_width = int(powerup_bar_width * progress)
            pygame.draw.rect(screen, color, (bar_x, bar_y, fill_width, powerup_bar_height))

            # Progress bar border
            pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, powerup_bar_width, powerup_bar_height), 1)

            return y_pos + 35

        if self.powerup_manager.is_active("rapid_fire"):
            y_offset = draw_powerup_with_bar(
                "Rapid Fire",
                self.powerup_manager.get_timer('rapid_fire'),
                POWERUP_DURATION * 2,
                POWERUP_COLORS["rapid_fire"],
                y_offset
            )

        if self.powerup_manager.is_active("spread_shot"):
            y_offset = draw_powerup_with_bar(
                "Spread Shot",
                self.powerup_manager.get_timer('spread_shot'),
                POWERUP_DURATION * 2,
                POWERUP_COLORS["spread_shot"],
                y_offset
            )

        if self.powerup_manager.is_active("shield"):
            y_offset = draw_powerup_with_bar(
                "Shield",
                self.powerup_manager.get_timer('shield'),
                SHIELD_DURATION * 2,
                POWERUP_COLORS["shield"],
                y_offset
            )

        if self.powerup_manager.is_active("double_damage"):
            y_offset = draw_powerup_with_bar(
                "Double Damage",
                self.powerup_manager.get_timer('double_damage'),
                POWERUP_DURATION * 2,
                POWERUP_COLORS["double_damage"],
                y_offset
            )

        if self.powerup_manager.is_active("magnet"):
            y_offset = draw_powerup_with_bar(
                "Magnet",
                self.powerup_manager.get_timer('magnet'),
                POWERUP_DURATION * 2,
                POWERUP_COLORS["magnet"],
                y_offset
            )

        if self.powerup_manager.is_active("time_slow"):
            y_offset = draw_powerup_with_bar(
                "Time Slow",
                self.powerup_manager.get_timer('time_slow'),
                POWERUP_DURATION * 2,
                POWERUP_COLORS["time_slow"],
                y_offset
            )

        # Draw boss health bar
        if self.boss:
            # Health bar background
            bar_x = (WIDTH - BOSS_HEALTHBAR_WIDTH) // 2
            bar_y = 60
            pygame.draw.rect(
                screen,
                (50, 50, 50),
                (bar_x, bar_y, BOSS_HEALTHBAR_WIDTH, BOSS_HEALTHBAR_HEIGHT),
            )

            # Health bar fill
            health_ratio = self.boss.health / self.boss.max_health
            health_width = int(BOSS_HEALTHBAR_WIDTH * health_ratio)
            health_color = (255, int(255 * health_ratio), int(255 * health_ratio))
            pygame.draw.rect(
                screen,
                health_color,
                (bar_x, bar_y, health_width, BOSS_HEALTHBAR_HEIGHT),
            )

            # Health bar border
            pygame.draw.rect(
                screen,
                (255, 255, 255),
                (bar_x, bar_y, BOSS_HEALTHBAR_WIDTH, BOSS_HEALTHBAR_HEIGHT),
                2,
            )

            # Boss label
            boss_label = self.font.render("BOSS", True, BOSS_COLOR)
            screen.blit(boss_label, (bar_x - boss_label.get_width() - 10, bar_y - 5))

            # Health text
            health_text = self.small_font.render(
                f"{self.boss.health}/{self.boss.max_health}", True, TEXT_COLOR
            )
            screen.blit(
                health_text,
                (
                    bar_x + BOSS_HEALTHBAR_WIDTH // 2 - health_text.get_width() // 2,
                    bar_y + 2,
                ),
            )

        # Draw boss warning
        if self.boss_warning:
            warning_alpha = int(200 * abs(math.sin(self.boss_warning_timer / 10)))
            warning_surface = pygame.Surface((WIDTH, 100), pygame.SRCALPHA)
            warning_text = self.font.render(
                "WARNING! BOSS APPROACHING!", True, (255, 0, 0, warning_alpha)
            )
            warning_surface.blit(
                warning_text, (WIDTH // 2 - warning_text.get_width() // 2, 40)
            )
            screen.blit(warning_surface, (0, HEIGHT // 2 - 50))

        # Draw controls
        controls_text = self.small_font.render(
            "WASD/Arrows: Move | SPACE: Shoot | ESC: Pause", True, TEXT_COLOR
        )
        screen.blit(controls_text, (20, HEIGHT - 40))

    def draw_pause(self, screen):
        """Draw pause overlay with menu."""
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # Pause text
        pause_text = self.large_font.render("PAUSED", True, PAUSE_COLOR)
        screen.blit(
            pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 100)
        )

        # Draw pause menu options
        menu_start_y = HEIGHT // 2
        for i, option in enumerate(self.pause_options):
            # Highlight selected option
            if i == self.pause_selected:
                color = COMBO_COLOR
                text = self.large_font.render(f"> {option} <", True, color)
            else:
                color = TEXT_COLOR
                text = self.font.render(option, True, color)

            text_x = WIDTH // 2 - text.get_width() // 2
            text_y = menu_start_y + i * 60
            screen.blit(text, (text_x, text_y))

        # Controls hint
        controls_text = self.small_font.render(
            "W/S or Up/Down Arrow Keys • ENTER to select • ESC to resume", True, TEXT_COLOR
        )
        screen.blit(
            controls_text, (WIDTH // 2 - controls_text.get_width() // 2, HEIGHT - 80)
        )


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
