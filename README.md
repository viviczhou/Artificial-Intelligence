# Project: Automated Reasoning

In this project, I implemented three inference methods for Propositional Logic and demonstrate them on some example problems.

## Part I: Representation

Implement a propositional theorem prover. Therefore, the program will be concerned with formulas. The fomulas were represented as trees.

## Part II: Basic Model Checking

First technique: the “truth-table enumeration method” described in AIMA Figure 7.10. 

## Part III: Advanced Propositional Inference

Second technique: propositional resolution (as described in AIMA Figure 7.12). 

## Part IV: The DPLL algorithm for checking satisfiability (AIMA Figure 7.17)

## Part V: Parsers
Wrote parsers that read various textual representations of Propositional Logic sentences and create the internal representations (tree structures).
Several of these techniques require the knowledge base to be converted to clauses (conjunctive normal form, CNF). Parse knowledge bases to be in CNF.

### Template of Inputs

Taking the following problems as examples, they are all amenable to solution using Propositional Logic using both theorem proving and satisfiability testing approaches.
    Q1: Modus Ponens test. Knowledge base:
    P => Q
    P
    Query: Q
    Ans with model checking: TRUE
    Ans with resolution: TRUE

#### The four selected problems are listed below.

1. Modus Ponens: Show that {P, P ⇒ Q} 􏰀 Q.

2. Wumpus World (Simple): Consider the following facts using the Wumpus World predicates from AIMA:
¬P1,1
B1,1 ⇐⇒(P1,2∨P2,1)
B2,1 ⇐⇒ (P1,1 ∨ P2,2 ∨ P3,1) ¬B1,1
B2,1
Prove whether P1,2 is true or not (that is, whether there is a pit at location [1,2]).
The textbook gives several other examples of knowledge bases and queries using the Wumpus World that you can also try.

3. Horn Clauses (Russell & Norvig) If the unicorn is mythical, then it is immortal, but if it is not mythical, then it is a mortal mammal. If the unicorn is either immortal or a mammal, then it is horned. The unicorn is magical if it is horned.
(a) Can we prove that the unicorn is mythical? (b) Can we prove that the unicorn is magical?
(c) Can we prove that the unicorn is horned?

4. The Doors of Enlightenment (from CRUX 357): There are four doors X, Y , Z, and W leading out of the Middle Sanctum. At least one of them leads to the Inner Sanctum. If you enter a wrong door, you will be devoured by a fierce dragon. Well, there were eight priests A, B, C, D, E, F, G, and H, each of whom is either a knight or a knave. (Knights always tell the truth and knaves always lie.) They made the following statements to the philosopher:
• A: X isagooddoor.
• B: AtleastoneofthedoorsY orZ isgood.
• C: A and B are both knights.
• D: X and Y are both good doors.
• E: X and Z are both good doors.
• F: Either D or E is a knight.
• G: IfC isaknight,soisF.
• H: If G and I (meaning H) are knights, so is A.
(a) Smullyan’s problem: Which door should the philosopher choose?
(b) Liu’s problem: The philosopher lacked concentration. All he heard was the first statement (A’s) and the last statement (H’s) plus two fragments:
• C: A and ...are both knights.
• G: IfC isaknight,...
Prove that he had heard enough to make a decision.

### Extra Credit
There are two opportunities for extra credit for this project. You may do zero, either, or both. The maximum grade you can receive on this project is 120%.
• Implement a parser for WFFs. You must write a module which accepts strings as input (e.g., “P ^ Q) => R v !S)” and parses them to build (and return) a tree-structured representation of the formula. If you do this, then your program will be capable of operating using ask and tell, as discussed in class. You can receive up to 10% extra credit for a wff parser.
• Implement CNF conversino for WFFs. You must write a module which automatically converts an underlying knowledge base into conjunctive normal form. Note that you can do this either by modifying the KB, or by directly extracting a set of clauses. If you do this, then you must augment your resolution module to use your automatically constructed CNF representation (as opposed to a by-hand initialization). You can receive up to 10% extra credit for implementing automatic CNF con- version.

### Writeup
Lastly, you must produce a short PDF writeup with at least the following four sections:
1. Key Datastructures (Describe how you represented formulas, models, and clauses)
2. Performance (Include your programs answers to the four questions. Include results for model checking and resolution).
3. Member contributions (describe each team member’s contributions to the project)

Submission Instructions
Upload a ZIP archive with everything (source code and writeup) to Black- Board before the deadline.
Place all your source code into a directory called src. You must also include a plain-text README file in your src directory which describes how to build and run your program, and includes the names and UR NetID’s for each contributing team member. Zip your src directory, README, and PDF writup into a single file and upload to blackboard.
Submissions received by 11:59PM Sunday, October 27th will receive a flat 5% bonus credit. Submissions will be accepted until 11:59PM, Wednesday, October 30th.
