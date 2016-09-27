import numpy as np
import math
import scipy.special as sc

# Umbrella class. This class or its children are initialized in ParametersInference classes.

class TheoreticalMoments:
  def __init__(self, Delta_t, which_moments):
    self.Delta_t = Delta_t
    self.which_moments = which_moments
  
  def calculate_moments(self, parameters):
    check = np.asarray([self.calculate_moment( parameters, n ) for n in self.which_moments ])
    return( check  )
  
  def calculate_moment(self, parameters, n):
    return(0)  

# Theoretical moments for the turning angle given the shot-noise model

class TheoreticalMomentsAngleShotAndWhiteNoise(TheoreticalMoments):
  def __init__(self, Delta_t, which_moments, MomentsTumbleAngleDistribution):
    TheoreticalMoments.__init__(self, Delta_t, which_moments)
    self.MomentsTumbleAngleDistribution = MomentsTumbleAngleDistribution

  def calculate_moment(self, parameters, n):

    D_rot , tumble_rate= parameters[0:2]
    distribution_parameters = parameters[2:len(parameters)]
    self.MomentsTumbleAngleDistribution.set_distribution_parameters(distribution_parameters)
    
    if(n == 1):
      return( (1.0 - tumble_rate*self.Delta_t)  *  np.sqrt( 4.0*D_rot/(math.pi* self.Delta_t) ) + 
	     tumble_rate*self.MomentsTumbleAngleDistribution.nth_moment(np.pi, 1)      )  

    elif(n == 2):
      return(2*D_rot + tumble_rate*self.MomentsTumbleAngleDistribution.nth_moment( np.pi, 2) )
    
    elif(n == 3):
      return( (1.0 - tumble_rate*self.Delta_t)  *  ( 4.0*np.sqrt(((D_rot)**3.0) * self.Delta_t  /(math.pi) ) ) + tumble_rate*  ( self.MomentsTumbleAngleDistribution.nth_moment(np.pi,3)   + 
	        6*D_rot*self.Delta_t*self.MomentsTumbleAngleDistribution.nth_moment(np.pi,1) )    ) 
    elif(n == 4):
      return(tumble_rate * ( self.MomentsTumbleAngleDistribution.nth_moment(np.pi,4) + 
	     self.Delta_t*2.0*D_rot*6.0 * ( self.MomentsTumbleAngleDistribution.nth_moment(np.pi,2)  ) ) )  

    #elif(n == 5): # mixed term missing !
      #return(tumble_rate * ( self.MomentsTumbleAngleDistribution.nth_moment(np.pi,5) ) ) 
    
    elif(n == 6):
      return(tumble_rate*(self.MomentsTumbleAngleDistribution.nth_moment(np.pi,6)  +  
			  15*self.Delta_t*2.0*D_rot*(self.MomentsTumbleAngleDistribution.nth_moment(np.pi,4 ) ) )  )
   
    #elif(n == 7): # mixed term missing !
      #return(tumble_rate * ( self.MomentsTumbleAngleDistribution.nth_moment(np.pi,7)  )  )
    
    elif(n == 8):
      return(tumble_rate*(28*self.Delta_t*2.0*D_rot*self.MomentsTumbleAngleDistribution.nth_moment(np.pi,6) 
			  +  self.MomentsTumbleAngleDistribution.nth_moment(np.pi, 8.0) ) )

    else:
      print str(n) + "th moment not defined"

# Umbrella class for arbitrary Tumble angle distribution classes

class MomentsTumbleAngleDistribution:
  def __init__(self, distribution_parameters ):
    self.distribution_parameters = distribution_parameters
  
  def set_distribution_parameters(self, distribution_parameters ):
    self.distribution_parameters = distribution_parameters
  
  def nth_moment (self, n):
    return(0)
    
# Moments of the gamma distributions restricted to the interval [0, right_limit]. Used for E. coli  

class MomentsRestrictedGammaDistribution(MomentsTumbleAngleDistribution):
  def nth_moment (self, right_limit, n):
    sigma , k= self.distribution_parameters
    return( (sigma**n)*sc.gammainc(k+n,right_limit/sigma)*sc.gamma(n+k)/(sc.gamma(k)*sc.gammainc(k,right_limit/sigma))    )    



# Moments of the exp-constant distribution restricted to the interval [0, right_limit]. Used for P. putida  

class MomentsExponentialPlusConstant(MomentsTumbleAngleDistribution):
  def nth_moment (self, right_limit, n):
    Delta_beta, constant = self.distribution_parameters
    return( (moment_exp_n(Delta_beta, n) + (constant/(n+1.0))* np.pi**(n+1) )/ normalization(Delta_beta, constant)     )     
  
  def intexp(self,argument, Delta_beta, n):
    tosum = np.zeros(n)
    for i in range(1,n+1):
      tosum[i-1] =  ((0.0+ math.factorial(n))/(0.0+math.factorial(i))) *(Delta_beta*argument)**i* (-1)**(n-i) 
    return( exp(argument*Delta_beta)*( sum( tosum )+ (-1.0)**n * math.factorial(n))/Delta_beta**(n+1) ) 

  def moment(self, Delta_beta, n):
    return( intexp(np.pi, Delta_beta, n) - intexp(0, Delta_beta, n) )
  
  def normalization(self, Delta_beta, constant):
    return( (1/Delta_beta)*(exp(np.pi*Delta_beta)-1) + np.pi*constant)
 
 