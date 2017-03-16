from multiprocessing import cpu_count
from collections import deque
import copy
from icarus.util import Tree

############################## GENERAL SETTINGS ##############################

# Level of logging output
# Available options: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = 'INFO'

# If True, executes simulations in parallel using multiple processes
# to take advantage of multicore CPUs
PARALLEL_EXECUTION = True

# Number of processes used to run simulations in parallel.
# This option is ignored if PARALLEL_EXECUTION = False
N_PROCESSES = cpu_count()

# Granularity of caching.
# Currently, only OBJECT is supported
CACHING_GRANULARITY = 'OBJECT'

# Format in which results are saved.
# Result readers and writers are located in module ./icarus/results/readwrite.py
# Currently only PICKLE is supported 
RESULTS_FORMAT = 'PICKLE'

# Number of times each experiment is replicated
# This is necessary for extracting confidence interval of selected metrics
N_REPLICATIONS = 1

# List of metrics to be measured in the experiments
# The implementation of data collectors are located in ./icaurs/execution/collectors.py
# Remove collectors not needed
DATA_COLLECTORS = [
           'CACHE_HIT_RATIO',   # Measure cache hit ratio 
           'LATENCY',           # Measure request and response latency (based on static link delays)
           # 'LINK_LOAD',         # Measure link loads
           # 'PATH_STRETCH',      # Measure path stretch
                   ]



########################## EXPERIMENTS CONFIGURATION ##########################

# Default experiment values, i.e. values shared by all experiments

# Number of content objects
N_CONTENTS = 3*10**5

# Number of content requests generated to pre-populate the caches
# These requests are not logged
N_WARMUP_REQUESTS = 1*10**6

# Number of content requests that are measured after warmup
N_MEASURED_REQUESTS = 3*10**6

# Number of requests per second (over the whole network)
REQ_RATE = 1.0

# Cache eviction policy
CACHE_POLICY = 'LRU'

# Zipf alpha parameter, remove parameters not needed
# ALPHA = [0.6, 0.8, 1.0]
ALPHA = [0.8]

# Total size of network cache as a fraction of content population
# Remove sizes not needed
NETWORK_CACHE = [0.02, 0.05, 0.07, 0.1, 0.13, 0.17, 0.2, 0.3, 0.5]



STRATEGIES = [
     'LCE',             # Leave Copy Everywhere
     # 'NO_CACHE',        # No caching, shortest-path routing
     # 'HR_SYMM',         # Symmetric hash-routing
     # 'HR_ASYMM',        # Asymmetric hash-routing
     # 'HR_MULTICAST',    # Multicast hash-routing
     # 'HR_HYBRID_AM',    # Hybrid Asymm-Multicast hash-routing
     # 'HR_HYBRID_SM',    # Hybrid Symm-Multicast hash-routing
     # 'CL4M',            # Cache less for more
     'PROB_CACHE',      # ProbCache
     'LCD',             # Leave Copy Down
     'MEDGE',
     'CMEDGE',
     # 'CLCE',
     # 'CCLCE',
     'CB',
     # 'NCMEDGE',
     # 'CTEDGE',
     # 'RAND_CHOICE',     # Random choice: cache in one random cache on path
     # 'RAND_BERNOULLI',  # Random Bernoulli: cache randomly in caches on path
             ]

# Instantiate experiment queue
EXPERIMENT_QUEUE = deque()

# Build a default experiment configuration which is going to be used by all
# experiments of the campaign
default = Tree()

default['workload'] = {'name':       'STATIONARY',
                       'n_contents': N_CONTENTS,
                       'n_warmup':   N_WARMUP_REQUESTS,
                       'n_measured': N_MEASURED_REQUESTS,
                       'rate':       REQ_RATE}



default['cache_placement']['name'] = 'UNIFORM'
default['content_placement']['name'] = 'UNIFORM'
default['cache_policy']['name'] = CACHE_POLICY
default['topology']['name'] = 'RANDOM3'
# default['topology']['h'] = HEIGHT


for alpha in ALPHA:
    for network_cache in NETWORK_CACHE:
        for strategy in STRATEGIES:
            experiment = copy.deepcopy(default)
            experiment['workload']['alpha'] = alpha
            experiment['strategy']['name'] = strategy
            experiment['cache_placement']['network_cache'] = network_cache
            experiment['desc'] = "Alpha: %s, strategy: %s, topology: %s, network cache: %s" \
                                 % (str(alpha), strategy, 'GEANT', str(network_cache))
            EXPERIMENT_QUEUE.append(experiment)