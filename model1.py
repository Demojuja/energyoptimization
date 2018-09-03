import pandas as pd
import pulp

generators = pd.read_csv('generators_variables_1.csv', sep=';', index_col=['Generators'])
#print(factories)

#print(factories.index)

demand = pd.read_csv('demand_variables_1.csv', sep=';', index_col=['Month'])
print(demand.index)



generatorOut = pulp.LpVariable.dict("genOut",
                                    ((gen, month) for gen in generators.index for month in demand.index),
                                    lowBound=0,
                                    cat='Integer')
