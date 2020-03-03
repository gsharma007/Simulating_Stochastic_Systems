set comps; /*index i*/
set machs; /*index m*/

param mach_cap{machs};
param cost_comp{comps};
param con_comp_mach{comps,machs};

var x{comps} >=0 ;  /*# of comps to be produced*/
var theta;

/* objective function */
maximize revenue: sum {i in machs} cost_comp[i]*x[i] +theta;

/* constraints*/
subject to capacity_constraint {m in machs}: sum{i in comps} con_comp_mach[i,m]*x[i] <= mach_cap[m];
#subject to demand_constraint {j in prods, s in scens}: y[j,s] <= d[j,s];
#subject to component_availability {i in comps, s in scens}: sum{j in prods} W[i,j]*y[j,s] <= x[i];


#Notes:
#sub problem- always gives lower bound in case of minimization problem
#master problem- does this give upper bound?
#Lshaped as two minimization problems as master and sub problem
#cut formulation- Always formulate as the minimization problems
#so that cuts can be made without worrying about the sign of the dual variable
#is first stage problem- auxiliary?
#second stage problem vs the feasibility problem, what's the difference?
#optimality cut, one in each iteration but feasibility cuts can be multiple
