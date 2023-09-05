import Game
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statistics


def basic_test(jobs_number, time_range, machine_number, threshold):
    jobs = []
    Game.create_jobs(jobs, jobs_number, time_range)
    machines = []
    Game.create_machines(machines, machine_number, jobs)
    Game.job_assignment(machines, jobs)
    
    count_changes, rounds, _ = Game.play(jobs, machines, threshold)
    if rounds < threshold - 1 :
        print("The system reached equilibrium in " + str(count_changes) + " steps")
    else:
        print("The system did not reach equilibrium")
    Game.print_machines_and_jobs(machines)


def no_nequilibrioum_test(threshold):
    jobs = []
    machines = []
    no_nequilibrioum_example(jobs,machines)
    count_changes, rounds, _ = Game.play(jobs, machines, threshold)
    if rounds < threshold - 1 :
        print("The system reached equilibrium in " + str(count_changes) + " steps")
    else:
        print("The system did not reach equilibrium")

def no_nequilibrioum_example(jobs, machines):
    j1 = Game.Job(4)
    j2 = Game.Job(3)
    j3 = Game.Job(5.5)
    j4 = Game.Job(9.25)
    jobs.extend([j1,j2,j3,j4])

    machines.append(Game.Machine(1, [j1,j2,j3,j4], "default"))
    machines.append(Game.Machine(0.5, [j4,j2,j3,j1], "default"))
    machines.append(Game.Machine(0.25, [j4,j2,j3,j1], "default"))

def create_two_machines(jobs_number, time_range, job_time = 0.5):
    jobs = []
    Game.create_jobs(jobs, jobs_number, time_range)
    machines = []
    machines.append(Game.Machine(1, jobs, "random"))
    machines.append(Game.Machine(job_time, jobs, "random"))
    
    np_machine1 = np.array(machines[0].priority)
    np_machine2 = np.array(machines[1].priority)
    while np.array_equal(np_machine1,np_machine2):
        machines.remove(machines[1])
        machines.append(Game.Machine(0.5, jobs, "random"))
        np_machine1 = np.array(machines[0].priority)
        np_machine2 = np.array(machines[1].priority)

    return jobs, machines


def two_machines_test(reps, jobs_number, time_range, job_time, threshold, BRD):
    counts = []
    iterations_list = []
    for _ in range(reps):
        jobs, machines = create_two_machines(jobs_number, time_range, job_time)
        count_changes, iterations = Game.play_two(jobs, machines, threshold, BRD)
        counts.append(count_changes)
        iterations_list.append(iterations)
    return counts, iterations_list



def run_tests_and_visualize(reps=100, jobs_number=10, time_range=5, job_time=0.5, threshold=1000):
    BRDs = ['pi1', 'pi2', 'random', 'STL', 'LTS']
    
    for BRD in BRDs:
        print(f"Running tests for BRD: {BRD}\n{'='*70}")
        
        # Run the two machines test
        counts, iterations_list = two_machines_test(reps, jobs_number, time_range, job_time, threshold, BRD)

        # Compute statistics
        avg_count, median_count, std_dev_count = compute_statistics(counts)
        avg_iterations, median_iterations, std_dev_iterations = compute_statistics(iterations_list)

        # Print statistics
        print(f"Count Changes - Avg: {avg_count}, Median: {median_count}, Std Dev: {std_dev_count}")
        print(f"Iterations - Avg: {avg_iterations}, Median: {median_iterations}, Std Dev: {std_dev_iterations}")

        # Visualize data
        visualize_data(counts, f"Count Changes ({BRD})")
        visualize_data(iterations_list, f"Iterations ({BRD})")

def compute_statistics(data):
    avg = statistics.mean(data)
    median = statistics.median(data)
    std_dev = statistics.stdev(data)
    return avg, median, std_dev

def visualize_data(data, title):
    # Set the style and context for Seaborn plots
    sns.set_style("whitegrid")
    sns.set_context("talk")

    plt.figure(figsize=(15, 5))

    # Histogram with KDE
    plt.subplot(1, 2, 1)
    sns.histplot(data, kde=True, color=sns.color_palette("coolwarm", 7)[4])
    plt.title(f'Histogram with KDE for {title}')
    plt.xlabel(title)
    plt.ylabel('Frequency')

    # Boxplot
    plt.subplot(1, 2, 2)
    sns.boxplot(data=data, color=sns.color_palette("coolwarm", 7)[2])
    plt.title(f'Boxplot for {title}')
    plt.xlabel(title)

    plt.tight_layout()
    plt.show()
 
def initialize_machines(jobs):
    """Initialize three machines with specified work times and random priorities."""
    machines = []
    machines.append(Game.Machine(1, jobs, "random"))
    machines.append(Game.Machine(1.5, jobs, "random"))
    machines.append(Game.Machine(2, jobs, "random"))
    return machines

def initialize_jobs():
    """Initialize six jobs with random times between 1 and 10."""
    return [Game.Job(random.uniform(1, 10)) for _ in range(6)]

def assign_to_fastest_machine(jobs, machines):
    """Assign all jobs to the fastest machine."""
    for job in jobs:
        job.change_machine(machines[2], machines)

def test_three_machines_convergence(reps = 1000, threshold = 1000):
    non_converging_inputs = []

    for _ in range(reps):
        # Initialize jobs and machines
        jobs = initialize_jobs()
        machines = initialize_machines(jobs)
        
        # Assign all jobs to the fastest machine
        assign_to_fastest_machine(jobs, machines)
        
        # Play the game and check for convergence
        _, rounds, _ = Game.play(jobs, machines, threshold)
        
        # If the system did not converge, save the input
        if rounds == threshold - 1:
            non_converging_inputs.append((jobs, machines))

    # Print non-converging inputs
    for idx, (jobs, machines) in enumerate(non_converging_inputs, 1):
        print(f"Non-converging input {idx}:")
        
        # Print jobs with rounded times
        job_times = [round(job.time, 3) for job in jobs]
        print("Jobs:", job_times)
        
        # Print machine priorities as rounded job times
        for machine in machines:
            priority_times = [round(job.time, 3) for job in machine.priority]
            print(f"Machine {machine.id} Priority:", priority_times)
        
        # Print initial state as job times for the machine with work_time of 2
        print("Initial State:", job_times)
        print("--------------------------------------------------")





