import pandas as pd
import pulp

# PARAMETERS
generatorsParam = pd.read_csv('generators_variables_1.csv', sep=';', index_col=['Generators'])
demandParam = pd.read_csv('demand_variables_1.csv', sep=';', index_col=['Month'])

# print(len(generatorsParam.index));

# print(generatorsParam.loc['L','Max'])

# DECISION VARIABLES
genOutVarNames = [];
genOnOffVarNames = [];
for gen in generatorsParam.index:
    for month in demandParam.index:
        # DECISION VARIABLE: p(i,t), generator Output per generator and month
        genOutVarNames.append("p(" + gen + "," + str(month) + ")")
        # DECISION VARIABLE: x(i,t), generator on or off per generator and month
        genOnOffVarNames.append("x(" + gen + "," + str(month) + ")")

# print(genOnOffVarNames);
# print(genOutVarNames);
genOutLpVar = pulp.LpVariable.dicts("genOut",
                                    genOutVarNames,
                                    cat='Integer');

genOnOffLpVar = pulp.LpVariable.dicts("genOnOff",
                                      genOnOffVarNames,
                                      cat='Binary');

# MODEL
toSum = [];
for gen in generatorsParam.index:
    for month in demandParam.index:
        idx = 'p(' + gen + ',' + str(month) + ')'
        toSum.append(genOutLpVar[idx] * float(generatorsParam.loc[gen, 'Cost']))

model = pulp.LpProblem("Cost minimising scheduling problem", pulp.LpMinimize)
model += pulp.lpSum(toSum)

# model = pulp.LpProblem("Cost minimising scheduling problem", pulp.LpMinimize)
# model += pulp.lpSum(
#     [production[m, f] * factories.loc[(m, f), 'Variable_Costs'] for m, f in factories.index]
#     + [factory_status[m, f] * factories.loc[(m, f), 'Fixed_Costs'] for m, f in factories.index]
#     + [switch_on[m, f] * 20000 for m, f in factory_A_index]
#     + [switch_on[m, f] * 400000 for m, f in factory_B_index]
# )
