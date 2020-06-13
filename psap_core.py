import datetime
import pygame
import numpy as np
import pickle
from ai_class import AI
from player_class import Player
from object_print_class import ObjectPrint
from object_print_class import FlashingObject
from psap_parameters import *
# -------------------------------------------------------------------------------------------------

"""Initialize pygame modules"""
pygame.init()

def psap(participant_name, opponent_image_name):
    """Initialize the game screen"""
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption(screen_name)

    """Initialize clock variables"""
    clock = pygame.time.Clock()
    safe_period = 0

    """Initialize game phases"""
    phase = 0
    phase_timer = 0
    start = ObjectPrint(start_message, start_message_fontsize, start_message_x, start_message_y, screen)
    practice = ObjectPrint(practice_opponent_name, practice_opponent_fontsize, practice_opponent_x, practice_opponent_y,
                           screen)
    transition = ObjectPrint(transition_message, transition_message_fontsize, transition_message_x, transition_message_y,
                             screen)
    end = ObjectPrint(end_message, end_message_fontsize, end_message_x, end_message_y, screen)

    """Initialize AI variables"""
    opponent = AI()
    screen_opponent_name = ObjectPrint(opponent_name, opponent_name_fontsize, opponent_name_x, opponent_name_y, screen)
    screen_opponent_points = FlashingObject(opponent.points, opponent_points_fontsize, opponent_points_x, opponent_points_y,
                                            screen)

    opponent_image = pygame.image.load(opponent_image_name)
    """Initialize Player variables"""
    participant = Player()
    screen_player_name = ObjectPrint(participant_name, participant_name_fontsize, participant_name_x, participant_name_y,
                                     screen)
    screen_player_points = FlashingObject(participant.points, participant_points_fontsize, participant_points_x,
                                          participant_points_y, screen)

    """Initialize interface variables"""
    screen_counter = FlashingObject(participant.count, counter_fontsize, counter_x, counter_y, screen)
    screen_choice_1 = ObjectPrint('1', indicators_fontsize, indicators_x, indicators_y, screen)
    screen_choice_2 = ObjectPrint('2', indicators_fontsize, indicators_x + indicator_spacing, indicators_y, screen)
    screen_choice_3 = ObjectPrint('3', indicators_fontsize, indicators_x + (2 * indicator_spacing), indicators_y, screen)
    defense_meter_label = ObjectPrint(meter_label, meter_label_fontsize, meter_label_x, meter_label_y, screen)
    choice_list = [screen_choice_1, screen_choice_2, screen_choice_3]

    """DATA OUTPUT"""
    data = {'1': {}, '2': {}, '3': {}}

    """Functions"""


    def game_screen_display(tic, screen_player_points, screen_opponent_points, opponent, participant,
                            screen_counter, screen_choice_1, screen_choice_2, screen_choice_3,
                            screen_opponent_name, screen_player_name, choice_list):
        if participant_earned_animation:
            screen_player_points.begin_flashing(participant.earned_point_animation_timer, 'pos')
        if participant_provoked_animation:
            screen_player_points.begin_flashing(participant.provoked_animation_timer, 'neg')
        if opponent_earned_animation:
            screen_opponent_points.begin_flashing(opponent.earned_point_animation_timer, 'pos')
        if opponent_provoked_animation:
            screen_opponent_points.begin_flashing(opponent.provoked_animation_timer, 'neg')
        screen_player_points.flashing_check(tic)
        screen_opponent_points.flashing_check(tic)
        if participant_choice_dump_animation:
            if participant.choice_dump_animation_timer > 0:
                screen_counter.font_color = (255, 0, 0)
            else:
                screen_counter.font_color = (0, 0, 0)
        # USE: Light up active counter.
        if active_counter_animation:
            for choice in choice_list:
                if choice.content == participant.active_counter:
                    choice.font_color = (0, 255, 0)  # choose active counter color
                else:
                    choice.font_color = (0, 0, 0)
        # Display objects
        if meter_print:
            defense_meter_label.display_object()
        if opponent_points_print:
            screen_opponent_points.display_object()
        if counter_print:
            screen_counter.display_object()
        if indicators_print:
            screen_choice_1.display_object()
            screen_choice_2.display_object()
            screen_choice_3.display_object()
        if opponent_name_print:
            screen_opponent_name.display_object()
        if participant_name_print:
            screen_player_name.display_object()
        if participant_points_print:
            screen_player_points.display_object()
        if opponent_image_print:
            screen.blit(opponent_image, (opponent_image_x, opponent_image_y))


    def get_block_quantities(number):
        hundreds = number // 100
        number -= (100 * hundreds)
        tens = number // 10
        ones = number % 10
        return [hundreds, tens, ones]


    def print_meters(block_list, screen, meter_x, meter_y, block_spacing_x, block_spacing_y, hundreds_block_color,
                     tens_block_color, ones_block_color, block_width, block_height):
        if meter_print:
            for block in range(block_list[0]):
                pygame.draw.rect(screen, pygame.Color(hundreds_block_color),
                                 (meter_x + (block_spacing_x * block), meter_y, block_width, block_height))
            for block in range(block_list[1]):
                pygame.draw.rect(screen, pygame.Color(tens_block_color), (
                meter_x + (block_spacing_x * block), meter_y + block_spacing_y, block_width, block_height))
            for block in range(block_list[2]):
                pygame.draw.rect(screen, pygame.Color(ones_block_color), (
                meter_x + (block_spacing_x * block), meter_y + (2 * block_spacing_y), block_width, block_height))


    # ----------------------------------------------------------------------------------------------------------------------
    """Game Loop"""
    running = True
    while running:
        tic = clock.tick(30) / 1000
        screen.fill((255, 255, 255))
        for event in pygame.event.get():

            #   ALL THE OUTPUT THING GO HERE
            if event.type == pygame.QUIT:
                print(phase)
                running = False
            # ----------------------------------------------------------------------------------------------------------------------
            """Keydown events"""
            if event.type == pygame.KEYDOWN:

                if phase % 2 == 0:
                    # TODO: write dictionary data to dataframe here or in phase section
                    # changed: deleted player and AI resets, moved them to press n below
                    # changed: deleted graphical functions below to check if they are necessary
                    if event.key == pygame.K_n:
                        if phase < 8:
                            participant = Player()
                            opponent = AI()
                            screen_player_points = FlashingObject(participant.points, participant_points_fontsize,
                                                                  participant_points_x, participant_points_y, screen)
                            screen_opponent_points = FlashingObject(opponent.points, opponent_points_fontsize,
                                                                    opponent_points_x,
                                                                    opponent_points_y, screen)
                            screen_counter = FlashingObject(participant.count, counter_fontsize, counter_x, counter_y,
                                                            screen)
                            phase += 1
                            if phase == 1:
                                phase_timer = practice_phase_duration
                                opponent.points = practice_opponent_points
                            else:
                                phase_timer = block_phase_duration
                                safe_period = safe_period_default

                if event.key == pygame.K_ESCAPE:
                    data_file_name = participant_name + "_"  + \
                        str(datetime.datetime.now())\
                        .replace(" ", "_").replace(":", "_").replace(".", "_").replace("-", "_") + ".pickle"
                    data_file = open(data_file_name, 'ab')
                    pickle.dump(data, data_file)
                    data_file.close()
                    pygame.display.quit()
                    running = False

                if not phase % 2 == 0:
                    if event.key == pygame.K_KP1:
                        participant.counter_update('1')

                    if event.key == pygame.K_KP2:
                        participant.counter_update('2')

                    if event.key == pygame.K_KP3:
                        participant.counter_update('3')
        # ---------------------------------------------------------------------------------------------------------------------
        if phase == 0:  # PHASE: start
            if start_message_print:
                start.display_object()
            pygame.display.update()
            continue
        # ---------------------------------------------------------------------------------------------------------------------
        if phase == 1:  # PHASE: practice
            phase_timer -= tic  # TODO: code smell
            if phase_timer <= 0: phase += 1  # TODO: code smell

            participant.timekeeping(tic)
            opponent.timekeeping(tic)
            participant.condition_check(tic, option1_presses, option2_presses, option3_presses,
                                        participant_earned_animation_duration, participant_defense_duration_mean,
                                        participant_defense_duration_sd)

            # use: participant stealing points
            if participant.stole_point == 1 and len(opponent.defense_blocks) <= 0 < opponent.points:
                """Successful point steal"""
                opponent.points -= 1
                opponent.provoked_animation_timer = opponent_provoked_animation_duration
                participant.stole_point = 0
            else:
                participant.stole_point = 0

            """ObjectPrint content updates"""
            screen_player_points.content = participant.points
            screen_counter.content = participant.count
            screen_opponent_points.content = opponent.points

            print_meters(get_block_quantities(len(participant.defense_blocks)), screen, meter_x, meter_y, block_spacing_x,
                         block_spacing_y, hundreds_block_color, tens_block_color, ones_block_color, block_width,
                         block_height)

            game_screen_display(tic, screen_player_points, screen_opponent_points, opponent, participant,
                                screen_counter, screen_choice_1, screen_choice_2, screen_choice_3,
                                practice, screen_player_name, choice_list)

            pygame.display.update()
            continue
        # ----------------------------------------------------------------------------------------------------------------------
        if phase % 2 == 0:  # PHASE: transition
            if phase > 2:
                data[str((int(phase / 2) - 1))]['player_points'] = participant.points
                data[str((int(phase / 2) - 1))]['total_presses'] = participant.counters_data_output
                data[str((int(phase / 2) - 1))]['player_provoked'] = participant.provoked_total
                data[str((int(phase / 2) - 1))]['dumps'] = participant.dumps
                # TODO: remove the seconds latency, add number of clicks on the dumped counter
                data[str((int(phase / 2) - 1))]['defense_rewards'] = participant.defense_blocks_data
            # CHANGED: adjustable phase num
            if phase >= (num_phases * 2 + 2):  # PHASE: end
                if end_message_print:
                    end.display_object()
                pygame.display.update()
                continue
            else:
                if transition_message_print:
                    transition.display_object()
                pygame.display.update()
                continue

        else:  # PHASE: block
            phase_timer -= tic
            if phase_timer <= 0: phase += 1
            if safe_period > 0:
                safe_period -= tic
            else:
                safe_period = 0

            participant.timekeeping(tic)
            opponent.timekeeping(tic)

            """Participant's move"""
            participant.condition_check(tic, option1_presses, option2_presses, option3_presses,
                                        participant_earned_animation_duration, participant_defense_duration_mean,
                                        participant_defense_duration_sd)
            # use: participant stealing points
            if participant.stole_point == 1 and len(opponent.defense_blocks) <= 0 < opponent.points:
                """Successful point steal"""
                opponent.points -= 1
                opponent.provoked_animation_timer = opponent_provoked_animation_duration
                participant.stole_point = 0
            else:
                participant.stole_point = 0

            """Opponent's move"""
            # use: opponent choice
            if opponent.choice_cooldown == 0:
                opponent.ai_choose(opponent_aggression)
                opponent.manage_choice_result(choice1_delay_mean, choice1_delay_sd, choice2_delay_mean, choice2_delay_sd,
                                              choice3_delay_mean, choice3_delay_sd)
            opponent.manage_choice_timer(tic, opponent_earned_animation_duration, opponent_defense_duration_mean,
                                         opponent_defense_duration_sd)
            # use: opponent stole points
            if opponent.stole_point == 1:
                if safe_period <= 0:
                    if len(participant.defense_blocks) <= 0 < participant.points:
                        participant.points -= 1
                        participant.provoked = 1
                        participant.provoked_total += 1
                        participant.provoked_animation_timer = participant_provoked_animation_timer
                        opponent.stole_point = 0
                    elif participant.points <= 0:
                        opponent.stole_point = 0
                        opponent.choice = 1
                        opponent.choice_cooldown = 1
                        opponent.choice_timer = choice1_delay_mean - choice1_delay_sd
                    else:
                        opponent.stole_point = 0
                else:
                    # opponent.defense_blocks = np.append(opponent.defense_blocks, np.random.normal(opponent_defense_duration_mean, opponent_defense_duration_sd, 1))
                    opponent.stole_point = 0
                    opponent.choice = 1
                    opponent.choice_cooldown = 1
                    opponent.choice_timer = choice1_delay_mean - choice1_delay_sd

            """Data Processes"""

            """ObjectPrint content updates"""
            screen_player_points.content = participant.points
            screen_counter.content = participant.count
            screen_opponent_points.content = opponent.points

            """Print Display"""
            print_meters(get_block_quantities(len(participant.defense_blocks)), screen, meter_x, meter_y, block_spacing_x,
                         block_spacing_y, hundreds_block_color, tens_block_color, ones_block_color, block_width,
                         block_height)
            game_screen_display(tic, screen_player_points, screen_opponent_points, opponent, participant,
                                screen_counter, screen_choice_1, screen_choice_2, screen_choice_3,
                                screen_opponent_name, screen_player_name, choice_list)

            pygame.display.update()
            continue
