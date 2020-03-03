#the character # gives us the possibility to write comments
set PROD;
set RAW;
param price{PROD};
param avail{RAW};
param consumption{RAW,PROD};
var production {PROD} >= 0 integer; #amount of production it is important to define the sign of the DV!

maximize Total_Profit: sum{j in PROD} price[j] * production[j];
subject to AvConstr1{i in RAW}: sum {j in PROD} consumption[i,j] * production[j] <= avail[i];

