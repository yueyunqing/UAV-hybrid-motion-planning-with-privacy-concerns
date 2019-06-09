#!/usr/bin/env python
# main function
import numpy as np
from path import Path
from point import Point
import geneticAlgorithm as gA
from quickSort import quick_sort
from gridVisualization import grid_visualization
from mapTools import privacy_init, map_generate

path = []
grid_x = 5
grid_y = 5
grid_z = 5
thickness = 5
occ_grid = None
population = 500
max_generation = 30
tournament_size = 10
objectives = []
no_of_objectives = 1
obstacles_per_axis = 1
starting_point = Point(0, 0, 0)
end_point = Point(4, 4, 4)
grid_map = [grid_x, grid_y, grid_z]
sigma = 0.00001
mutation_rate = 5
ts = 2
sr = 40
safety_threshold = 0.5
privacy_threshold = 0.1
privacy_radius = 1


if __name__ == "__main__":
    # Create a 3D Occupancy Grid
    print('\033[94m Generating random occupancy grid and objectives... \033[0m')
    occ_grid, obstacle_num = map_generate(grid_x, grid_y, grid_z,
                                          starting_point, end_point, safety_threshold, privacy_threshold)
    print(occ_grid)
    pri_grid, privacy_sum = privacy_init(grid_x, grid_y, grid_z, starting_point, end_point, occ_grid, privacy_radius)
    print(pri_grid)
    objectives = [end_point]
    alg = gA.GeneticAlgorithm(population, 0.00001, 5, 2, 40, grid_map)

    print('\033[94m Generating random initial solutions... \033[0m')
    paths = alg.init_population(starting_point, objectives)

    for p in range(len(paths)):
        paths[p].fitness = alg.get_fitness(paths[p].points, occ_grid, pri_grid,
                                           starting_point, end_point, privacy_sum, obstacle_num)

    max_p = max(paths, key=lambda x: x.fitness)

    max_f = -5
    count = 0
    fitnv = []
    print(len(paths))

    for i in range(max_generation):
        quick_sort(paths)
        if max_f < paths[0].fitness:
            max_f = paths[0].fitness
            print('\033[94m Current maximum fitness:\033[0m\033[92m ' + str(
                max_f) + '\033[0m\033[94m, Generation:\033[0m\033[92m ' + str(i) + ' \033[0m')
            for j in range(len(paths[0].points)):
                print(paths[0].points[j])
            print("the generation", i, len(paths[0].points))
            alg.get_fitness(paths[0].points, occ_grid, pri_grid, starting_point, end_point, privacy_sum, obstacle_num)

        p1 = alg.tournament_select(paths)
        p2 = alg.tournament_select(paths)

        new_path = []
        # Always crossover (cr = 1)
        new_path1 = alg.cross_over(paths[p1].points, paths[p2].points, objectives)
        new_path2 = alg.cross_over(paths[p2].points, paths[p1].points, objectives)

        new_path1_ = alg.mutate(new_path1, objectives)
        new_path1_.fitness = alg.get_fitness(new_path1.points, occ_grid, pri_grid,
                                             starting_point, end_point, privacy_sum, obstacle_num)
        paths[-2] = new_path1_

        new_path2_ = alg.mutate(new_path2, objectives)
        new_path2_.fitness = alg.get_fitness(new_path2.points, occ_grid, pri_grid,
                                             starting_point, end_point, privacy_sum, obstacle_num)
        paths[-1] = new_path2_

    # optimal path
    quick_sort(paths)
    for j in range(len(paths[0].points)):
        print(paths[0].points[j])
    print("optimal", len(paths[0].points))

    # initial path
    for j in range(len(max_p.points)):
        print(max_p.points[j])
    print("initial", len(max_p.points))

    grid_visualization(occ_grid, starting_point, objectives, paths[0].points, max_p.points)