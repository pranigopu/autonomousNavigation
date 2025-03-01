import time
import threading

# Simulated pathfinding function (takes time to compute a new path)
def fake_pathfinding():
    print("Pathfinding started...")
    time.sleep(3)  # Simulate long computation
    print("Pathfinding completed!")
    return [(i, i) for i in range(5)]  # Return a dummy path

# **Test 1: Without Multithreading (Blocking Execution)**
def test_single_threaded():
    print("\n--- Single-Threaded Execution ---")
    start_time = time.time()

    # Simulating agent movement updates before pathfinding
    for i in range(3):
        print(f"Agent moving... Step {i+1}")
        time.sleep(1)  # Simulate movement update delay

    # Pathfinding (BLOCKS execution)
    path = fake_pathfinding()

    # Simulating agent movement updates after pathfinding
    for i, pos in enumerate(path):
        print(f"Agent moving to {pos}")
        time.sleep(1)

    print(f"Total Time (Single-Threaded): {time.time() - start_time:.2f} seconds")

# **Test 2: With Multithreading (Non-Blocking Execution)**
def test_multi_threaded():
    print("\n--- Multi-Threaded Execution ---")
    start_time = time.time()

    # Simulating agent movement updates before pathfinding
    for i in range(3):
        print(f"Agent moving... Step {i+1}")
        time.sleep(1)  # Simulate movement update delay

    # Start pathfinding in a separate thread
    pathfinding_thread = threading.Thread(target=fake_pathfinding)
    pathfinding_thread.start()

    # Continue agent movement updates WHILE pathfinding is running
    for i in range(3):
        print(f"Agent still moving... Step {i+1}")
        time.sleep(1)

    # Ensure pathfinding completes before proceeding
    pathfinding_thread.join()

    # Simulating agent movement updates after pathfinding
    path = [(i, i) for i in range(5)]  # Dummy path
    for i, pos in enumerate(path):
        print(f"Agent moving to {pos}")
        time.sleep(1)

    print(f"Total Time (Multi-Threaded): {time.time() - start_time:.2f} seconds")

# Run both tests
test_single_threaded()
test_multi_threaded()
