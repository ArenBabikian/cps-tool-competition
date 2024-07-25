import matplotlib
matplotlib.use('TkAgg')
from math import cos, sin, radians

from matplotlib import pyplot as plt
import matplotlib.patches as patches
from shapely.geometry import LineString, Polygon
from shapely.affinity import translate, rotate
from descartes import PolygonPatch
from math import atan2, pi, degrees


# https://stackoverflow.com/questions/34764535/why-cant-matplotlib-plot-in-a-different-thread
class RoadTestVisualizer:
    """
        Visualize and Plot RoadTests
    """

    little_triangle = Polygon([(10, 0), (0, -5), (0, 5), (10, 0)])
    square = Polygon([(5, 5), (5, -5), (-5, -5), (-5, 5), (5,5)])
    FIGLEN = 6
    FONTSIZE = FIGLEN * 3
    LABELSIZE = FONTSIZE+2
    PAD = (FIGLEN-3) // 2 + 1
    MULT = FIGLEN/4

    def __init__(self, map_size):
        self.map_size = map_size
        self.last_submitted_test_figure = None

        # Make sure there's a windows and does not block anything when calling show
        plt.ion()
        plt.show()

    def _setup_params(self):

        # Set the default line width to 4
        params = ['lines.linewidth', 'lines.markersize', 'xtick.major.width', 'ytick.major.width']
        # params = ['lines.linewidth', 'lines.markersize']
        for param in params:
            plt.rcParams[param] = plt.rcParams[param] * self.MULT
        # print(plt.rcParams['lines.linewidth'])
        # print(plt.rcParams['lines.markersize'])
        # print(plt.rcParams['xtick.major.size'])
        # print(plt.rcParams['ytick.major.size'])
        
        # plt.rcParams['lines.linewidth'] = 4
        # plt.rcParams['lines.markersize'] = 10
        
        # plt.rcParams['lines.linewidth'] =1.5

    def _setup_figure(self):
        if self.last_submitted_test_figure is not None:
            # Make sure we operate on the right figure
            plt.figure(self.last_submitted_test_figure.number)
            plt.clf()
        else:
            self.last_submitted_test_figure = plt.figure(figsize=(self.FIGLEN, self.FIGLEN))  # Set the figure size to a square (6x6 inches)

        # plt.gcf().set_title("Last Generated Test")
        plt.gca().set_aspect('equal', 'box')
        plt.gca().set(xlim=(-30, self.map_size + 30), ylim=(-30, self.map_size + 30))

        # Increase the size of the axis labels
        plt.tight_layout(pad=self.PAD)
        plt.xticks(fontsize=self.FONTSIZE)
        plt.yticks(fontsize=self.FONTSIZE)

    def visualize_road_test(self, the_test):

        self._setup_figure()
        self._setup_params()

        # Add information about the test validity
        # title_string = ""
        # if the_test.is_valid is not None:
        #     title_string = title_string + "Test is " + ("valid" if the_test.is_valid else "invalid")
        #     if not the_test.is_valid:
        #         title_string = title_string + ":" + the_test.validation_message

        # plt.suptitle(title_string, fontsize=14)
        # plt.draw()
        # plt.pause(0.001)
        
        # Plot the map. Trying to re-use an artist in more than one Axes which is supported
        # map_patch = patches.Rectangle((0, 0), self.map_size, self.map_size, linewidth=1, edgecolor='black', facecolor='none')
        # plt.gca().add_patch(map_patch)


        # Road Geometry.
        road_poly = LineString([(t[0], t[1]) for t in the_test.interpolated_points]).buffer(8.0, cap_style=2, join_style=2)
        road_patch = PolygonPatch(road_poly, fc='gray', ec='dimgray')  # ec='#555555', alpha=0.5, zorder=4)
        plt.gca().add_patch(road_patch )

        # Interpolated Points
        sx = [t[0] for t in the_test.interpolated_points]
        sy = [t[1] for t in the_test.interpolated_points]
        plt.plot(sx, sy, 'yellow')

        # Road Points
        x = [t[0] for t in the_test.road_points]
        y = [t[1] for t in the_test.road_points]
        plt.plot(x, y, 'wo')

        # Plot the little triangle indicating the starting position of the ego-vehicle
        delta_x = sx[1] - sx[0]
        delta_y = sy[1] - sy[0]

        current_angle = atan2(delta_y, delta_x)

        rotation_angle = degrees(current_angle)
        transformed_fov = rotate(self.little_triangle, origin=(0, 0), angle=rotation_angle)
        transformed_fov = translate(transformed_fov, xoff=sx[0], yoff=sy[0])
        plt.plot(*transformed_fov.exterior.xy, color='black')

        # Plot the little square indicating the ending position of the ego-vehicle
        delta_x = sx[-1] - sx[-2]
        delta_y = sy[-1] - sy[-2]

        current_angle = atan2(delta_y, delta_x)

        rotation_angle = degrees(current_angle)
        transformed_fov = rotate(self.square, origin=(0, 0), angle=rotation_angle)
        transformed_fov = translate(transformed_fov, xoff=sx[-1], yoff=sy[-1])
        plt.plot(*transformed_fov.exterior.xy, color='black')


        # # Add information about the test validity
        # title_string = ""
        # if the_test.is_valid is not None:
        #     title_string = " ".join([title_string, "Test", str(the_test.id), "is" , ("valid" if the_test.is_valid else "invalid")])
        #     if not the_test.is_valid:
        #         title_string = title_string + ":" + the_test.validation_message

        # plt.suptitle(title_string, fontsize=14)
        # plt.draw()
        plt.savefig('optangle/_figs/full.png')
        plt.pause(0.001)


    def simple_vis(self, the_test):

        self._setup_figure()

        # Road Points
        x = [t[0] for t in the_test.road_points]
        y = [t[1] for t in the_test.road_points]
        plt.plot(x, y, 'ko-')

        length = 40
        radius = length / 2
        radius_label = radius * 1.66

        # initial_x, initial_y = the_test.road_points[0]
        # plt.plot([initial_x, initial_x + length], [initial_y, initial_y], 'r--')
        for i in range(len(the_test.road_points) - 1):
            x2, y2 = the_test.road_points[i]
            if i == 0:
                x1, y1 = x2-(radius), y2
                plt.text(x1, y1, f"p₀₀", ha='center', va='center', color='blue', fontsize=self.LABELSIZE)
                # dash to make the first subscript 0 into a θ
                plt.plot([x1, x1+3], [y1-0.9, y1-0.9], 'b-', linewidth=1)
            else:
                x1, y1 = the_test.road_points[i-1]
            dx = x2 - x1
            dy = y2 - y1
            scale_factor = length / (dx**2 + dy**2)**0.5
            plt.plot([x2, x2 + scale_factor*dx], [y2, y2 + scale_factor*dy], 'r--')

            # Calculate the angle between the current segment and the next segment
            x3, y3 = the_test.road_points[i]
            x4, y4 = the_test.road_points[i+1]
            dx2 = x4 - x3
            dy2 = y4 - y3
            angle = atan2(dy2, dx2) - atan2(dy, dx)
            angle_degrees = degrees(angle)

            # Plot the segment of a circle to indicate the angle
            start_angle = degrees(atan2(dy, dx))
            end_angle = start_angle + angle_degrees

            new_start_angle = start_angle if start_angle >= 0 else 360 + start_angle
            new_end_angle = end_angle if end_angle > 0 else 360 + end_angle

            if new_start_angle > new_end_angle:
                start_angle, end_angle = end_angle, start_angle

            print(f"start_angle: {start_angle}, end_angle: {end_angle}")

            arc = patches.Arc((x2, y2), 2*radius, 2*radius, angle=0, theta1=start_angle, theta2=end_angle, color='blue', linewidth=self.MULT)
            plt.gca().add_patch(arc)

            # Add theta symbol followed by the index of the point
            mid_angle = (new_start_angle + new_end_angle) / 2
            mid_x = x2 + radius_label * cos(radians(mid_angle))
            mid_y = y2 + radius_label * sin(radians(mid_angle))
            SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
            plt.text(mid_x, mid_y, f"θ{i}".translate(SUB), ha='center', va='center', color='blue', fontsize=self.LABELSIZE)
        plt.draw()
        plt.savefig('optangle/_figs/simple.png')
        plt.pause(0.001)