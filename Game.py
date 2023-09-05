import random

def create_jobs(jobs_array, jobs_number, time_range):
    for _ in range(jobs_number):
        random_time = random.randint(1, time_range)
        jobs_array.append(Job(random_time))

def create_machines(machines, machines_number, jobs_array):
    for _ in range(machines_number):
        random_type_index = random.randint(0, 2)
        random_type = Machine.machine_type[random_type_index]
        random_time_index = random.randint(0, 2)
        random_time = Machine.work_times[random_time_index]
        machines.append(Machine(random_time, jobs_array, random_type))
    
def job_assignment(machines, jobs_array):
    for job in jobs_array:
        random_machine_index = random.randint(0, len(machines) - 1)
        machine = machines[random_machine_index]
        machine.add_to_machine(job)

def print_machines_and_jobs(machines):
    print("=" * 50)
    print("Machines and their Jobs:")
    print("=" * 50)
    for machine in machines:
        machine.print_machine_jobs()
        print("-" * 50)

def play(jobs, machines,threshold):
    changed = False
    rounds = 0
    iterations = 0
    count_changes = 0
    for rounds in range(threshold):
        for job in jobs:
            iterations += 1
            better_machine = job.find_better_machine(machines)
            if job.machine_id != better_machine.id:
                job.change_machine(better_machine, machines)
                changed = True
                count_changes += 1
        if not changed:
            break
        changed = False

    return count_changes, rounds, iterations

def determine_job_order(BRD, machines, jobs):
    """Determine the order of jobs based on the specified BRD."""
    if BRD == 'pi1':
        return machines[0].priority
    elif BRD == 'pi2':
        return machines[1].priority
    elif BRD == 'STL':
        return sorted(jobs, key=lambda job: job.time)
    elif BRD == 'LTS':
        return sorted(jobs, key=lambda job: job.time, reverse=True)
    elif BRD == 'random':
        return random.sample(jobs, len(jobs))
    else:
        raise ValueError(f"Unknown BRD: {BRD}")

def is_equilibrium(jobs, machines):
    """Check if all jobs are in their optimal machines."""
    for job in jobs:
        better_machine = job.find_better_machine(machines)
        if job.machine_id != better_machine.id:
            return False
    return True

def play_two(jobs, machines, threshold, BRD):
    count_changes = 0
    iterations = 0

    job_order = determine_job_order(BRD, machines, jobs)

    if BRD == 'random':
        for _ in range(threshold):
            job = random.choice(jobs)
            iterations += 1
            better_machine = job.find_better_machine(machines)
            if job.machine_id != better_machine.id:
                job.change_machine(better_machine, machines)
                count_changes += 1
            # Check for equilibrium after each random job pick
            if is_equilibrium(jobs, machines):
                break
    else:
        changed = False  # Flag to check if any job changed its machine in the current round
        for _ in range(threshold):
            for job in job_order:
                iterations += 1
                better_machine = job.find_better_machine(machines)
                if job.machine_id != better_machine.id:
                    job.change_machine(better_machine, machines)
                    count_changes += 1
                    changed = True  # Job changed its machine

            if not changed:  # If no job changed its machine in the current round, break
                break
            changed = False  # Reset the flag for the next round

    return count_changes, iterations


    

class Machine:
    current_id = 1
    machine_type = ["SPT","LPT","random"]
    work_times = [0.5,1,2]    
    # work_time: The speed of the machine
    # work_list: A list of all jobs currently in the machine
    # priority: A list of job preferences for the machine
    def __init__(self, work_time, jobs, machine_type):
        self.id = Machine.current_id
        Machine.current_id += 1
        self.work_time = work_time
        self.work_list = []
        #Building the priority list based on the specified machine_type
        if machine_type == "default":
            self.priority = jobs
            self.machine_type = "default"   
        elif machine_type == "SPT":
            self.machine_type = machine_type
            self.priority = sorted(jobs, key=lambda job: job.time) # Sort jobs based on their time
        elif machine_type == "LPT":
            self.machine_type = machine_type
            self.priority = sorted(jobs, key=lambda job: job.time, reverse=True) # Sort jobs in reverse order of time
        elif machine_type == "random":
            self.machine_type = machine_type
            jobs_copy = jobs.copy()
            random.shuffle(jobs_copy)# Randomize the job priority
            self.priority = jobs_copy
        else:
            raise ValueError("Invalid machine_type")
    
    #  A helper function to find the index of a job in the priority list
    def priority_index(self, job):
        try:
            index = self.priority.index(job)
            return index
        except ValueError:
            return -1  # If job is not found in the priority list

    def add_to_machine(self, job):
        job.machine_id = self.id
        job_priority = self.priority_index(job)
        i = 0
        current_job_finish_time = (job.time * (1/self.work_time))

        # Calculate the finish time for the new job based on its position in the priority array
        while i < len(self.work_list) and job_priority > self.priority_index(self.work_list[i]):
            current_job_finish_time += (self.work_list[i].time * (1/self.work_time)) # Adding the time, not finish time
            i += 1

        job.finish_time = current_job_finish_time
        self.work_list.insert(i, job)

        # Update the finish times of all jobs that come after the new job's position
        i += 1
        while i < len(self.work_list):
            self.work_list[i].finish_time += (job.time * (1/self.work_time)) # Adding the job time, not finish time
            i += 1

    def remove_from_machine(self, job):
        if not self.work_list: return None
        else:
            i = 0
            # Find the index of the job in the work_list
            while i < len(self.work_list) and not self.work_list[i] == job: i += 1
            if not self.work_list: return None
            else:
                # Update the finish times of all jobs that come after the job that is removed
                i += 1
                while i < len(self.work_list):
                    self.work_list[i].finish_time -= (job.time * (1/self.work_time))
                    i += 1
                job.machine_id = None
                job.finish_time = job.time    
                self.work_list.remove(job)

    def calculate_sum_times(self):
        sum_times = 0
        i = 0
        for job in self.work_list:
            sum_times += job.finish_time
            i += 1
        return sum_times
    
    def print_machine_jobs(self):
        print(f"Machine {self.id} ({self.machine_type}):")
        print(f"Work Time: {self.work_time}")
        self.print_machine_priority()
        print("Jobs:")
        for job in self.work_list:
            print(f"  Job ID: {job.id}, finish time: {job.finish_time}. job time: {job.time}")\
            
    def print_machine_priority(machine):
        priority_ids = [job.id for job in machine.priority]
        print(f"Priority: {' -> '.join(map(str, priority_ids))}")


class Job:
    current_id = 1

    def __init__(self, time):
        self.id = Job.current_id
        Job.current_id += 1
        self.time = time
        self.finish_time = time 
        self.machine_id = None

    def find_better_machine(self, machines_array):
        best_machine = None
        min_time = float('inf')
        for machine in machines_array:
            current_job = self.expected_time_for_machine(machine)
            if min_time > current_job:  
                min_time = current_job
                best_machine = machine
        return best_machine
            
    def expected_time_for_machine(self, machine):
        job_priority = machine.priority_index(self)
        i = 0
        current_job_finish_time = (self.time * (1/machine.work_time))

        # Calculate the finish time for the new job based on its position in the priority array
        while i < len(machine.work_list) and job_priority > machine.priority_index(machine.work_list[i]):
            current_job_finish_time += (machine.work_list[i].time / machine.work_time)
            i += 1

        return current_job_finish_time

    def change_machine(self, new_machine, machine_array):
        old_machine_id = self.machine_id
        for machine in machine_array:
            if machine.id == old_machine_id:
                machine.remove_from_machine(self)
                break
        new_machine.add_to_machine(self)




