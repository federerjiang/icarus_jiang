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

REQ_RATE = 1.0

# Cache eviction policy
CACHE_POLICY = 'LRU'

# Zipf alpha parameter, remove parameters not needed
# ALPHA = [0.6, 0.8, 1.0]
ALPHA = [0.8]

# Total size of network cache as a fraction of content population
# Remove sizes not needed
NETWORK_CACHE = [0.02, 0.05, 0.1, 0.2, 0.3, 0.5]
# NETWORK_CACHE = [0.3]

# HEIGHT = 4
BRANCH = [2]

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
     # 'CMEDGE',
     # 'CLCE',
     # 'CCLCE',
     'CTEDGE',
     'CB',
     # 'NCMEDGE',
     # 'RAND_CHOICE',     # Random choice: cache in one random cache on path
     # 'RAND_BERNOULLI',  # Random Bernoulli: cache randomly in caches on path
             ]

# Instantiate experiment queue
EXPERIMENT_QUEUE = deque()

# Build a default experiment configuration which is going to be used by all
# experiments of the campaign
default = Tree()



trace_folder = "/home/federerjiang/workplace/icarus_jiang/trace/Trace4/"
trace_file = trace_folder + "SNMtrace.txt"
contents = trace_folder + "contents.txt"
N_CONTENTS = 1761204
N_WARMUP_REQUESTS =  1000000
N_MEASURED_REQUESTS = 3773900

default['workload'] = {'name':  'TRACE_DRIVEN',
                       'reqs_file': trace_file,
                       'contents_file': contents,
                       'n_contents': N_CONTENTS,
                       'n_warmup': N_WARMUP_REQUESTS,
                       'n_measured': N_MEASURED_REQUESTS}

'''
* name: TRACE_DRIVEN
 * args:
    * reqs_file: the path to the requests file
    * contents_file: the path to the contents file
    * n_contents: number of content objects
    * n_warmup: number of warmup requests
    * n_measured: number of measured requests
'''
default['cache_placement']['name'] = 'UNIFORM'
default['content_placement']['name'] = 'UNIFORM'
default['cache_policy']['name'] = CACHE_POLICY
# default['topology']['name'] = 'SINET-EDGE',
# default['topology']['h'] = HEIGHT


TOPOLOGIES =  [
        # 'GEANT',
        # 'SINET',
        'SINET-EDGE',
        # 'WIDE',
        # 'GARR',
        # 'TISCALI',
        # 'RANDOM',
              ]


for alpha in ALPHA:
    for network_cache in NETWORK_CACHE:
        for strategy in STRATEGIES:
            for topology in TOPOLOGIES:
              experiment = copy.deepcopy(default)
              experiment['workload']['alpha'] = alpha
              experiment['strategy']['name'] = strategy
              experiment['topology']['name'] = topology
              experiment['cache_placement']['network_cache'] = network_cache
              experiment['desc'] = "Alpha: %s, strategy: %s, topology: %s, network cache: %s" \
                                 % (str(alpha), strategy, topology, str(network_cache))
              EXPERIMENT_QUEUE.append(experiment)