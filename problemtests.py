'''
Project #2 Automated Reasoning
Version 2.0 created at 2019/10/24
    Test theorem prover by applying the following four problems.
'''

from algorithms import *

def test(information, query):
    kb = KB()
    print('Knowledge base:')
    for i in information:
        kb.tell(i)
        print(i)
    print('Query:')
    for i in query:
        print(i)
        alpha = expr(i)
        mc_q = kb.model_checking(alpha)
        mc_notq = kb.model_checking(~alpha)
        if mc_q == mc_notq:
            print('Ans with model checking: Maybe')
        if mc_q != mc_notq:
            print('Ans with model checking:', str(mc_q))
        plr_q = PL_Resolution(kb, alpha)
        plr_notq = PL_Resolution(kb, ~alpha)
        if plr_q == plr_notq:
            print('Ans with resolution: Maybe')
        if plr_q != plr_notq:
            print('Ans with resolution:', str(plr_q))
        dpll = DPLL_Satisfiable(alpha)
        print('Ans with dpll satisfiable: ' + str(dpll))

if __name__ == "__main__":
    print('Modus Ponens test.')
    mp_information = ['P', 'P ==> Q']
    mp_alpha = ['Q']
    test(mp_information, mp_alpha)
    print('\nWumpus World test.')
    ww_information = ['~P11', 'B11 <=> (P12 | P21)', 'B21 <=> (P11 | P22 | P31)', '~B11', 'B21']
    ww_alpha = ['P12']
    test(ww_information, ww_alpha)
    print('\nHorned Clauses test.')
    hc_information = ['Mythical ==> Immortal', '~Mythical ==> Mammal', '(Immortal | Mammal) ==> Horned', 'Horned ==> Magical']
    hc_alpha = ['Mythical', 'Magical', 'Horned']
    test(hc_information, hc_alpha)
    print('\nThe Door of Enlightenment test. Smullyan’s problem:')
    de_alpha = ['X', 'Y', 'Z', 'W']
    de_information_a = ['A <=> X', 'B <=> (Y | Z)', 'C <=> (A & B)', 'D <=> (X & Y)', 'E <=> (X & Z)',
                      'F <=> (D | E)', 'G <=> (C ==> F)', 'H <=> ((G & H) ==> A)', 'X | Y | Z | W']
    test(de_information_a, de_alpha)
    print('\nThe Door of Enlightenment test. Liu’s problem:')
    de_information_b = ['A <=> X', 'C <=> A', 'G <=> (C ==> (A | ~A))', 'H <=> ((G & H) ==> A)', 'X | Y | Z | W']
    test(de_information_b, de_alpha)
