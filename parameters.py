import numpy as np


class ParametersMoments:
  def __init__(self):
    self.dt_data = 0.05
    self.max_moment= 8
    self.Delta_t= 0.5  # putida 0.3
    self.number_of_conditions = 2.
    self.number_of_bootstraps = 0
    self.min_track_length= 10
    self.conditions_to_check = np.arange(-np.pi, np.pi+0.01, (2*np.pi)/self.number_of_conditions )
    self.cut_points = 10
    self.interval_points = int(self.Delta_t/self.dt_data) 
    self.variance_conditions = 1000 # ((np.pi/self.number_of_conditions))**2

    self.data_path = ""   # To be set

class SettingParameterInference:
  def __init__(self):
    self.which_moments = np.array([1,2,3,4,6,8])
    self.ranges_brute_search = (slice(0.01, 0.1, 0.01), slice(0.1, 0.7, 0.02), slice(0.1, 0.7, 0.1), slice(2, 8, 0.25))




class ParametersTumbleRec:
  def __init__(self):
    self.alpha_error = 0.05
    k_gamma = 2.73
    sigma_gamma = 0.64
    right_limit = np.pi
    self.distribution0_parameters = [k_gamma, sigma_gamma, right_limit]
    Drot = 0.06
    sigma_normal = math.sqrt(2*Drot*self.Delta_t)
    self.distribution1_parameters = [sigma_normal, right_limit]
    self.test_data_path = ""   # To be set
