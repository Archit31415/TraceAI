def infinite_recursive_call(depth):
    if depth % 100 == 0:
        print(f"Reached depth: {depth}")
        
    return infinite_recursive_call(depth + 1)

if __name__ == "__main__":
    infinite_recursive_call(1)