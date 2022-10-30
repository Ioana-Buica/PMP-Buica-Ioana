from pgmpy.models import BayesianNetwork
from pgmpy.inference import VariableElimination

game_model = BayesianNetwork(
    [
        ("PlayerA_card1", "PlayerB_card1"), # ambi au o carte

        ("PlayerA_card1", "PlayerA_card2"),
        ("PlayerB_card1", "PlayerA_card2"),

        ("PlayerA_card1", "PlayerB_card2"),
        ("PlayerB_card1", "PlayerB_card2"),
        ("PlayerA_card2", "PlayerB_card2"),

        ("PlayerA_card1","PlayerA_move"),
        ("PlayerA_card2","PlayerA_move"),

        ("PlayerA_move" ,"PlayerB_move"),
        ("PlayerB_card1","PlayerB_move"),
        ("PlayerB_card2","PlayerB_move"),

        ("PlayerB_move","PlayerA_move2"),
        ("PlayerA_card1","PlayerA_move2"),
        ("PlayerA_card2","PlayerA_move2")
    ]
)

# Defining the parameters using CPT
from pgmpy.factors.discrete import TabularCPD

cpd_playerA_card1 = TabularCPD(                     #    A_f    K_f    Q_f    K_i    Q_i
    variable="PlayerA_card1", variable_card=5, values=[[0.2], [0.2], [0.2], [0.2], [0.2]]
       # player 1 are 5 carti din care sa aleaga (1/5 = 0.20)
)   
cpd_playerB_card1 = TabularCPD(                    
    variable="PlayerB_card1", variable_card=5, 
        #    A_f  K_f   Q_f   K_i   Q_i
    values=[[0,   0.25, 0.25, 0.25, 0.25],  # A_f
            [0.25,0   , 0.25, 0.25, 0.25],  # K_f
            [0.25,0.25, 0   , 0.25, 0.25],  # Q_f
            [0.25,0.25, 0.25, 0   , 0.25],  # K_i
            [0.25,0.25, 0.25, 0.25, 0   ]], # Q_i
        # avem 0 pe diagonala deoarece nu pot amandoi players sa aiba aceasi carte
        # player 2 are 4 carti din care sa aleaga (1/4 = 0.25)
    evidence=["PlayerA_card1"], evidence_card=[5],
)   
cpd_playerA_card2 = TabularCPD(                     #    A_f    K_f    Q_f    K_i    Q_i
    variable="PlayerA_card2", variable_card=5, 
           #          A_f            |           K_f           |           Q_f           |           K_i           |           Q_i
           # A_f  K_f  Q_f  K_i  Q_i | A_f  K_f  Q_f  K_i  Q_i | A_f  K_f  Q_f  K_i  Q_i | A_f  K_f  Q_f  K_i  Q_i | A_f  K_f  Q_f  K_i  Q_i
    values=[[0,   0,   0,   0,   0,    0,   0.25,0.30,0.30,0.30, 0,   0.30,0.25,0.30,0.30, 0,   0.30,0.30,0.25,0.30, 0.30,0.30, 0.30,0.30,0.25], 
            [0.25,0,   0.30,0.30,0.30, 0,   0,   0   ,0   ,0  ,  0.30,0   ,0.25,0.35,0.35, 0.30,0,   0.35,0.25,0.35, 0.35,0,   0.35,0.35,0.25], 
            [0.25,0.30,0,   0.35,0.35,  0.30,0.25,0   ,0.35,0.35, 0,   0   ,0   ,0   ,0  ,  0.35,0.35,0,   0.25,0.35, 0.35,0.35,0,   0.35,0.25], 
            [0.25,0.35,0.35,0,   0.35, 0.35,0.25,0.35,0   ,0.35, 0.35,0.35,0.25,0   ,0.35, 0,   0,   0,   0,   0,    0,   0.35,0.35,0,   0.25], 
            [0.25,0.35,0.35,0.35,0,    0.35,0.25,0.35,0.35,0  ,  0.35,0.35,0.25,0.35,0  ,  0.35,0.35,0.35,0.25,0,    0,   0,   0,   0,   0]],
    evidence=["PlayerA_card1","PlayerB_card1"], evidence_card=[5, 5],
)   
cpd_playerB_card2 = TabularCPD(                    
    variable="PlayerB_card2", variable_card=5, 
        #                  1             |              2               |                3            |             4               |              5          |          1              |            2           |           3            |            4           |            5           |            1           |            2           |             3          |             4          |            5           |            1           |             2          |             3          |           4            |            5           |             1          |             2          |             3          |             4          |          5                                                                                                                                                                                                                                                                                                                             
    values=[[0,   0   , 0   , 0   , 0    , 0,    0   , 0   , 0   , 0    , 0,    0   , 0   , 0   , 0   , 0,    0   , 0   , 0   , 0   , 0,   0  , 0  ,0    ,0   , 0   ,0   ,0   ,0   ,0   ,0   ,0.3 ,0.3 ,0.3 ,0.3 ,0   ,0.3 ,0.3 ,0.5 ,0.5 ,0   ,0.3 ,0.5 ,0.3 ,0.5 ,0   ,0.3 ,0.5 ,0.5 ,0.3 ,0   ,0   ,0   ,0   ,0   ,0   ,0.3 ,0.3 ,0.5 ,0.5 ,0   ,0.3 ,0.25,0.3 ,0.3 ,0   ,0.5 ,0.3 ,0.3 ,0.5 ,0   ,0.5 ,0.3 ,0.5 ,0.3 ,0   ,0   ,0   ,0   ,0   ,0   ,0.3 ,0.5 ,0.3 ,0.5 ,0   ,0.5 ,0.3 ,0.3 ,0.5 ,0   ,0.3 ,0.3 ,0.25,0.3 ,0   ,0.5 ,0.5 ,0.3 ,0.3 ,0   ,0   ,0   ,0   ,0   ,0   ,0.3 ,0.5 ,0.5 ,0.3 ,0   ,0.5 ,0.3 ,0.5 ,0.3 ,0   ,0.5 ,0.5 ,0.3 ,0.3 ,0   ,0.3 ,0.3 ,0.3 ,0.25],  
            [0.25,0   , 0.3 , 0.3 , 0.3  , 0,    0   , 0   , 0   , 0    , 0.3 , 0   , 0.3 , 0.5 , 0.5 , 0.3 , 0   , 0.5 , 0.3 , 0.5 , 0.3 ,0,   0.5 ,0.5 ,0.3 , 0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0.3 ,0   ,0.3 ,0.5 ,0.5 ,0   ,0   ,0   ,0   ,0   ,0.3 ,0   ,0.25,0.35,0.35,0.5 ,0   ,0.35,0.35,0.5 ,0.5 ,0   ,0.35,0.5 ,0.35,0.3 ,0   ,0.5 ,0.3 ,0.5 ,0   ,0   ,0   ,0   ,0   ,0.5 ,0   ,0.35,0.35,0.5 ,0.3 ,0   ,0.35,0.25,0.35,0.5 ,0   ,0.5 ,0.35,0.35,0.3 ,0   ,0.5 ,0.5 ,0.3 ,0   ,0   ,0   ,0   ,0   ,0.5 ,0   ,0.35,0.5 ,0.35,0.5 ,0   ,0.5 ,0.35,0.35,0.3 ,0   ,0.35,0.35,0.25], 
            [0.25,0.3 , 0   , 0.35, 0.35 , 0.3 , 0.3 , 0   , 0.5 , 0.5  , 0,    0   , 0   , 0   , 0   , 0.35, 0.5 , 0   , 0.35, 0.5 , 0.35,0.5 ,0   ,0.5 ,0.35, 0.3 ,0.3 ,0   ,0.5 ,0.5 ,0.3 ,0   ,0.35,0.35,0.35,0   ,0   ,0   ,0   ,0   ,0.5 ,0.35,0   ,0.35,0.5 ,0.5 ,0.35,0   ,0.5 ,0.35,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0.35,0.5 ,0   ,0.35,0.5 ,0.5 ,0.35,0   ,0.35,0.5 ,0   ,0   ,0   ,0   ,0   ,0.35,0.35,0   ,0.25,0.35,0.5 ,0.5 ,0   ,0.35,0.35,0.35,0.5 ,0   ,0.5 ,0.35,0.5 ,0.35,0   ,0.5 ,0.35,0   ,0   ,0   ,0   ,0   ,0.5 ,0.5 ,0   ,0.35,0.35,0.35,0.35,0   ,0.35,0.25],  
            [0.25,0.35, 0.35, 0   , 0.35 , 0.35, 0.35, 0.5 , 0   , 0.5  , 0.35, 0.5 , 0.35, 0   , 0.5 , 0,    0   , 0   , 0   , 0,    0.35,0.5 ,0.5 ,0,   0.35, 0.35,0.35,0.5 ,0   ,0.5 ,0.35,0.35,0   ,0.35,0.35,0.5 ,0.35,0.35,0   ,0.5 ,0   ,0   ,0   ,0   ,0   ,0.5 ,0.35,0.5 ,0   ,0.35,0.35,0.5 ,0.35,0   ,0.5 ,0.5 ,0.35,0.35,0   ,0.5 ,0.35,0.35,0.25,0   ,0.35,0   ,0   ,0   ,0   ,0   ,0.5 ,0.5 ,0.35,0   ,0.35,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0.35,0.5 ,0.5 ,0   ,0.35,0.5 ,0.35,0.5 ,0   ,0.35,0.5 ,0.5 ,0.35,0   ,0.35,0   ,0   ,0   ,0   ,0   ,0.35,0.35,0.35,0   ,0.25],  
            [0.25,0.35, 0.35, 0.35, 0    , 0.35, 0.35, 0.5 , 0.5, 0     , 0.35, 0.5 , 0.35, 0.5 , 0   , 0.35, 0.5 , 0.5 , 0.35, 0,    0,   0 ,  0 ,  0,   0   , 0.35,0.35,0.5 ,0.5 ,0   ,0.35,0.35,0.35,0   ,0   ,0.5 ,0.35,0.35,0.5 ,0   ,0.5 ,0.35,0.5 ,0.35,0.  ,0   ,0   ,0   ,0   ,0   ,0.35,0.5 ,0.35,0.5 ,0   ,0.5 ,0.35,0.35,0.5 ,0   ,0.35,0.35,0.25,0.35,0   ,0.5 ,0.5 ,0.35,0.35,0   ,0   ,0   ,0   ,0   ,0   ,0.35,0.5 ,0.5 ,0.35,0   ,0.5 ,0.35,0.5 ,0.35,0   ,0.5 ,0.5 ,0.35,0.35,0   ,0.35,0.35,0.35,0.25,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ]], 
        # avem 0 pe diagonala deoarece nu pot amandoi players sa aiba aceasi carte
        # player 2 are 4 carti din care sa aleaga (1/4 = 0.25)
    evidence=["PlayerA_card1","PlayerB_card1","PlayerA_card2"], evidence_card=[5, 5, 5],
)   

cpd_playerA_move = TabularCPD(                     #    A_f    K_f    Q_f    K_i    Q_i
    variable="PlayerA_move", variable_card=2, 
    #                              |                       |                       |                       |                                   
    values=[[0, 0, 0.25, 0.50, 0.75, 0, 0, 0.25, 0.50, 0.75, 0, 0.25, 0.50, 0.75, 1, 0.25, 0.50, 0.75, 1, 1, 0.25, 0.50, 0.75, 1, 1],       # 0 -> don't BET
            [1, 1, 0.75, 0.50, 0.25, 1, 1, 0.75, 0.50, 0.25, 1, 0.75, 0.50, 0.25, 0, 0.75, 0.50, 0.25, 0, 0, 0.75, 0.50, 0.25, 0, 0]],      # 1 -> BET
       # player 1 are 2 miscari (BET si NO BET )
       # pariaza in functie de cate carti are mai mari (1 - x/4)
       # are o carte in mana deci au ramas 4 carti in joc
    evidence=["PlayerA_card1","PlayerA_card2"], evidence_card=[5, 5],
)   
cpd_playerB_move = TabularCPD(                    
    variable="PlayerB_move", variable_card=2, 
    # ce miscare a ales player 1:   0 | 1
    #        A_f  K_f  Q_f  K_i   Q_i | A_f  K_f   Q_f   K_i  Q_i
    #                                                                                                                              |
    values=[[0, 0, 0.25, 0.50, 0.75, 0, 0, 0.25, 0.50, 0.75, 0, 0.25, 0.50, 0.75, 1, 0.25, 0.50, 0.75, 1, 1, 0.25, 0.50, 0.75, 1, 1,0, 0, 0.25, 0.50, 0.75, 0, 0, 0.25, 0.50, 0.75, 0, 0.25, 0.50, 0.75, 1, 0.25, 0.50, 0.75, 1, 1, 0.25, 0.50, 0.75, 1, 1],       # 0 -> don't BET
            [1, 1, 0.75, 0.50, 0.25, 1, 1, 0.75, 0.50, 0.25, 1, 0.75, 0.50, 0.25, 0, 0.75, 0.50, 0.25, 0, 0, 0.75, 0.50, 0.25, 0, 0,1, 1, 0.75, 0.50, 0.25, 1, 1, 0.75, 0.50, 0.25, 1, 0.75, 0.50, 0.25, 0, 0.75, 0.50, 0.25, 0, 0, 0.75, 0.50, 0.25, 0, 0]],      # 1 -> BET
       
       # player 2 are 2 miscari (BET[1] si NO BET )
       # daca player 1 a pariat
       # pariaza in functie de cate carti are mai mari (1 - x/4) - 0,25(daca player 1 a pariat)
       # daca player 1 a ales sa nu parieze pariem pt. orice carete
       # fara ultimele 2
       # are o carte in mana deci au ramas 4 carti in joc
       evidence=["PlayerA_move","PlayerB_card1","PlayerB_card2"], evidence_card=[2, 5, 5],
)   
cpd_playerA_move2 = TabularCPD(                     #    A_f    K_f    Q_f    K_i    Q_i
    variable="PlayerA_move2", variable_card=2, 
    # ce miscare a ales player 1:   0 | 1
    #        A_f  K_f  Q_f  K_i   Q_i | A_f  K_f   Q_f   K_i  Q_i
    values=[[0, 0, 0.25, 0.50, 0.75, 0, 0, 0.25, 0.50, 0.75, 0, 0.25, 0.50, 0.75, 1, 0.25, 0.50, 0.75, 1, 1, 0.25, 0.50, 0.75, 1, 1,0, 0, 0.25, 0.50, 0.75, 0, 0, 0.25, 0.50, 0.75, 0, 0.25, 0.50, 0.75, 1, 0.25, 0.50, 0.75, 1, 1, 0.25, 0.50, 0.75, 1, 1],       # 0 -> don't BET
            [1, 1, 0.75, 0.50, 0.25, 1, 1, 0.75, 0.50, 0.25, 1, 0.75, 0.50, 0.25, 0, 0.75, 0.50, 0.25, 0, 0, 0.75, 0.50, 0.25, 0, 0,1, 1, 0.75, 0.50, 0.25, 1, 1, 0.75, 0.50, 0.25, 1, 0.75, 0.50, 0.25, 0, 0.75, 0.50, 0.25, 0, 0, 0.75, 0.50, 0.25, 0, 0]],      # 1 -> BET
       
    evidence=["PlayerB_move","PlayerA_card1","PlayerA_card2"], evidence_card=[2, 5, 5],
) 

game_model.add_cpds(
    cpd_playerA_card1, cpd_playerB_card1, cpd_playerA_card2, cpd_playerB_card2, cpd_playerA_move, cpd_playerB_move, cpd_playerA_move2
)
print()
print(game_model.check_model())
print(game_model.nodes())
print(game_model.edges())
print()