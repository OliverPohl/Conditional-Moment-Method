import numpy as np

import conditional_moments as cm
import parameter_inference as par_inf
import tumble_recognizer as tumble


def main():
  
  #################   Conditional Moments    ################################################

  conditional_moments = cm.ConditionalMomentsAngle()
  experimental_moments_tensor = conditional_moments.calculate_conditional_moment_tensor()

  ####################   Parameter inference    ###############################################

  parameter_inference = par_inf.ParametersInferenceEcoli(conditional_moments.par_moments.Delta_t)
  inferred_parameter_tensor , mean_square_error_tensor = parameter_inference.calculate_inferred_parameters_tensor(experimental_moments_tensor)

  ################ Tumble recognizer ######################

  tumble_or_run =  tumble.TumbleOrRun()

  indices_time_tumble_run_array = tumble_or_run.calculate_parameters_tensor()
  tumble_or_run.plot_trajectory_tumble_run(indices_time_tumble_run_array)

if __name__ == "__main__":
    main()