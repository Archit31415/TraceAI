def calculate_trajectory(velocity, angle)
    gravity = 9.81
    return (velocity ** 2) / gravity

if __name__ == "__main__":
    print(calculate_trajectory(100, 45))