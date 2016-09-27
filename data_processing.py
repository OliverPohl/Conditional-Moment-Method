import numpy as np
import math




class Data:  
  def __init__(self, data_path, indices_path=None): # in indices_path we find selected indices (seperated by ',') 
      data = np.loadtxt(data_path)
      if (indices_path == None):
	indices = np.sort( np.unique(data[:,0]))
      else:
	indices= [ [ float( x ) for x in row.split(',') if x.strip() ] for row in open( indices_path, 'rt' ) ]  
	indices= sort(list(sum(indices, []) ))# hack to flatten indices
      self.data = [  data[ data[:,0]==index ] for index in indices]
      del(data)


class EditData:
  def __init__(self, data):
    self.edited_data = np.copy(data)    
    
  def edit_data(self, min_track_length, cut_points, interval_points):
    self.edited_data=[track[cut_points:len(track)-cut_points: interval_points,:] for track in self.edited_data if len(track) > min_track_length]
    print "long enough tracks selected, cut and thinned"

# Calculate stochastic processes: angle or speed

class StochasticProcess():
  def __init__(self):
    self.process = []
    
  def calculate_process(self, edited_data):
    return(0)

class SpeedProcess(StochasticProcess):
  def __init__(self, delta_t):
    self.delta_t
  def calculate_process(self, edited_data):
    for track in edited_data:
      X = track[:,2]
      Y = track[:,3]
      length = len(X)
      speeds = np.sqrt(  (X[1:length]-X[0:length-1]  )**2 + (Y[1:length]-Y[0:length-1]  )**2   )/delta_t
      self.process.append( np.vstack( (traj*np.ones(len(angle)),  angle )) )
    print "process calculated"  
      
class AngleProcess(StochasticProcess):

  def calculate_process(self, edited_data):
    for track in edited_data:
      X = track[:,2]
      Y = track[:,3]
      length = len(X)
      angle = np.arctan2( Y[1:length]-Y[0:length-1]  ,  X[1:length]-X[0:length-1]   )
      self.process.append( np.vstack( (track[0,0]*np.ones(len(angle)),  angle )) )
    self.process = np.asarray(self.process)
    print "process calculated"  



class dX: 
  def __init__(self):
    self.dX = []
  def create_dX(self, X_process):
    return(0)
  
  
class d_sigma(dX) :
  def create_dX(self, X_process):
    for track in X_process:
      values = track[1] 
      self.dX.append( self.angle_distance( np.abs( values[1:len(values) ] - values[0:len(values)-1]) )  )
      
  def create_dX_and_index(self, X_process):
    for track in X_process:
      values = track[1] 
      self.dX.append( np.asarray( [ track[0][0:len(values)-1], self.angle_distance( np.abs( values[1:len(values) ] - values[0:len(values)-1]) )] )  )      
      
        
  def angle_distance(self, angle):
    angle[angle>np.pi]= 2*np.pi - angle[angle>np.pi]
    return(angle)
  
  
class d_speed(dX) :
  def create_dX(self, X_process):
    for track in X_process:
      values = track[1] 
      self.dX.append( values[1:len(values) ] - values[0:len(values)-1] )
        


  
  
    
    
    
    

    