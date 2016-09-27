import numpy as np
from scipy import optimize

import optimization as opt
import angular_moments as mom
import parameters as par



# Subsumes methods together and gives the inferred parameters

class ParametersInference():
  def __init__(self, Delta_t):
    self.par_inference = par.SettingParameterInference()
    self.Delta_t =Delta_t
    self.theoretical_moments = mom.TheoreticalMoments(Delta_t, self.par_inference.which_moments)
    
  def calculate_inferred_parameters_tensor(self, experimental_moments_tensor):
    mean_squared =  opt.MeanSquaredErrorNormalized() 
    optimization = opt.OptimizationBruteThenDescend(self.par_inference.ranges_brute_search, mean_squared.calculate_mean_squared_error)
    infer_parameter_tensor =  InferParameterTensor(np.shape(experimental_moments_tensor[:,:,0]))
    infer_parameter_tensor.calculate_parameter_tensor(experimental_moments_tensor[:,:, self.par_inference.which_moments-1], self.theoretical_moments.calculate_moments, optimization) 
    return(np.array(infer_parameter_tensor.parameter_tensor), np.array(infer_parameter_tensor.error_tensor)) # creates moments tensor with dimensions :     number_of_bootstraps *  max_moment * length(conditions_to_check) 


class ParametersInferenceEcoli(ParametersInference):
  def __init__(self, Delta_t):
    ParametersInference.__init__(self,  Delta_t)
    self.moments_tumble_angle_distribution = mom.MomentsRestrictedGammaDistribution( (1,1) )
    self.theoretical_moments = mom.TheoreticalMomentsAngleShotAndWhiteNoise(self.Delta_t, self.par_inference.which_moments, self.moments_tumble_angle_distribution)
    
    
class ParametersInferencePPutida(ParametersInference):
  def __init__(self, Delta_t):
    ParametersInference.__init__(self, Delta_t)
    self.moments_tumble_angle_distribution = mom.MomentsRestrictedGammaDistribution( (1,1) )
    self.theoretical_moments = mom.TheoreticalMomentsAngleShotAndWhiteNoise(self.Delta_t, self.par_inference.which_moments, self.moments_tumble_angle_distribution)
    
        
  
    
# Prepares the infered_parameter tensor    

class InferParameterTensor:
  def __init__(self, dimensions_tensor):
    self.parameter_tensor = [ [ [] for x in range(dimensions_tensor[1])  ]  for x in range(dimensions_tensor[0]) ] 
    self.error_tensor = [ [ [] for x in range(dimensions_tensor[1])  ]  for x in range(dimensions_tensor[0]) ] 
    self.dimensions_tensor = dimensions_tensor
  
  def calculate_parameter_tensor(self, experimental_moments_tensor, calculate_theoretical_moments, optimization) :
    for boot in range(self.dimensions_tensor[0]) : 
      for cond in range(self.dimensions_tensor[1]) : 
	inferred_params, error = optimization.return_optimized_parameters( (calculate_theoretical_moments, experimental_moments_tensor[boot, cond, :]) )
	self.parameter_tensor[boot][cond] = inferred_params  ## TODO !!
	self.error_tensor[boot][cond] = error ## TODO !!




 