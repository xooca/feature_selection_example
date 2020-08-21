def reward_function(params):
    def get_next5waypoints(cwpnt,index):
        if (cwpnt + index) > len(waypoints):
            diff = (cwpnt + index)-len(waypoints)
            retval = waypoints[diff]
        else:
            retval = waypoints[cwpnt + index]
        return retval

    import math
    # Read input variables
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    direction_stearing=params['steering_angle']
    steering = abs(params['steering_angle'])
    heading = params['heading']
    speed = params['speed']
    progress = params['progress']
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    steps = params['steps']
    all_wheels_on_track = params['all_wheels_on_track']
    reward = 1.0
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
    SPEED_THRESHOLD = 3
    if not all_wheels_on_track:
        reward *= 0.0001
    elif speed < SPEED_THRESHOLD:
        # Penalize if the car goes too slow
        reward *= 0.001
    else:
        # High reward if the car stays on track and goes fast
        if direction_diff > DIRECTION_THRESHOLD:
            reward *= 0.05
        else:
            reward *= 3
    if progress == 100:
        reward *= 5
    return float(reward)

