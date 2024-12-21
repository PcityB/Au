from deap import base, creator, tools, algorithms
import numpy as np

def setup_ga():
    """Setup DEAP Genetic Algorithm framework."""
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    
    toolbox = base.Toolbox()
    toolbox.register("attr_float", np.random.uniform, 0, 1)
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr_float, n=100)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    
    toolbox.register("mate", tools.cxBlend, alpha=0.5)
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.1)
    toolbox.register("select", tools.selTournament, tournsize=3)
    
    return toolbox

def fitness_function(individual, target_grid):
    """Fitness based on similarity with target grid."""
    diff = np.abs(np.array(individual) - np.array(target_grid).flatten())
    return -np.sum(diff),  # Negative because DEAP minimizes fitness

def evolve_population(target_grid, toolbox):
    """Run GA to optimize prototype patterns."""
    population = toolbox.population(n=100)
    
    toolbox.register("evaluate", fitness_function, target_grid=target_grid)
    
    for gen in range(50):
        offspring = algorithms.varAnd(population, toolbox,
                                       cxpb=0.5,
                                       mutpb=0.2)
        fits = map(toolbox.evaluate, offspring)
        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit
        
        population[:] = toolbox.select(offspring, k=len(population))
    
    best_pattern = tools.selBest(population, k=1)[0]
    return np.reshape(best_pattern, target_grid.shape)
