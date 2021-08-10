

class AnimationParameters:
    """
    AnimationParameters class contains all the attributes
    needed in order to plot or animate the Ramer Douglas
    Peuker Algorithm.
    For each RDP iteration, 3 lines are needed.
        => first line: draw the base line.
        => second line: loop over every point between the
            two points that were used to draw the base line.
        => third line: marks the single point that is
            part of the solution.
    Furthermore, in order to generate successful animations,
    30 extra frames will be used to be able to maintain the
    solution line enough time.

    The rest of the parameters will be extracted from the
    plot_data attribute from RamerDouglasPeukerAlgorithm
    class.
    """
    NUM_LINES_NEEDED_PER_ITER = 3
    NUM_FRAMES_FOR_SOLUTION = 30

    def __init__(self, data_solution):
        self.__num_lines = len(data_solution) * AnimationParameters.NUM_LINES_NEEDED_PER_ITER
        self.__num_frames_for_lines = len(data_solution)
        self.__num_frames_total_lines = self.set_num_frames_total_lines(1 + self.num_frames_for_lines +
                                        AnimationParameters.NUM_FRAMES_FOR_SOLUTION, data_solution)
        self.__num_frames_for_each_iteration = self.set_num_frames_for_each_iteration(data_solution)

    @property
    def num_lines(self):
        return self.__num_lines

    @property
    def num_frames_for_lines(self):
        return self.__num_frames_for_lines

    @property
    def num_frames_total_lines(self):
        return self.__num_frames_total_lines

    @property
    def num_frames_for_each_iteration(self):
        return self.__num_frames_for_each_iteration

    def __str__(self):
        msg = """
        Animation Parameters:
            num_lines:{0}
            num_frames:{1}
            num_frames_total_lines:{2}
            mun_frames_each_iteration:{3}
        """.format(self.num_lines, self.num_frames_for_lines, self.num_frames_total_lines,
                   self.num_frames_for_each_iteration)
        return msg

    def set_num_frames_total_lines(self, new_frames, data_sol):
        """

        :param new_frames: contains:
            => 1 frame to draw each main line.
            => 1 frame for the line that represents the end solution.
            => As many frames as used to maintain the solution in the animation.

        :param data_sol: list that contains the solution. From it, the frames
        extracted are:
            => As many frames as points between the 2 points that shapes the main
            line.
            => 1 extra frame to hide the main line and place the selected point.

        :return: an integer that contains the number of total frames needed.
        """
        return new_frames + sum(len(data_sol[i][2]) + 1 for i in range(0, self.num_frames_for_lines))

    @staticmethod
    def set_num_frames_for_each_iteration(data_sol):
        """
        A list that contains as many slots as main lines.
        Each slot will have an integer number that represents
        the number of frames needed for each main line iteration.
        The number of frames depends on:
            => the number of points between the main line.
            => 1 extra frame to plot the main line.
            => 1 extra frame to place the selected point and hide
                the main line.
        :param data_sol: list that contains the plot_data attr from
        RamerDouglasPeukerAlgorithm class.

        :return: A list that contains as many slots as main lines.
        """
        num_frames_each_iter = [0 for _ in range(0, len(data_sol))]
        for i in range(0, len(data_sol)):
            num_frames_each_iter[i] += (2 + len(data_sol[i][2]))
        return num_frames_each_iter
