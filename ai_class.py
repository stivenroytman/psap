import numpy as np


class AI:
    """PSAP AI class"""

    def __init__(self):

        """Counters"""
        self.points = 0
        self.defense_blocks = list()

        """Timers"""
        self.choice_timer = 0  # what: time for choice to be executed
        self.earned_point_animation_timer = 0
        self.provoked_animation_timer = 0

        """Binary Variables"""
        self.choice_cooldown = 0  # what: indicates that a choice is being executed
        self.stole_point = 0

        """Qualitative Variables"""
        self.choice = 0  # what: indicates which choice was made

    # ------------------------------------------------------------------------------------------------

    """Functions"""

    def ai_choose(self, aggression):
        """Make a decision about which option to pursue"""
        other = (1 - aggression) / 2
        choice = np.random.choice(a=[1, 2, 3], p=[other, aggression, other])
        self.choice = choice

    def manage_choice_result(self, choice1_delay_mean=15, choice1_delay_sd=2,
                             choice2_delay_mean=5, choice2_delay_sd=1,
                             choice3_delay_mean=5, choice3_delay_sd=1):
        """Set timer appropriately based on choice."""
        if self.choice == 1:
            self.choice_timer = np.random.normal(choice1_delay_mean, choice1_delay_sd, 1)[0]
        elif self.choice == 2:
            self.choice_timer = np.random.normal(choice2_delay_mean, choice2_delay_sd, 1)[0]
        elif self.choice == 3:
            self.choice_timer = np.random.normal(choice3_delay_mean, choice3_delay_sd, 1)[0]
        self.choice_cooldown = 1

    def manage_choice_timer(self, external_tic, earned_animation_duration=1,
                            defense_duration_mean=30, defense_duration_sd=5):
        """Execute choice effects upon timer completion."""
        #  what(external_tic): global tic variable from timekeeping
        if self.choice_timer <= 0:
            self.choice_timer = 0
            if self.choice == 1:
                self.points += 1
                self.earned_point_animation_timer = earned_animation_duration
            if self.choice == 2:
                self.stole_point = 1
            if self.choice == 3:
                self.defense_blocks = np.append(self.defense_blocks, np.random.normal(defense_duration_mean, defense_duration_sd, 1))
            self.choice_cooldown = 0
            self.choice = 0
        else:
            self.choice_timer -= external_tic

    def timekeeping(self, tic):

        if len(self.defense_blocks) > 0:
            self.defense_blocks[0] -= tic
            self.defense_blocks = np.delete(self.defense_blocks, np.where(self.defense_blocks <= [0]))

        if self.provoked_animation_timer > 0:
            self.provoked_animation_timer -= tic
        else:
            self.provoked_animation_timer = 0

        if self.earned_point_animation_timer > 0:
            self.earned_point_animation_timer -= tic
        else:
            self.earned_point_animation_timer = 0
