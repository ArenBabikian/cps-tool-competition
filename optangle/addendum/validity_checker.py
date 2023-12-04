
import logging as log
import random
from time import sleep

from code_pipeline.test_analysis import compute_all_features
from code_pipeline.tests_generation import RoadTestFactory


# TEMP
import sys
from code_pipeline.validation import TestValidator
# from rigaa.utils.road_validity_check import is_inside_map
# from self_driving.simulation_data import SimulationDataRecordProperties
import optangle.src.debug as debug





from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.termination import Termination
from pymoo.optimize import minimize
import math
import numpy as np
import matplotlib.pyplot as plt
import optangle.src.utils as utils

class ValidityChecker():
    """
        Yassou
    """

    def __init__(self, executor=None, map_size=None):
        self.executor = executor
        self.map_size = map_size

    def start(self):
        # self.gridsearchCriticalangle()
        # self.featureEvaluation()
        # self.fitnessEvaluation()s
        # self.sharpness3Evaluation()
        # self.simpletest()
        # self.gatheroobdata()
        self.analysis()

    def analysis(self):
        p0 = "src.aren_generator_ArenGenerator_170167962743.0" # 15, 50, (5, 30)
        p1 = "src.optangle_OptAngleGenerator_170168349804.0" # 10, 35, (5, 30)
        p2 = "src.optangle_OptAngleGenerator_170170774747.0" # 20, 65, (3, 20)
        p3 = "src.optangle_OptAngleGenerator_170171651030.0" # 20, 65, (3, 20), new heuristics for diversity
        for p in [p3]:
            debug.analyse_result_features(f"C:\git\cps-tool-competition\\results\\{p}")

        

    # TODO TEMP remove this
    # is_valid, validation_msg = debug.validate(self.executor, the_test)
    # # if validation_msg == "Not entirely inside the map boundaries":
    # debug.visualise(self.executor, the_test)

    def gatheroobdata(self):

        pts = [
            (50, 100),
            (90, 100),
            (130, 120),
            (160, 100),
            (190, 110)
        ]
        the_test = RoadTestFactory.create_road_test(pts)

        # Test is valid, so we can simulate it
        test_outcome, description, execution_data = self.executor.execute_test(the_test)

        # Extract the oob_percentage values from the execution_data
        oob_percentages = [state.oob_percentage for state in execution_data]
        oob_distance = [state.oob_distance for state in execution_data]
        steering = [state.steering for state in execution_data]

        # Plot the oob_percentage values
        plt.clf()
        plt.plot(oob_percentages)
        plt.xlabel('Simulation Step')
        plt.ylabel('oob_percentage')
        plt.title('oob_percentage from Execution Data')
        plt.savefig("C:\git\cps-tool-competition\\aren\\archive\\f_long_perc.png")
        plt.clf()
        
        plt.plot(oob_distance)
        plt.xlabel('Simulation Step')
        plt.ylabel('oob_distance')
        plt.title('oob_distance from Execution Data')
        plt.savefig("C:\git\cps-tool-competition\\aren\\archive\\f_long_dist.png")
        plt.clf()
        
        plt.plot(steering)
        plt.xlabel('Simulation Step')
        plt.ylabel('steering angle')
        plt.title('steering angle from Execution Data')
        plt.savefig("C:\git\cps-tool-competition\\aren\\archive\\f_long_steer.png")


        # Specify the file path to save the execution data
        output_file = "C:\git\cps-tool-competition\\aren\\archive\exec_data.json"

        # Open the file in write mode
        with open(output_file, "w") as f:
            for state in execution_data:
                f.write(str(state) + "\n")


    def simpletest(self):

        max_num_points = 26
        angle = 20
        # define random individual
        individual = {}
        individual['num_points'] = max_num_points
        for i in range(max_num_points):
            if i <= max_num_points/2:
                individual[f'p{i}_theta'] = angle
            else:
                individual[f'p{i}_theta'] = 0-angle

        print(individual)


        # make test and run
        road_points, missing_dist = utils.getRoadPointsFromAngles(individual, self.map_size)
        the_test = RoadTestFactory.create_road_test(road_points)
        
        is_valid = debug.validate(self.executor, the_test)
        print(f"VALID?: {is_valid}")\

        features = compute_all_features(the_test, [])
        print(f"FEATURES: {features}")

        
        debug.visualise(self.executor, the_test)
            # sleep(5)



    def sharpness3Evaluation(self):
        road_points = [
            (100, 50),
            (100, 60),
            (100, 70),
            (100, 80)
        ]

        csv_info = [",".join(["theta0", "theta1", "theta2", "is_valid"])]

        ran = range(-35, 36, 5)
        individual = {'num_points':3}
        for theta0 in ran:
            individual[f'p0_theta'] = theta0
            
            x, y, r = [], [], []
            for theta1 in ran:
                individual[f'p1_theta'] = theta1
                for theta2 in ran:
                    individual[f'p2_theta'] = theta2

                    # road_points = [(100, 10), (100, 20), (100, 30), (100, 40)]
                    road_points = []

                    rps = utils.getRoadPointsFromAngles(individual,  self.map_size)
                    road_points.extend(rps)
                    the_test = RoadTestFactory.create_road_test(road_points)
                    is_valid = debug.validate(self.executor, the_test)
                    debug.visualise(self.executor, the_test)
                    # exit()

                    x.append(theta1)
                    y.append(theta2)
                    r.append(is_valid)

                    state = ",".join([str(theta0), str(theta1), str(theta2), str(is_valid)])
                    print(state)
                    csv_info.append(state)

            # Create scatter plot
            plt.scatter(x, y, c=r, cmap='bwr')
            plt.colorbar(label='Validity')
            plt.legend()
            plt.xlabel('theta1')
            plt.ylabel('theta2')
            plt.title(f'Validity Plot for theta0={theta0}')
            plt.savefig(f'aren/results/data3/t0_{theta0}.png')
            # plt.show()
            plt.clf()

        csv = '\n'.join(csv_info)
        
        with open('aren\\data3.csv', 'w') as output_file:
            output_file.write(csv)

    def sharpness2Evaluation(self):

        csv_info = [",".join(["theta0", "theta1", "is_valid"])]
        x, y, r = [], [], []

        ran = range(-35, 36, 2)
        individual = {'num_points': 2}
        for theta0 in ran:
            individual[f'p0_theta'] = theta0
            for theta1 in ran:
                individual[f'p1_theta'] = theta1

                # road_points = [(100, 10), (100, 20), (100, 30), (100, 40)]
                road_points = []

                rps = utils.getRoadPointsFromAngles(individual, self.map_size)
                road_points.extend(rps)
                the_test = RoadTestFactory.create_road_test(road_points)
                is_valid = debug.validate(self.executor, the_test)
                # debug.visualise(self.executor, the_test)
                # exit()

                x.append(theta0)
                y.append(theta1)
                r.append(is_valid)

                state = ",".join([str(theta0), str(theta1), str(is_valid)])
                print(state)
                csv_info.append(state)

        csv = '\n'.join(csv_info)

        with open('aren/data2.csv', 'w') as output_file:
            output_file.write(csv)

        # Create scatter plot
        plt.scatter(x, y, c=r, cmap='bwr')
        plt.colorbar(label='Validity')
        plt.legend()
        plt.xlabel('theta0')
        plt.ylabel('theta1')
        plt.title('Validity Plot')
        plt.savefig('aren/data2.png')
        plt.show()


    def getDirCov(self, x):    
        # theoretical maximum is 0.5, if we have a full circle.
        # This is because we use a method based on cos/dot-product
        angles_range = [0,0]
        cur_angle = 0
        num_p = x['num_points']
        for i in range(num_p):
            theta = x[f'p{i}_theta']
            cur_angle += theta
            angles_range[0] = min(angles_range[0], cur_angle)
            angles_range[1] = max(angles_range[1], cur_angle)

        dir_cov = (angles_range[1] - angles_range[0]) / 360
        return dir_cov


    def fitnessEvaluation(self):

        max_num_points = 10
        # define the solution

        heuristic_vals = []
        feature_vals = []
        diff = []

        while len(heuristic_vals) < 30:

            # define random individual
            individual = {}
            individual['num_points'] = max_num_points
            for i in range(max_num_points):
                individual[f'p{i}_theta'] = random.randint(-35, 35)

            # measure dir_cov heuristic
            dir_cov = self.getDirCov(individual)

            # make test and run
            road_points, missing_dist = utils.getRoadPointsFromAngles(individual, self.map_size)
            hv1 = missing_dist
            
            hv2 = utils.heu_approxSelfIntersecting(road_points)

            # Create the test
            the_test = RoadTestFactory.create_road_test(road_points)
            
            # HV3: too_sharp_turn:
            hv3 = utils.heu_tooSharpTurns(the_test)

            if hv1 > 0 or hv2 > 0 or hv3 > 0:
                continue
            is_valid = debug.validate(self.executor, the_test)
            # debug.visualise(self.executor, the_test)

            if is_valid:
                # test_outcome, description, execution_data = self.executor.execute_test(the_test)

                # test_outcome, description, execution_data = self.executor._execute(the_test)
                # features = compute_all_features(the_test, execution_data)

                features = compute_all_features(the_test, [])

                heuristic_vals.append(dir_cov)
                feature_vals.append(features['DIR_COV'])
                diff.append((dir_cov - features['DIR_COV'])/features['DIR_COV'])

                # print(f"ANGLE: {angle} >>> FEATURES: {features}")
                # sleep(5)

        print(f"HEURISTICS: {heuristic_vals}")
        print(f"FEATURES: {features}")
        print(f"DIFF: {diff}")

        plt.plot([0, 0.5], [0, 0.5], color='red', linestyle='--')
        plt.scatter(feature_vals, heuristic_vals)
        plt.xlabel("features['DIR_COV']")
        plt.ylabel("heuristic_vals")
        plt.title("Feature vs Heuristic Values")
        plt.xlim(0, 0.5)
        plt.ylim(0, 0.7)
        plt.show()
        plt.pause(20)


    def gridsearchCriticalangle(self):

        d2ang = {
            5: range(15, 21),
            10: range(35, 41),
            15: range(50, 56),
            20: range(65, 71)
        }

        for dist in d2ang.keys():
            for angle in d2ang[dist]:

                p0 = (150, 50)
                p1 = (p0[0], p0[1] + dist)
                
                road_points = [p0, p1]

                p_now = p0
                p_next = p1
                for i in range(10):
                    p_temp = p_next
                    p_next = utils.get_next_point(p_next, p_now, angle, dist)
                    p_now = p_temp
                    road_points.append(p_next)

                log.info("Generated test using: %s", road_points)
                the_test = RoadTestFactory.create_road_test(road_points)

                is_valid = debug.validate(self.executor, the_test)
                debug.visualise(self.executor, the_test)

                print(f"ANGLE: {angle}, DIST: {dist} >>> VALID?: {is_valid}")
                if not is_valid:
                    sleep(5)
                    break


    def featureEvaluation(self):

        d_init = 60
        d = 20
        n_segs = 5
        angles = range(0, 360, 15)

        for angle in angles:
            
            angle_rad = math.radians(angle)
            p0_x = 100 + d_init * math.cos(angle_rad)
            p0_y = 100 + d_init * math.sin(angle_rad)
            p0 = (p0_x, p0_y)

            p1_x = p0_x - d * math.cos(angle_rad+math.pi/2)
            p1_y = p0_y - d * math.sin(angle_rad+math.pi/2)
            p1 = (p1_x, p1_y)

            road_points = [p0, p1]

            p_now = p0
            p_next = p1
            for i in range(n_segs):
                if i > n_segs/3:
                    a = 30
                else:
                    a = -30
                p_temp = p_next
                p_next = utils.get_next_point(p_next, p_now, a, d)
                p_now = p_temp
                road_points.append(p_next)

            the_test = RoadTestFactory.create_road_test(road_points)
            is_valid = debug.validate(the_test)
            debug.visualise(the_test)

            if is_valid:
                # test_outcome, description, execution_data = self.executor.execute_test(the_test)

                test_outcome, description, execution_data = self.executor._execute(the_test)
                features = compute_all_features(the_test, execution_data)

                print(f"ANGLE: {angle} >>> FEATURES: {features}")
                sleep(5)




