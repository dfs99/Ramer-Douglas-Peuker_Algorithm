import os
import re
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from src.data import AnimationParameters
from src.exceptions import RDPPainterException


class RamerDouglasPeukerPainter:
    """
    In order to use the RamerDouglasPeukerPainter class
    you must install first FFmpeg and add it to the
    environment variables. Otherwise, you cannot generate
    the animation.
    """

    FIGURE = plt.figure()
    AXES = FIGURE.add_subplot()
    FPS = 30
    FILENAME_REGEX = "[a-zA-Z0-9]"
    GIF_EXTENSION = "GIF_EXTENSION"
    VIDEO_EXTENSION = "VIDEO_EXTENSION"
    EXTENSIONS = {"GIF_EXTENSION": "gif", "VIDEO_EXTENSION": "mp4"}
    ANIMATION_INTERVALS = {"FAST": 10, "MEDIUM": 600, "SLOW": 2000}
    WRITER_GIF = animation.PillowWriter(fps=FPS)
    WRITER_VIDEO = animation.FFMpegWriter(fps=FPS)

    def __init__(self, data_solution, starting_points, ending_points):
        self.__data_solution = data_solution
        self.__starting_points = starting_points
        self.__ending_points = ending_points
        self.__animation_param_instance = AnimationParameters(data_solution)
        self.__lines = self.__set_lines()
        self.__starting_line = RamerDouglasPeukerPainter.AXES.plot([], [])[0]
        self.__already_plotted_matrix = self.__set_already_plotted_matrix()

    @property
    def data_solution(self):
        return self.__data_solution

    @property
    def starting_points(self):
        return self.__starting_points

    @property
    def ending_points(self):
        return self.__ending_points

    @property
    def animation_param_instance(self):
        return self.__animation_param_instance

    @property
    def lines(self):
        return self.__lines

    @property
    def starting_line(self):
        return self.__starting_line

    @property
    def already_plotted_matrix(self):
        return self.__already_plotted_matrix

    def __set_lines(self):
        """
        There will be as many lines as num_lines attribute from
        AnimationParameters instance plus the final line that
        shapes the set of ending points.

        :return: list of line2D(_lineN) from Matplotlib where
                N is the total number of lines.
        """
        total_lines = [RamerDouglasPeukerPainter.AXES.plot([], [])[0] for _ in
                       range(0, self.animation_param_instance.num_lines)]
        total_lines.append(RamerDouglasPeukerPainter.AXES.plot([], [])[0])
        return total_lines

    def __set_already_plotted_matrix(self):
        """
        Already plotted matrix is a boolean matrix that is used to animate
        the algorithm. If a cell is True, then the iteration has been represented
        successfully and the next one can be represented.
        :return: boolean matrix
        """
        return [False for _ in range(0, len(self.animation_param_instance.num_frames_for_each_iteration))]

    @staticmethod
    def __check_path(path):
        if not os.path.exists(path):
            raise RDPPainterException("Error while generating the animation: Path to store does not exist.")
        return path

    @staticmethod
    def __check_filename(filename):
        pattern = re.compile(RamerDouglasPeukerPainter.FILENAME_REGEX)
        if not pattern.match(filename):
            raise RDPPainterException("Error while generating the animation: Filename is not valid.")
        return filename

    @staticmethod
    def __check_format_to_save(format_to_save):
        """
        :param format_to_save: Valid values: "GIF_EXTENSION" or "VIDEO_EXTENSION"
        :return: The proper writer and extension in order to generate the animation.
        """
        if format_to_save not in RamerDouglasPeukerPainter.EXTENSIONS.keys():
            raise RDPPainterException("Error while generating the animation: Wrong Format to save.")
        if format_to_save == RamerDouglasPeukerPainter.GIF_EXTENSION:
            return RamerDouglasPeukerPainter.WRITER_GIF, RamerDouglasPeukerPainter.EXTENSIONS[format_to_save]
        elif format_to_save == RamerDouglasPeukerPainter.VIDEO_EXTENSION:
            return RamerDouglasPeukerPainter.WRITER_VIDEO, RamerDouglasPeukerPainter.EXTENSIONS[format_to_save]
        return format_to_save

    @staticmethod
    def __check_speed(speed):
        if speed not in RamerDouglasPeukerPainter.ANIMATION_INTERVALS.keys():
            raise RDPPainterException("Error while generating the animation: Wrong speed keyword.")
        return RamerDouglasPeukerPainter.ANIMATION_INTERVALS[speed]

    @staticmethod
    def __convert_to_ordered_list(args):
        """
        Although the lines are passed through a list, funcAnimation
        iterates through it and passes the line2D's as *args. Thus,
        args are converted again into a list.

        :return: list of line2Ds
        """
        return list(args)

    @staticmethod
    def show_animation():
        """
        Note that Matplotlib displays the axes with different
        limits. This can lead to wrong figures such as
        perpendicular lines. The box aspect is a way of solving
        the problem though its not appreciated in big scenarios.

        Plots the animation through matplotlib library.
        The box aspect is set to 1 in order to maintain
        its dimensions. In addition, the animation is closed.
        """
        RamerDouglasPeukerPainter.AXES.set_box_aspect(1)
        plt.show()
        plt.close(RamerDouglasPeukerPainter.FIGURE)

    @staticmethod
    def _get_lines(lines, index):
        """
        Gets the lines to be used to plot the current iteration.
        Each iteration has 3 lines.

        :param lines: list of line2D(_lineN)
        :param index: iteration index.
        :return: The current iteration lines.
        """
        start = index * AnimationParameters.NUM_LINES_NEEDED_PER_ITER
        end = start + AnimationParameters.NUM_LINES_NEEDED_PER_ITER
        return lines[start:end]

    def _draw_starting_points(self):
        """
        Plots the starting points of the algorithm.
        Attributes used to plot data:
            => color: black
            => line style: dashed
            => marker: x
            => line width: 1
        :return: starting line.
        """
        RamerDouglasPeukerPainter.AXES.plot([point.x for point in self.starting_points],
                                            [point.y for point in self.starting_points],
                                            color='k', linestyle='dashed', marker='x', lw=1)
        return self.starting_line,

    def _animate_iteration(self, i, *args):
        """
        Using the already plotted boolean matrix to know at every moment
        which iteration has either represented or not. It takes the 3 lines
        that belongs to the current iteration.
        => first line: used to represent the main line.
        => second line: used to represent all the sub lines with the points.
        => third line: used to plot the successful point.

        if j == 0, then gets the first three lines.
        if j > 0, if already_plotted_matrix[j-1] is false, the previous
            iteration has neither started nor finished. Otherwise, it
            gets the current iteration lines.

        k index: is used to plot an iteration. Due to the fact that the i value
        increments in each frame till the maximum value, it starts from 0. The
        first iteration will have the first nth frames where n is taken from
        the attr __num_frames_for_each_iteration of AnimationParameters class
        which is a list that has as many slots as iterations and the value is
        the number of frames that will be used to display the iteration.
        Thus, if the iteration has already been plotted, the k index will be
        updated. In order to get the number of frames of the current iteration
        and the exact frame of it, k must be subtracted from i.

        index lines:: i - k
            => if index_lines == 0: It's the first frame of the iteration.
                Frame used to plot the main line that connects the two points.
            => if index_lines == num_frames_iter - 1: Its the last frame of the
                iteration. Frame used to hide the main line, the line used to
                represent the sub lines and to show the point that will be stored
                in the solution.
            => A value between these limits means a frame to represent a point.

        The rest values of i will be used to maintain for a few ms the solution
        in the animation. The last value is used to close the plot.

        :param i: ith frame
        :param args: all the line2D used to animate the algorithm.
        :return: list of line2D(_line) used to represent every iteration.
        """
        lines = RamerDouglasPeukerPainter.__convert_to_ordered_list(args)
        for j in range(0, len(self.animation_param_instance.num_frames_for_each_iteration)):
            if j > 0:
                if self.already_plotted_matrix[j - 1] is True:
                    current_lines = RamerDouglasPeukerPainter._get_lines(lines, j)
                else:
                    current_lines = RamerDouglasPeukerPainter._get_lines(lines, j - 1)
            else:
                current_lines = RamerDouglasPeukerPainter._get_lines(lines, j)

            k = sum(self.animation_param_instance.num_frames_for_each_iteration[z]
                    if self.already_plotted_matrix[z] is True else 0
                    for z in range(0, len(self.animation_param_instance.num_frames_for_each_iteration)))

            index_lines = i - k
            if index_lines < self.animation_param_instance.num_frames_for_each_iteration[j] \
                    and self.already_plotted_matrix[j] is False:
                if index_lines == 0:
                    # draw main line.
                    x = [self.data_solution[j][l].x for l in range(0, 2)]
                    y = [self.data_solution[j][l].y for l in range(0, 2)]
                    current_lines[index_lines].set_data(x, y)
                    current_lines[index_lines].set_color("blue")
                    current_lines[index_lines].set_marker("X")
                elif index_lines == self.animation_param_instance.num_frames_for_each_iteration[j] - 1:
                    # hide the sub line
                    current_lines[index_lines - (self.animation_param_instance.num_frames_for_each_iteration[j] - 1)].set_data([], [])
                    # show the successful point using the third line.
                    x, y = [], []
                    for sub_list in self.data_solution[j][2]:
                        if sub_list[-1] is True:
                            x.append(sub_list[0].x)
                            y.append(sub_list[0].y)
                            break
                    current_lines[2].set_data(x, y)
                    current_lines[2].set_color("green")
                    current_lines[2].set_marker("X")
                    current_lines[2].set_markersize(11)
                    # hide main line.
                    current_lines[1].set_data([], [])
                else:
                    # draw the point sub line.
                    x, y = [], []
                    for l in range(0, len(self.data_solution[j][2])):
                        if l == index_lines - 1:
                            x = [self.data_solution[j][2][l][m].x for m in range(0, 2)]
                            y = [self.data_solution[j][2][l][m].y for m in range(0, 2)]
                            break
                    current_lines[1].set_data(x, y)
                    current_lines[1].set_color("blue")
                    current_lines[1].set_marker("X")
                    pass
                break
            else:
                self.already_plotted_matrix[j] = True

        if i >= self.animation_param_instance.num_frames_total_lines - \
                (1 + self.animation_param_instance.NUM_FRAMES_FOR_SOLUTION):
            if i == self.animation_param_instance.num_frames_total_lines - 1:
                # close the plot
                plt.close()
            self.starting_line.set_data([], [])
            lines[-1].set_data([point.x for point in self.ending_points], [point.y for point in self.ending_points])
            lines[-1].set_color("green")
            lines[-1].set_marker("X")
            lines[-1].set_markersize(12)
            lines[-1].set_linewidth(3)
        return [line for line in self.lines]

    def generate_animation(self, path_to_save, file_name, format_to_save, speed):
        """
        Generates an animation:
        :param path_to_save: It must be a directory.
        :param file_name: the name used to save the animation.
        :param format_to_save: either gif or mp4
        :param speed: of animation.
        """
        path = RamerDouglasPeukerPainter.__check_path(path_to_save)
        name = RamerDouglasPeukerPainter.__check_filename(file_name)
        given_writer, given_format = RamerDouglasPeukerPainter.__check_format_to_save(format_to_save)
        given_speed = RamerDouglasPeukerPainter.__check_speed(speed)
        absolute_path = path + "/" + name + "." + given_format
        current_animation = animation.FuncAnimation(RamerDouglasPeukerPainter.FIGURE, self._animate_iteration,
                                                    init_func=self._draw_starting_points, fargs=self.lines,
                                                    frames=self.animation_param_instance.num_frames_total_lines,
                                                    interval=given_speed, repeat=False, blit=True)
        RamerDouglasPeukerPainter.AXES.set_box_aspect(1)
        current_animation.save(absolute_path, writer=given_writer)
