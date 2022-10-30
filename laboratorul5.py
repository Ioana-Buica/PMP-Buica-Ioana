from pgmpy.models import BayesianNetwork
from pgmpy.inference import VariableElimination

game_model = BayesianNetwork(
    [
        ("PlayerA", "PlayerB"), # ambi au o carte

        ("PlayerA","PlayerA_move"),

        ("PlayerA_move","PlayerB_move"),
        ("PlayerB","PlayerB_move"),

        ("PlayerB_move","PlayerA_move2"),
        ("PlayerA","PlayerA_move2"),

        ("PlayerA","Cartea_mai_mare"),
        ("PlayerB","Cartea_mai_mare"),

        ("PlayerA_move","Rezultat"),
        ("PlayerB_move","Rezultat"),
        ("PlayerA_move2","Rezultat"),
        ("Cartea_mai_mare","Rezultat")
    ]
)

# Defining the parameters using CPT
from pgmpy.factors.discrete import TabularCPD

cpd_playerA = TabularCPD(                     #    A_f    K_f    Q_f    K_i    Q_i
    variable="PlayerA", variable_card=5, values=[[0.2], [0.2], [0.2], [0.2], [0.2]]
       # player 1 are 5 carti din care sa aleaga (1/5 = 0.20)
)   
cpd_playerB = TabularCPD(                    
    variable="PlayerB", variable_card=5, 
        #    A_f  K_f   Q_f   K_i   Q_i
    values=[[0,   0.25, 0.25, 0.25, 0.25],  # A_f
            [0.25,0   , 0.25, 0.25, 0.25],  # K_f
            [0.25,0.25, 0   , 0.25, 0.25],  # Q_f
            [0.25,0.25, 0.25, 0   , 0.25],  # K_i
            [0.25,0.25, 0.25, 0.25, 0   ]], # Q_i
        # avem 0 pe diagonala deoarece nu pot amandoi players sa aiba aceasi carte
        # player 2 are 4 carti din care sa aleaga (1/4 = 0.25)
    evidence=["PlayerA"], evidence_card=[5],
)   
cpd_playerA_move = TabularCPD(                     #    A_f    K_f    Q_f    K_i    Q_i
    variable="PlayerA_move", variable_card=2, 
    #        A_f K_f   Q_f  K_i   Q_i
    values=[[0,  0.25, 0.5, 0.75, 1],       # 0 -> don't BET
            [1,  0.75, 0.5, 0.25, 0]],      # 1 -> BET
       # player 1 are 2 miscari (BET si NO BET )
       # pariaza in functie de cate carti are mai mari (1 - x/4)
       # are o carte in mana deci au ramas 4 carti in joc
    evidence=["PlayerA"], evidence_card=[5],
)   
cpd_playerB_move = TabularCPD(                    
    variable="PlayerB_move", variable_card=2, 
    # ce miscare a ales player 1:   0 | 1
    #        A_f  K_f  Q_f  K_i   Q_i | A_f  K_f   Q_f   K_i  Q_i
    values=[[0,   0  , 0  , 1  ,  1,    0,   0.5,  0.25, 1,   1],   # 0 -> don't BET
            [1,   1  , 1  , 0  ,  0,    1,   0.5,  0.75, 0,   0]],  # 1 -> BET
       # player 2 are 2 miscari (BET[1] si NO BET )
       # daca player 1 a pariat
       # pariaza in functie de cate carti are mai mari (1 - x/4) - 0,25(daca player 1 a pariat)
       # daca player 1 a ales sa nu parieze pariem pt. orice carete
       # fara ultimele 2
       # are o carte in mana deci au ramas 4 carti in joc
       evidence=["PlayerA_move","PlayerB"], evidence_card=[2, 5],
)   
"""
# pentru ex.2 c)
cpd_playerA_move = TabularCPD(                     #    A_f    K_f    Q_f    K_i    Q_i
    variable="PlayerA_move", variable_card=2, 
    #        A_f K_f   Q_f  K_i   Q_i
    values=[[0,  1,    1,   1,    1],       # 0 -> don't BET
            [1,  0,    0,   0,    0]],      # 1 -> BET
       # player 1 are 2 miscari (BET si NO BET )
       # pariaza in functie de cate carti are mai mari (1 - x/4)
       # are o carte in mana deci au ramas 4 carti in joc
    evidence=["PlayerA"], evidence_card=[5],
)   
cpd_playerB_move = TabularCPD(                    
    variable="PlayerB_move", variable_card=2, 
    # ce miscare a ales player 1:   0 | 1
    #        A_f  K_f  Q_f  K_i   Q_i | A_f  K_f   Q_f   K_i  Q_i
    values=[[0,   0  , 0  , 0  ,  0,    0,   0,    0,    0,   0],   # 0 -> don't BET
            [1,   1  , 1  , 1  ,  1,    1,   1,    1,    1,   1]],  # 1 -> BET
       # player 2 are 2 miscari (BET[1] si NO BET )
       # daca player 1 a pariat
       # pariaza in functie de cate carti are mai mari (1 - x/4) - 0,25(daca player 1 a pariat)
       # daca player 1 a ales sa nu parieze pariem pt. orice carete
       # fara ultimele 2
       # are o carte in mana deci au ramas 4 carti in joc
       evidence=["PlayerA_move","PlayerB"], evidence_card=[2, 5],
)
"""   
cpd_playerA_move2 = TabularCPD(                     #    A_f    K_f    Q_f    K_i    Q_i
    variable="PlayerA_move2", variable_card=2, 
    # ce miscare a ales player 1:   0 | 1
    #        A_f  K_f  Q_f  K_i   Q_i | A_f  K_f   Q_f   K_i  Q_i
    values=[[0,   0  , 0  , 0  ,  0,    0,   0.5,  0.25, 1,   1],
            [1,   1  , 1  , 1  ,  1,    1,   0.5,  0.75, 0,   0]],
    
    evidence=["PlayerB_move","PlayerA"], evidence_card=[2, 5],
)   
cpd_cartea_mai_mare = TabularCPD(        
    variable="Cartea_mai_mare", variable_card=2, 
    values=[[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],   # a pierdut 
            [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1]],  # a castigat
    evidence=["PlayerA","PlayerB"], evidence_card=[5, 5],
) 
cpd_rezultat= TabularCPD(                 
    variable="Rezultat", variable_card=2, 
    values=[[0, 0, 0, 0, 1, 1, -2, -2, -1, -1, -1, -1, -2, -2, -2, -2],   # in functie de jucatorul 1
            [1, 1, 1, 1, 0, 0,  3,  3,  2,  2,  2,  2,  3,  3,  3,  3]],  
    evidence=["PlayerA_move","PlayerB_move","PlayerA_move2","Cartea_mai_mare"], evidence_card=[2, 2, 2, 2],
) 

game_model.add_cpds(
    cpd_playerA, cpd_playerB, cpd_playerA_move, cpd_playerB_move, cpd_playerA_move2, cpd_cartea_mai_mare, cpd_rezultat
)
print()
print(game_model.check_model())
print(game_model.nodes())
print(game_model.edges())
print()
print("Esti Jucatorul 1 si ai primit un Rege de Frunza, ar trebui sa pariezi sau nu?")
infer = VariableElimination(game_model)
# calculam in cazul cand primul player are K_frunza
posterior_p = infer.query(["PlayerA_move"], evidence={"PlayerA": 1})
print(posterior_p)
if posterior_p.values[0] > posterior_p.values[1]:
    print("Nu va paria")
else:
    print("Va paria")

print()
print("Esti Jucatorul 2 si ai primit un Rege de Inima iar Jucatorul 1 a decis sa parieze. Cum ar trebui sa decizi?")
infer = VariableElimination(game_model)
# calculam in cazul cand primul player are K_inima
# si cand Player 1 a pariat
posterior_p = infer.query(["PlayerB_move"], evidence={"PlayerA_move": 1, "PlayerB": 3})
print(posterior_p)
if posterior_p.values[0] > posterior_p.values[1]:
    print("Nu va paria")
else:
    print("Va paria")


#print(game_model.get_cpds())
#print(game_model.get_independencies())