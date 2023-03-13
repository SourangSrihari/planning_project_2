import cv2
import numpy as np
from matplotlib import pyplot as plt
import heapq as hq
from queue import PriorityQueue
import pygame as pg
import time


def change_points(coords, height):
    """Convert coordinates into pygame coordinates (lower-left => top left)."""
    return (coords[0], height - coords[1])

def change_points_rect(coords, height, obj_height):
    """Convert an object's coords into pygame coordinates (lower-left of object => top left in pygame coords)."""
    return (coords[0], height - coords[1] - obj_height)

def game(visited, ideal_path):
    pg.init()
    display = pg.display.set_mode((600,250))
    obs_color = (0, 255, 255)
    border = (255, 255, 0)
    validation = True
    clock = pg.time.Clock()

    rectangle_lower_clearance = change_points_rect([95, 0], 250, 105)
    rectangle_upper_clearance = change_points_rect([95, 145], 250, 105)
    triangle_clearance_first = change_points([455, 20], 250)
    triangle_clearance_second = change_points([463, 20], 250)
    triangle_clearance_third = change_points([515.5, 125], 250)
    triangle_clearance_fourth = change_points([463, 230], 250)
    triangle_clearance_fifth = change_points([455, 230], 250)
    hexagon_clearance_first = change_points([300, 205.76], 250)
    hexagon_clearance_second = change_points([230, 165.38], 250)
    hexagon_clearance_third = change_points([230, 84.61], 250)
    hexagon_clearance_fourth = change_points([300, 44.23], 250)
    hexagon_clearance_fifth = change_points([370, 84.61], 250)
    hexagon_clearance_sixth = change_points([370, 165.38], 250)    

    rectangle_lower_without_clearance = change_points_rect([100, 0], 250, 100)
    rectangle_upper_without_clearance = change_points_rect([100, 150], 250, 100)
    triangle_without_clearance_first = change_points([460, 25], 250)
    triangle_without_clearance_second = change_points([460, 225], 250)
    triangle_without_clearance_third = change_points([510, 125], 250)
    hexagon_without_clearance_first = change_points([235,87.5], 250)
    hexagon_without_clearance_second = change_points([300,50], 250)
    hexagon_without_clearance_third = change_points([365,87.5], 250)
    hexagon_without_clearance_fourth = change_points([365,162.5], 250)
    hexagon_without_clearance_fifth = change_points([300,200], 250)
    hexagon_without_clearance_sixth = change_points([235,162.5], 250)

    while validation:
        for a in pg.event.get():
            if a.type == pg.QUIT:
                validation = False

        pg.draw.rect(display, border, pg.Rect(rectangle_lower_clearance[0], rectangle_lower_clearance[1], 60, 105))
        pg.draw.rect(display, border, pg.Rect(rectangle_upper_clearance[0], rectangle_upper_clearance[1], 60, 105))
        pg.draw.polygon(display, border, ((triangle_clearance_first),(triangle_clearance_second),(triangle_clearance_third), (triangle_clearance_fourth), (triangle_clearance_fifth)))
        pg.draw.polygon(display, border, ((hexagon_clearance_first),(hexagon_clearance_second),(hexagon_clearance_third),(hexagon_clearance_fourth),(hexagon_clearance_fifth),(hexagon_clearance_sixth)))
        pg.draw.rect(display, obs_color, pg.Rect(rectangle_lower_without_clearance[0], rectangle_lower_without_clearance[1], 50, 100))
        pg.draw.rect(display, obs_color, pg.Rect(rectangle_upper_without_clearance[0], rectangle_upper_without_clearance[1], 50, 100))
        pg.draw.polygon(display, obs_color, ((triangle_without_clearance_first),(triangle_without_clearance_second),(triangle_without_clearance_third)))
        pg.draw.polygon(display, obs_color, ((hexagon_without_clearance_first),(hexagon_without_clearance_second),(hexagon_without_clearance_third),(hexagon_without_clearance_fourth),(hexagon_without_clearance_fifth),(hexagon_without_clearance_sixth)))
        pg.draw.rect(display, border ,pg.Rect(0, 0, 600, 5))
        pg.draw.rect(display, border ,pg.Rect(0, 245, 600, 5))
        pg.draw.rect(display, border ,pg.Rect(0, 0, 5, 250))
        pg.draw.rect(display, border ,pg.Rect(595, 0, 5, 250))

        for j in visited:
            pg.draw.circle(display, (0, 255, 255), change_points(j, 250), 1)
            pg.display.flip()
            clock.tick(700)

        for i in ideal_path:
            pg.draw.circle(display,(255, 255, 0) , change_points(i, 250), 1)
            pg.display.flip()
            clock.tick(40)
        pg.display.flip()
        pg.time.wait(3000)
        validation = False
    pg.quit()


def orientation_block():
    occupied_space = []
    for x in range(0, 251):
        for y in range(0, 601):
            if (95<=x<=155) and (0<=y<=105):
                occupied_space.append((x, y))
            if (100<=x<=150) and (0<=y<=100):
                occupied_space.append((x, y))
            if (95<=x<=155) and (145<=y<=250):
                occupied_space.append((x, y))
            if (100<=x<= 150) and (150<=y<=250):
                occupied_space.append((x, y))                
            if (y+2*x-1156) < 0 and (y-2*x+906) > 0 and (455<=x) and (20<=y<=230):
                occupied_space.append((x, y))
            if (y-(15/26)*x - (425/13)) < 0 and (y+(15/26)*x - (4925/13)) < 0 and (y-(15/26)*x + (1675/13)) > 0 and (y+(15/26)*x-(2825/13)) > 0 and (230<=x<=370):
                occupied_space.append((x, y))
            if (y+2*x-1145) < 0 and (y-2*x+895) > 0 and (460<=x) and (20<=y<=230):
                occupied_space.append((x, y))
            if (y-(15/26)*x - (350/13)) < 0 and (y+(15/26)*x - (4850/13)) < 0 and (y-(15/26)*x + (1600/13)) > 0 and (y+(15/26)*x - (2900/13)) > 0 and (235<=x<=365):
                occupied_space.append((x, y))
            if (0 <= x <= 5) or (0 <= y <= 5) or (595 <= x <= 600) or (245 <= y <= 250):
                occupied_space.append((x, y))

    return occupied_space


def taking_start_from_user():
    user_input = input('enter the start node separated by comma')
    user_input = tuple(int(i) for i in user_input.split(","))
    while check: 
        if user_input in obstacle_areas or user_input[0] > 600 or user_input[1] > 250 or user_input[0] < 0 or user_input[1] < 0:
            print('Try again')
            user_input = input('enter the start node separated by comma ')
            user_input = tuple(int(i) for i in user_input.split(","))
        else:
            return user_input


def taking_goal_from_user():

    user_goal = input('enter the goal node separated by comma')
    user_goal = tuple(int(i) for i in user_goal.split(","))
    while check: 
        if user_goal in obstacle_areas or user_goal[0] > 600 or user_goal[1] > 250 or user_goal[0] < 0 or user_goal[1] < 0:
            print('Try again')
            user_goal = input('enter the goal node separated by comma ')
            user_goal = tuple(int(i) for i in user_goal.split(","))
        else:
            return user_goal
    return 

def upward_movement(pos1, pos2, pop_number):
    new_coordinates = (pos1, pos2+1)
    if new_coordinates not in visitor_list and new_coordinates not in obstacle_areas:
        cost_function = pop_number[0] + 1
        element = (cost_function, new_coordinates)
        for a in range(queue_list.qsize()):
            if queue_list.queue[a][1]==new_coordinates:
                if queue_list.queue[a][0]>cost_function:
                    queue_list.queue[a] = element
                    return
                else:
                    return
        queue_list.put(element)
        pop_1 = pop_number[1]
        deep_1 = new_coordinates
        map_dict[deep_1] = pop_1


def downward_movement(pos1, pos2, pop_number):
    new_coordinates = (pos1, pos2-1)
    if new_coordinates not in visitor_list and new_coordinates not in obstacle_areas:
        cost_function = pop_number[0] + 1
        element = (cost_function, new_coordinates)
        for a in range(queue_list.qsize()):
            if queue_list.queue[a][1]==new_coordinates:
                if queue_list.queue[a][0]>cost_function:
                    queue_list.queue[a] = element
                    return
                else:
                    return
        queue_list.put(element)
        pop_1 = pop_number[1]
        deep_1 = new_coordinates
        map_dict[deep_1] = pop_1


def leftward_movement(pos1, pos2, pop_number):
    new_coordinates = (pos1-1, pos2)

    if new_coordinates not in visitor_list and new_coordinates not in obstacle_areas:
        cost_function = pop_number[0] + 1
        element = (cost_function, new_coordinates)
        for a in range(queue_list.qsize()):
            if queue_list.queue[a][1]==new_coordinates:
                if queue_list.queue[a][0]>cost_function:
                    queue_list.queue[a] = element
                    return
                else:
                    return
        queue_list.put(element)
        pop_1 = pop_number[1]
        deep_1 = new_coordinates
        map_dict[deep_1] = pop_1

def rightward_movement(pos1, pos2, pop_number):
    new_coordinates = (pos1+1, pos2)
    if new_coordinates not in visitor_list and new_coordinates not in obstacle_areas:
        cost_function = pop_number[0] + 1
        element = (cost_function, new_coordinates)
        for a in range(queue_list.qsize()):
            if queue_list.queue[a][1]==new_coordinates:
                if queue_list.queue[a][0]>cost_function:
                    queue_list.queue[a] = element
                    return
                else:
                    return
        queue_list.put(element)
        pop_1 = pop_number[1]
        deep_1 = new_coordinates
        map_dict[deep_1] = pop_1


def up_right_movement(pos1, pos2, pop_number):
    new_coordinates = (pos1+1, pos2+1)
    if new_coordinates not in visitor_list and new_coordinates not in obstacle_areas:
        cost_function = pop_number[0] + 1.4
        element = (cost_function, new_coordinates)
        for a in range(queue_list.qsize()):
            if queue_list.queue[a][1]==new_coordinates:
                if queue_list.queue[a][0]>cost_function:
                    queue_list.queue[a] = element
                    return
                else:
                    return
        queue_list.put(element)
        pop_1 = pop_number[1]
        deep_1 = new_coordinates
        map_dict[deep_1] = pop_1



def up_left_movement(pos1, pos2, pop_number):
    new_coordinates = (pos1-1, pos2+1)
    if new_coordinates not in visitor_list and new_coordinates not in obstacle_areas:
        cost_function = pop_number[0] + 1.4
        element = (cost_function, new_coordinates)
        for a in range(queue_list.qsize()):
            if queue_list.queue[a][1]==new_coordinates:
                if queue_list.queue[a][0]>cost_function:
                    queue_list.queue[a] = element
                    return
                else:
                    return                        
        queue_list.put(element)
        pop_1 = pop_number[1]
        deep_1 = new_coordinates
        map_dict[deep_1] = pop_1


def down_right_movement(pos1, pos2, pop_number):
    new_coordinates = (pos1+1, pos2-1)
    
    if new_coordinates not in visitor_list and new_coordinates not in obstacle_areas:
        cost_function = pop_number[0] + 1.4
        element = (cost_function, new_coordinates)
        for a in range(queue_list.qsize()):
            if queue_list.queue[a][1]==new_coordinates:
                if queue_list.queue[a][0]>cost_function:
                    queue_list.queue[a] = element
                    return
                else:
                    return
        queue_list.put(element)
        pop_1 = pop_number[1]
        deep_1 = new_coordinates
        map_dict[deep_1] = pop_1


def down_left_movement(pos1, pos2, pop_number):
    new_coordinates = (pos1-1, pos2-1)
    if new_coordinates not in visitor_list and new_coordinates not in obstacle_areas:
        cost_function = pop_number[0] + 1.4
        element = (cost_function, new_coordinates)
        for a in range(queue_list.qsize()):
            if queue_list.queue[a][1]==new_coordinates:
                if queue_list.queue[a][0]>cost_function:
                    queue_list.queue[a] = element
                    return
                else:
                    return
        queue_list.put(element)
        pop_1 = pop_number[1]
        deep_1 = new_coordinates
        map_dict[deep_1] = pop_1


def back_track_node(dict, start, goal):
    pop_1 = start
    deep_1 = goal
    dict_key=dict[deep_1]
    map_dict_path.append(deep_1)
    map_dict_path.append(dict_key)
    while dict_key != pop_1:
        dict_key=dict[dict_key]
        map_dict_path.append(dict_key)
    map_dict_path.reverse()
    return map_dict_path

map_dict={}
check = True
obstacle_areas = orientation_block()
user_start = taking_start_from_user()
user_goal = taking_goal_from_user()
start_node = (0, (user_start))


visitor_list=[]
queue_list=PriorityQueue()
queue_list.put(start_node)
map_dict_path=[]

while(True):
    popped_element = queue_list.get(0)
    visitor_list.append(popped_element[1])


    current_position = popped_element[1]
    i = current_position[0]
    j = current_position[1]

    if current_position != user_goal:
        if j+1<251:
            upward_movement(i,j,popped_element)
        if j-1>0:
            downward_movement(i,j,popped_element)
        if i+1<601:
            rightward_movement(i,j,popped_element)
        if i-1>0:
            leftward_movement(i,j,popped_element)
        if j+1<251 and i+1<601:
            up_right_movement(i,j,popped_element)
        if j+1<251 and i-1>0:
            up_left_movement(i,j,popped_element)
        if j-1>0 and i-1>0:
            down_left_movement(i,j,popped_element)
        if j-1>0 and i+1<601:
            down_right_movement(i,j,popped_element)
    else:
        print("succesful")
        backtrack = back_track_node(map_dict, user_start, user_goal)

        game(visitor_list, backtrack)
        break