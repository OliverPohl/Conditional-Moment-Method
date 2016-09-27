# Conditional-Moment-Method
An implementation of a computational method, which infers information about chemotactic and tumbling behavior from bacterial trajectories. 



  #################   Conditional Moments    ################################################
  
Input: 	 To be found in parameters.py . Essentially data tracks, \Delta t and conditions.
Methods: To be found in conditional_moments.py, which uses data_processing.py . In short, data is processed (data_processing.py) and the moments are calculated
Output:  array "experimental_moments_tensor" gives moments conditioned on conditions (specified in parameters.py) 
	 and for different initial (bootstrapped datasets). It has dimensions: (1+number_of_bootstraps) *   number_of_conditions * maximal_moment . 
Examples:  
	experimental_moments_tensor[0,1,1] : second moment (python starts counting at 0) conditioned on the second condition
	of the original data tracks (first index = 0)
	experimental_moments_tensor[2,2,2] : third moment conditioned on the third condition of the second bootstrapped data tracks 
  
  
  
  ####################   Parameter inference    ###############################################
  
Input: 	 Experimental_moments_tensor, \Delta t, which_moments, i.e., the moments to be used for inference 
Methods: To be found in parameter_inference.py, which uses optimization.py. 
	 For the angular case treated here parameter_inference uses angular_moments.py.
	 In the Main one can specify which bacterium should be treated.
	 If other moments (i.e. for speed statistics) should be used, one needs to replace the angula_moments module and define a new subclass 
	 of TheoreticalMoments.
Functionality: 	 
	 In optimization.py the theoretical moments calculated in angular_moments.py are compared to the experimental ones.
	 The difference is minimized varying the free parameters governing the theoretical moments. 
	 
Output:  Array "inferred_parameter_tensor" give inferred model parameters conditioned on conditions (specified in parameters.py) 
	 and for different initial (bootstrapped datasets). It has dimensions: (1+number_of_bootstraps) *   number_of_conditions * number_of_inferred_parameters . 
	 In the angular case we infer : D_rot, tumble_rate, tumble_distribution_parameters (i.e. for the gamma distribution (sigma, k) )
	 
	 
  ################ Tumble recognizer ######################
  
Input:     	Inferred model parameters (specified in parameters.py), desired alpha_error, test_data
Methods: 	To be found in tumble_recognizer, which also uses data processing to define the stochastic process under consideration.
Functionality:  Likelihood ratio R is used to determine whether a turning angle is due to a tumbling event or Brownian noise. 
		The error of second kind (probability to find a tumble event which is none) is plotted in the terminal.
		
Output: 	Array indices_time_tumble_run_array, dimensions: datapoints*3.  
		column0  ,      column1,                column2, 
		track_ids    track_time_points      run (0) or tumble (1)
		
    We add a plot method, which visualizes the findings for one particular trajectory (to be specified in paramters).
	 
