import pandas as pd
import pulp

generators = pd.read_csv('generators_variables_1.csv', sep=';', index_col=['Month', 'Generator'])
#print(generators)

#print(generators.index)

demand = pd.read_csv('demand_variables_1.csv', sep=';', index_col=['Month'])
#print(demand.index)



generatorOut = pulp.LpVariable.dicts("genOut",
                                    ((month, gen) for month, gen in generators.index),
                                    lowBound=0,
                                    cat='Integer')
generator_status = pulp.LpVariable.dicts("gen_status",
                                         ((month, gen) for month, gen in generators.index),
                                         cat='Binary')
switch_on = pulp.LpVariable.dicts("switch_on",
                                  ((month, gen) for month, gen in generators.index),
                                  cat='Binary')

model = pulp.LpProblem("Cost minimising", pulp.LpMinimize)

gen_B_index = [tpl for tpl in generators.index if tpl[1] == 'B']
gen_L_index = [tpl for tpl in generators.index if tpl[1] == 'L']
gen_G_index = [tpl for tpl in generators.index if tpl[1] == 'G']
#print(gen_B_index)
model += pulp.lpSum(
    [generatorOut[month, gen] * generators.loc[(month, gen), 'Cost'] for month, gen in generators.index]
    + [generator_status[month, gen] * generators.loc[(month, gen), 'Cost']for month, gen in generators.index]
    + [switch_on[month, gen] * generators.loc[(month, gen), 'Switchon'] for month, gen in gen_B_index]
    + [switch_on[month, gen] * generators.loc[(month, gen), 'Switchon'] for month, gen in gen_L_index]
    + [switch_on[month, gen] * generators.loc[(month, gen), 'Switchon'] for month, gen in gen_G_index]
)