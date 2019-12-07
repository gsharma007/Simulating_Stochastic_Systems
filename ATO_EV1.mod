set comps;
set prods;
set machs;
set scens;

param p{s in scens};
param c{i in comps};
param r{j in prods};
param d{j in prods, s in scens};
param mc{m in machs};
param W{i in comps, j in prods};
param A{i in comps, m in machs};
param x{i in comps};
param s;

var y{j in prods}>=0;

maximize profiteev: -sum{i in comps} c[i]*x[i] + sum{j in prods} r[j]*y[j];

subject to demand{j in prods}: y[j]<=d[j,s];
subject to componentav{i in comps}: sum{j in prods} W[i,j]*y[j] - x[i] <=0;