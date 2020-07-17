import numpy as np


class Player:
    """PSAP player class"""

    def __init__(self):

        """Counters"""
        self.counters = {'1': 0, '2': 0, '3': 0}
        self.choice_dump_total = {'1': 0, '2': 0, '3': 0}
        self.active_counter = 0
        self.count = 0
        self.points = 0
        self.defense_blocks = np.array([])

        """Timers"""
        self.provoked_animation_timer = 0
        self.earned_point_animation_timer = 0
        self.choice_dump_animation_timer = 0

        """T/F Variables"""
        self.choice_dump = 0
        self.stole_point = 0
        self.provoked = 0

        """Exclusively Data Outputs"""
        self.counters_data_output = {'1': 0, '2': 0, '3': 0}  # changed
        self.defense_blocks_data = np.array([])
        self.provoked_total = 0
        self.provoked_timer = 0
        self.dumps = []
        self.choice_dumped = 0  # TODO: see if necessary

    def counter_update(self, counter, dump_animation_duration=0.5):
        """Update counter values on button press."""
        for counter_number in self.counters.keys():
            if counter_number != counter:
                if self.counters[counter_number] > 0:
                    self.choice_dump = 1
                    if self.provoked == 1:
                        self.dumps.append((counter_number, counter, self.counters[counter_number]))
                        self.provoked_timer = 0
                        self.provoked = 0
                    else:
                        self.dumps.append((counter_number, counter, "NA"))
                    # changed: deleted choice_dumped update
                    # TODO: see if it's necessary and possibly delete
                    self.choice_dump_total[counter_number] += 1
                    self.choice_dump_animation_timer = dump_animation_duration
                self.counters[counter_number] = 0
            else:
                self.counters[counter_number] += 1
                self.counters_data_output[counter_number] += 1  # changed
                self.active_counter = counter_number
                self.count = self.counters[counter_number]

    def condition_check(self, tic, condition1=100, condition2=10, condition3=10, earned_animation_duration=1,
                        defense_duration_mean=30,
                        defense_duration_sd=5):
        """Implement counter completion effects"""
        if self.counters['1'] == condition1:  # changed: added provoked negation from fulfilling any condition
            self.provoked = 0
            self.provoked_timer = 0
            self.points += 1
            self.earned_point_animation_timer = earned_animation_duration
            self.counters['1'] = 0
        if self.counters['2'] == condition2:
            self.provoked = 0
            self.provoked_timer = 0
            self.stole_point = 1
            self.counters['2'] = 0
        if self.counters['3'] == condition3: # changed
            self.provoked = 0
            self.provoked_timer = 0
            block_value = abs(np.random.normal(defense_duration_mean, defense_duration_sd, 1))
            self.defense_blocks = np.append(self.defense_blocks, block_value)
            self.defense_blocks_data = np.append(self.defense_blocks_data, block_value)
            self.counters['3'] = 0

    def timekeeping(self, tic):

        if self.provoked == 1:
            self.provoked_timer += tic
        else:
            self.provoked_timer = 0

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

        if self.choice_dump_animation_timer > 0:
            self.choice_dump_animation_timer -= tic
        else:
            self.choice_dump_animation_timer = 0
