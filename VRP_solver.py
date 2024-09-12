import numpy as np
import time
import sys

def euclidean_distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def polar_angle(x, y, depot_x, depot_y):
    return np.arctan2(y - depot_y, x - depot_x)

def sweep_algorithm(nodes, depot_index, capacity):
    depot_x, depot_y, _ = nodes[depot_index][:3]  # Extracting only the first three values
    sorted_nodes = sorted(nodes[1:], key=lambda node: polar_angle(node[1], node[2], depot_x, depot_y))
    
    routes = [[]]
    current_capacity = 0
    
    for node in sorted_nodes:
        node_index, node_x, node_y, demand = node[:4]  # Extracting only the first four values
        
        if current_capacity + demand > capacity:
            routes.append([])
            current_capacity = 0
        
        routes[-1].append(node_index)
        current_capacity += demand
    
    return routes


"""This function is crucial for reading and preparing data from VRP dataset files, 
providing necessary information such as node coordinates, demands, depot location,
and vehicle capacity for further processing in VRP algorithms or simulations."""

def read_vrp_dataset(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    nodes = []
    demands = {}
    section = None
    capacity = None  # Initialize capacity variable
    
    for line in lines:
        line = line.strip()
        if line.startswith("NODE_COORD_SECTION"):
            section = "NODE_COORD_SECTION"
        elif line.startswith("DEMAND_SECTION"):
            section = "DEMAND_SECTION"
        elif line.startswith("DEPOT_SECTION"):
            section = "DEPOT_SECTION"
        elif line.startswith("CAPACITY"):  # Extract capacity information
            capacity = int(line.split(":")[1].strip())
        elif line.startswith("EOF"):
            break
        elif section == "NODE_COORD_SECTION":
            data = line.split()
            node_index = int(data[0])
            x = float(data[1])
            y = float(data[2])
            nodes.append((node_index, x, y))
        elif section == "DEMAND_SECTION":
            data = line.split()
            node_index = int(data[0])
            demand = int(data[1])
            demands[node_index] = demand
        elif section == "DEPOT_SECTION":
            depot_index = int(line)
    
    nodes_with_demands = [(node[0], node[1], node[2], demands.get(node[0], 0)) for node in nodes]  # Providing default demand of 0
    
    return nodes_with_demands, depot_index, capacity  # Return capacity along with other data


""""Formatted routes" are the routes that have been processed and 
formatted for human-readable presentation."""

def format_routes(nodes, routes, capacity):
    formatted_routes = []
    for i, route in enumerate(routes):
        route_capacity = sum(nodes[node_index - 1][3] for node_index in route)  # Calculate route capacity
        formatted_route = f"Route {i + 1}: Capacity Used: {route_capacity}/{capacity}, Nodes:[ 1, "
        for node_index in route:
            formatted_route += f"{node_index}, "
        formatted_route += "1]"  # Add square brackets around the depot node index
        formatted_route = f"[{formatted_route}]"  # Enclose the entire route in square brackets
        formatted_routes.append(formatted_route)
        formatted_routes.append("\n\n")  # Add two newline characters after each route
    return formatted_routes


# Calculate total distance traveled by all vehicles
def total_distance(nodes, routes):
    total_distance = 0
    for route in routes:
        prev_node = nodes[0]  # Start from the depot
        for node_index in route:
            node = nodes[node_index - 1]  # Adjust index to start from 0
            total_distance += euclidean_distance(prev_node[1], prev_node[2], node[1], node[2])
            prev_node = node
        # Return to depot
        total_distance += euclidean_distance(prev_node[1], prev_node[2], nodes[0][1], nodes[0][2])
    return total_distance

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <vrp_dataset_path>")
        sys.exit(1)

    file_path = sys.argv[1]  # Path to the input file

    start_time = time.time()

    nodes, depot_index, capacity = read_vrp_dataset(file_path)  # Extract capacity from the dataset

    routes = sweep_algorithm(nodes, depot_index, capacity)
    formatted_routes = format_routes(nodes, routes, capacity)
    
    total_dist = total_distance(nodes, routes)
    
    num_vehicles = len(routes)  # Count the number of routes, each representing a vehicle

    # Print routes
    print(f"Name of Dataset: {file_path}")
    print(f"Capacity: {capacity}")  # Print the extracted capacity
    for route in formatted_routes:
        print(route)

    print(f"Total Nodes Processed: {len(nodes)}")
    print(f"Total Distance Traveled: {total_dist:}")
    print(f"Number of Vehicles Used: {num_vehicles}")
    
    end_time = time.time()
    execution_time = end_time - start_time  # Time in seconds
    print(f"Time for compute: {execution_time:} seconds")



# python VRP_solver.py A1.vrp