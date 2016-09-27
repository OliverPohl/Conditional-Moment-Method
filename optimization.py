import numpy as np
from scipy import optimize



class Optimization : 
  def return_optimized_parameters ():
    return(0)

# This optimiazation procedure searches the best starting value (brute) and terminates by a gradient based minimization procedure
# This class is initialized in the ParametersInference.calculate_inferred_parameters_tensor method. 

class OptimizationBruteThenDescend : 
  def __init__(self,  ranges, function_to_minimize):
    self.ranges = ranges
    self.function_to_minimize = function_to_minimize
  def return_optimized_parameters (self, tools):
    print "Brute+descend optimization procedure starting "
    out= optimize.brute(self.function_to_minimize, self.ranges, args = tools, full_output=True, finish=optimize.fmin ) # finish =None or optimize.fmin
    print "Done. Result: " + str(out[0])
    infered_parameters = out[0]
    error = out[1]
    return(infered_parameters, error)

# Here, the differences of experimental and theoretical data are normalized.
# This class is initialized in the ParametersInference.calculate_inferred_parameters_tensor method. 

class MeanSquaredErrorNormalized :
    
  def calculate_mean_squared_error(self, parameters, function, experimental_data):
    theoretical_data = function(parameters)
    if(theoretical_data.any < 0 ): # exclude unphysical values
      return(10000)
    else:
      moments_diff = (theoretical_data - experimental_data)/ ( (len(experimental_data)+0.0)*experimental_data)
      return( np.sqrt(np.dot(  moments_diff, moments_diff    ))  ) 

