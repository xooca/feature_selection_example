def reward_function(params):
    def get_next5waypoints(cwpnt,index):
        # = (cwpnt + index)
        if (cwpnt + index) == len(waypoints):
            retval = waypoints[0]
        elif (cwpnt + index) > len(waypoints):
            diff = (cwpnt + index)-len(waypoints)
            retval = waypoints[diff]
        else:
            retval = waypoints[cwpnt + index]
        return retval
    import math
    # Read input variables
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    speed = params['speed']
    progress = params['progress']
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    steps = params['steps']
    all_wheels_on_track = params['all_wheels_on_track']
    # Initialize the reward with typical value
    reward = 10
    # Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    # Convert to degree
    track_direction = math.degrees(track_direction)
    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff
    # Penalize the reward if the difference is too large
    DIRECTION_THRESHOLD = 10.0
    next_point_1 = get_next5waypoints(closest_waypoints[0],1)
    next_point_2 = get_next5waypoints(closest_waypoints[0],2)
    next_point_3 = get_next5waypoints(closest_waypoints[0],3)
    next_point_4 = get_next5waypoints(closest_waypoints[0],4)
    next_point_5 = get_next5waypoints(closest_waypoints[0],4)
    ind1 = next_point_1[0] > next_point_2[0] > next_point_3[0] > next_point_4[0] > next_point_5[0] 
    ind2 = next_point_1[0] < next_point_2[0] < next_point_3[0] < next_point_4[0] < next_point_5[0] 
    ind3 = next_point_1[1] > next_point_2[1] > next_point_3[1] > next_point_4[1] > next_point_5[1] 
    ind4 = next_point_1[1] < next_point_2[1] < next_point_3[1] < next_point_4[1] < next_point_5[1] 
    SPEED_TRESHOLD = 2
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    if direction_diff > DIRECTION_THRESHOLD:
        reward = reward - 5
    if distance_from_center <= marker_1:
        if (ind1 and ind3) or (ind2 and ind4):
            if speed < SPEED_TRESHOLD:
                reward = reward - 5
            else:
                reward = reward + 20
        else:
            reward = reward + 10
    elif distance_from_center <= marker_2:
        if (ind1 and ind3) or (ind2 and ind4):
            if speed < SPEED_TRESHOLD:
                reward = reward - 5
            else:
                reward = reward + 10
        else:
            reward = reward + 5
    elif distance_from_center <= marker_3:
         if (ind1 and ind3) or (ind2 and ind4):
            if speed < SPEED_TRESHOLD:
                reward = reward - 5
            else:
                reward = reward + 5
        else:
            reward = reward + 1
    else:
        reward = 1e-3  # likely crashed/ close to off track
    if not all_wheels_on_track:
        reward = reward - 10
    else:
        reward = reward + params["progress"]/5
    if progress == 100: 
        reward = reward + 20
    return float(reward)

