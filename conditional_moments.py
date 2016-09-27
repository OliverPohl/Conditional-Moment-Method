import numpy as np
import math
import random as rn
import sys

import data_processing as dp
import parameters as par


class ConditionalMoments:
  def __init__(self):
    self.par_moments = par.ParametersMoments()   
  def give_conditional_moment_tensor(self):
    pass 


class ConditionalMomentsAngle(ConditionalMoments):
  
  def calculate_conditional_moment_tensor(self):
    
    data = dp.Data(self.par_moments.data_path)
    edit_data = dp.EditData(data.data)
    edit_data.edit_data(self.par_moments.min_track_length, self.par_moments.cut_points, self.par_moments.interval_points)
    angle_process = dp.AngleProcess()
    angle_process.calculate_process(edit_data.edited_data)
    dX_data = dp.d_sigma()
    dX_data.create_dX(angle_process.process)
    conditions = MarkovianCondition()
    conditions.calculate_condition(angle_process.process)
    
    exponential_kernel = ExponentialKernelCyclic(self.par_moments.variance_conditions)
    
    moments_tensor = MomentsTensor(self.par_moments.max_moment, self.par_moments.conditions_to_check, self.par_moments.number_of_bootstraps+1, self.par_moments.Delta_t)  
    moments_tensor.create_moments_tensor(exponential_kernel, conditions.condition, dX_data.dX  )   
    return(moments_tensor.moments_tensor)



# The machine data (a list) consists of various arrays each representing one single track. 
#Each track contains various arrays: index, x-position , y-position





class Bootstrap:
  def __init__(self, seed):
    self.seed= seed
    self.mixed_data=[]
    
  def make_mixed_data(self, input_process):
    rn.seed(self.seed)
    indices = [ index[0] for index, stuff, otherstuff in input_process]
    for i in range(len(indices)):
      which_index = rn.choice(indices)   # choose one index randomly from all trajectory labels
      for track in input_process:
	if(track[0][0]== which_index):
	  self.mixed_data.append( track ) 
	  break


class Condition:
  def __init__(self):
    self.condition = []
  def calculate_condition(self):
    pass
  
class MarkovianCondition(Condition):
  def calculate_condition(self, input_process):
    for indices, cond in input_process:
      self.condition.append(  [ indices[0:len(indices)-1], cond[0:len(cond)-1] ]  ) # just without last point of each track since this is not a condition 



class ConditionsAndDX:
  def __init__(self):
    self.conditions_and_dX = []
 
  def create_conditions_and_dX (self, condition, dX): # list of all track arrays each of which having dimension: 3*tracklength. Each row: index, condition, dX    
    it= iter(dX)
    for indices, cond in condition:
      dx = it.next()
      if(len(indices)==len(dx)):
	self.conditions_and_dX.append( [ indices, cond, dx ]  )
      else:
	sys.exit( "ERROR: number of conditions and dx values are not the same for track " + str(indices[0]) )
	
class Kernel:
  def kernel_value (self):
    pass


class ExponentialKernel(Kernel):
  def __init__(self, variance):
    self.variance = variance
  def kernel_value (self, distance_argument_center):
    return(  np.exp( -(distance_argument_center)**2 / (2*self.variance) )  /np.sqrt(2*np.pi * self.variance) )

class ExponentialKernelCyclic(Kernel):
  def __init__(self, variance):
    self.variance = variance
  def kernel_value (self, distance_argument_center):
    return(  np.exp( -(self.angle_distance(distance_argument_center))**2 / (2*self.variance) )  /np.sqrt(2*np.pi * self.variance) )
  def angle_distance(self, angle):
    if(angle>np.pi):
      return(2*np.pi - angle)
    else:
      return(angle)



class Moment:  
  def __init__(self, ExponentialKernel, order, delta_t, condition_check):
    self.ExponentialKernel= ExponentialKernel
    self.delta_t = delta_t
    self.condition_check = condition_check
    self.order = order
  
  def calculate_moment(self, conditions_and_dX):
    moment = 0
    normalization = 0
    for indices, conditions, dx in conditions_and_dX:
      for i in range(len(indices)):
	weight = self.ExponentialKernel.kernel_value(np.abs(conditions[i]- self.condition_check)) 
	moment += (weight * dx[i]**self.order)
	normalization += weight
    if (normalization !=0):	
      return(moment/(self.delta_t*normalization))  
    else:
      sys.exit( "ERROR: No process points!!!" )
      
class MomentsTensor: 
  
  def __init__(self, max_moment, conditions_to_check, number_of_bootstraps, delta_t):
    self.max_moment = max_moment
    self.conditions_to_check = conditions_to_check
    self.number_of_bootstraps = number_of_bootstraps
    self.moments_tensor = np.zeros( (number_of_bootstraps, len(conditions_to_check), self.max_moment ) )
    self.delta_t = delta_t
    
    
  def create_moments_tensor(self, Kernel, condition, dX ):
  # Might want to call the    
    conditions_and_dx = ConditionsAndDX()
    conditions_and_dx.create_conditions_and_dX(condition, dX )
    for boot in range(self.number_of_bootstraps):
      print "bootstrap #" + str(boot)
      if(boot>0):
	booty = Bootstrap(boot) # Watch out: Every time the program runs, it calls the same random instances!
	booty.make_mixed_data(conditions_and_dx.conditions_and_dX)
	mixed_data = booty.mixed_data
      else:   # first input_process is the original data
	mixed_data = np.copy(conditions_and_dx.conditions_and_dX)	  
      for mom in range(self.max_moment):
	for cond in range(len(self.conditions_to_check)): 
	  moment = Moment(Kernel, mom+1, self.delta_t, self.conditions_to_check[cond])
	  self.moments_tensor[boot,cond, mom]= moment.calculate_moment(mixed_data) 
	print  str(mom+1) +". moment done"
    print "All moments calculated"



  
  
    
    
    
    

    