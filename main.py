import Game
import tests
import tests

def main():
    #tests.basic_test(jobs_number = 40, time_range = 40, machine_number = 3, threshold = 10000)
    
    #tests.no_nequilibrioum_test(threshold= 100000)
    tests.test_three_machines_convergence(1000, 1000)


if __name__ == "__main__":
    main()
