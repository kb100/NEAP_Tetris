#--- parameters for the XOR-2 experiment ---#

[NEAT] 
fitness_criterion = max #how to compute termination
fitness_threshold = 3.9 #if fit>"this "number" evolution terminates
#no_fitness_termination = True #if true, then  above are ignored
pop_size = 150 #number of individual"s in ea. generation
reset_on_extinction = False # If TRUE, new population if all die

[DefaultGenome]
# node activation options
activation_default = sigmoid #activation function for NEW nodes
activation_mutate_rate = 0.0 #probability that activation func will change
activation_options = sigmoid #act. func. for nodes

# node aggregation options 
aggregation_default = sum # agg. function for NEW nodes
aggregation_mutate_rate = 0.0  # prob that agg. func will change  
aggregation_options = sum #agg. func. for nodes

# node bias options  just assume guassian error and change curve
bias_init_mean = 0.0  
bias_init_stdev = 1.0 
bias_max_value = 30.0 
bias_min_value = -30.0 
bias_mutate_power = 0.5 
bias_mutate_rate = 0.7 
bias_replace_rate = 0.1

# genome compatibility options
compatibility_disjoint_coefficient = 1.0 # genomic distance threshold
compatibility_weight_coefficient = 0.5 # multipler distance 

# connection add/remove rates
conn_add_prob = 0.5 
conn_delete_prob = 0.5

# connection enable options
enabled_default = True 
enabled_mutate_rate = 0.01 # change of enable chance
feed_forward = True # networks will never be recurrent
initial_connection = full # not described in documentation

# node add/remove rates
node_add_prob = 0.2  
node_delete_prob = 0.2

# network parameters
num_hidden = 0 
num_inputs = 2
num_outputs = 6

# node response options multipliers
response_init_mean = 1.0 
response_init_stdev = 0.0 
response_max_value = 30.0 
response_min_value = -30.0 
response_mutate_power = 0.0 
response_mutate_rate = 0.0 
response_replace_rate = 0.0

# connection weight options 
weight_init_mean = 0.0 
weight_init_stdev = 1.0 
weight_max_value = 30 
weight_min_value = -30
weight_mutate_power = 0.5 
weight_mutate_rate = 0.8 
weight_replace_rate = 0.1

[DefaultSpeciesSet] 
compatibility_threshold = 3.0 # Genomic Distance  for SPECIES

[DefaultStagnation] 
species_fitness_func = max # function for species fitness
max_stagnation = 20  # number of gens allowed without improvement
species_elitism = 2	 # species protected from stagnation

[DefaultReproduction] 
elitism = 2 #choose best 2 and reproduce in speieces 
survival_threshold = 0.2 #fraction allowed to reproduce in ea. gen.


