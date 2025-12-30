# Python N-Queens Genetic Algorithm Project

## n-Queens Solver using a Genetic Algorithm
A visual and algorithmic solution to the n-Queens problem implemented using a Genetic Algorithm (GA) and rendered in real time with Pygame.

This project works with Python and algorithm design to demonstrate the application of evolutionary computation techniques to a classic constraint-satisfaction and combinatorial optimization problem.

## Overview

The n-Queens problem asks:

> How can *n* queens be placed on an *n × n* chessboard so that no two queens attack each other?

This project solves the problem using a Genetic Algorithm, evolving a population of candidate solutions over generations by applying:
- Fitness evaluation  
- Probabilistic parent selection  
- Crossover  
- Mutation  

The best solution from each generation is visualized live using Pygame.

## Genetic Algorithm Design

### Representation
- Each individual solution is a list of unique board positions
- Each position represents a queen’s location on the board

### Fitness Function
- Fitness is defined as the number of attacking queen pairs
- Lower fitness values are better
- A fitness of 0 indicates a valid solution

Attacks are calculated using:
- Vertical conflicts  
- Horizontal conflicts  
- Diagonal conflicts

### Selection
- Parents are chosen using fitness-weighted probabilistic selection
- Every candidate has a base chance to be selected
- Fitness influence is amplified using an exponential modifier to favor stronger solutions while maintaining population diversity

### Crossover
- Offspring are created using a midpoint crossover
- Parent genes are merged while maintaining unique board positions

### Mutation
- Random mutation occurs with a small probability
- A queen’s position is replaced with a new valid, unused location

## Visualization

- Implemented using Pygame
- Chessboard updates in real time
- Queens are rendered as red circles
- Current generation number is displayed on screen

This allows for direct observation of:
- Evolutionary progress
- Convergence behavior
- Genetic diversity across generations

## Technologies Used

- Python
- Pygam
- Genetic Algorithms
- Evolutionary Computation
- Constraint Satisfaction

## How to Run

### 1. Clone the repository
```bash
git clone https://github.com/ZanePeck01/python-genetic-algorithm-project.git
cd python-genetic-algorithm-project
```
Once in the repository, run this command to start the program:
```bash
python board.py
