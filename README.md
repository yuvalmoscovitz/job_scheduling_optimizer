# Dynamic Job Scheduling Simulation

## Project Overview

This project is a simulation-based study aimed at understanding the dynamics of job scheduling algorithms. Specifically, it evaluates the efficiency of various Best Response Dynamics (BRD) in job scheduling scenarios. The primary metrics for evaluation are the speed of convergence to a Nash equilibrium and the stability of the system under different initial conditions and machine priorities.

## Objectives

- To simulate job scheduling scenarios with multiple machines and jobs.
- To evaluate the performance of different BRD strategies.
- To analyze how machine priorities and initial conditions affect system performance.

## Metrics Evaluated

1. **Changes Count**: Represents the number of times a job changed its machine before reaching equilibrium. A lower value indicates fewer changes, suggesting a more stable system.
2. **Iterations**: Denotes the total number of times we check if a change was needed, until the system reaches equilibrium. A lower value indicates faster convergence.

## Experiments Conducted

The simulation runs multiple experiments with varying parameters such as:

- Number of jobs
- Number of machines
- Machine speeds
- Initial state of the system

Each experiment is repeated multiple times to ensure statistical validity.

## Results and Insights

The simulation generates detailed statistics and visualizations to provide insights into:

- The most efficient BRD strategy for faster convergence.
- The impact of machine priorities on system stability.
- Cases where the system fails to reach equilibrium.

## Contributing

If you're interested in contributing to this research, please feel free to fork the repository and submit a pull request.
