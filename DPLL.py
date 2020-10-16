# Run the DPLL algorithm on george formulas

# use to select random literal
import random
# used to access And, Or, Imp, etc. classes and all the helper functions
from george.frml import *

# you are encouraged to decompose your solution into multiple functions

import random

# Boolean Valuation class
# you may add more methods to this class
class BooleanValuation:

    def __init__(self):
        # dictionary attributes that maps strings to T/F (strings)
        self.__assignment = {}

    # returns the assignment dictionary
    def get_bv(self):
        return self.__assignment

    # creates a new BV like the argument but a copy of it
    def copy_bv(self):
        bv1 = BooleanValuation()
        bv1.__assignment = self.__assignment.copy()
        return bv1

    # these assume that they will be passed a Prop or Not !!
    # assigns 'T' to literal
    def assignLiteralTrue(self, literal):
        if isProp(literal):
            x = literal.get_name()
            self.__assignment[x] = 'T'
        elif isNot(literal):
            x = literal.get_arg().get_name()
            self.__assignment[x] = 'F'

    # assigns 'F' to literal
    def assignLiteralFalse(self, literal):
        if isProp(literal):
            x = literal.get_name()
            self.__assignment[x] = 'F'
        elif isNot(literal):
            x = literal.get_arg().get_name()
            self.__assignment[x] = 'T'

    # remove literal from Boolean Valuation
    def remove(self, literal):
        if isProp(literal):
            x = literal.get_name()
        elif isNot(literal):
            x = literal.get_arg().get_name()
        del self.__assignment[x]

    # returns a string containing all truth assignments sorted alphabetically by proposition
    def __str__(self):
        tmpStr= ""
        keys = list(self.__assignment.keys())
        keys.sort()
        for key in keys:
            tmpStr += "[{0}] = {1}\n".format(key, self.__assignment[key])
        return tmpStr

# Input: a george formula
# Output: True if the formula contains an illegal literal
def CNFCheckFormula(formula):
    # Return false if it is and, iff, imp or a not with multiple ! symbols
    return isAnd(formula) or isIff(formula) or isImp(formula) or (isNot(formula) and not isProp(formula.get_l()))

# Input: a george formula
# Output: True if the formula is in CNF and False otherwise
def CNFCheck(formula):
#     #TODO: Implement CNFCheck function

    # List representing clauses
    clauses = []

    # Return true if it's just a prop or not
    if isProp(formula) or (isNot(formula) and isProp(formula.get_l())):
        if isNot(formula) and formula.get_l().get_name() in ["True", "False"]:
            return False
        return True
    # If formula is an or, check that there are no contradictory or illegal literals
    elif isOr(formula):
        for literal in formula.get_args():
            if CNFCheckFormula(literal) or unitNegate(literal) in formula.get_args():
                return False
        return True
    # If formula is an and
    elif isAnd(formula):
        # Iterate through its clauses
        for clause in formula.get_args():
            
            # Make sure there are no illegal clauses
            if CNFCheckFormula(clause):
                return False
            
            # Initialize list contianing literals
            literals = []

            # If encountered an or clauses, loop through its literals
            if isOr(clause):
                for literal in clause.get_args():
                    # Ensure there are no illegal literals
                    if CNFCheckFormula(clause):
                        return False

                    # If encounter a prop, make sure it is not True or False and its negation isn't in the clause
                    if isProp(literal) and unitNegate(literal) not in literals and literal.get_name() not in ["True", "False"]:
                        literals.append(literal.get_name())
                    # If encounter a not, make sure it is not True or False and its negation isn't in the clause
                    elif isNot(literal) and unitNegate(literal) not in literals and literal.get_l().get_name() not in ["True", "False"]:
                        literals.append("!" + literal.get_l().get_name())
                    else:
                        return False
            # For the cases of a prop or not clause
            else:
                # If encounter a prop, make sure it is not True or False and its negation isn't in the formula
                if isProp(clause) and clause.get_name() not in ["True", "False"]:
                    literals.append(clause.get_name())
                # If encounter a not, make sure it is not True or False and its negation isn't in the formula
                elif isNot(clause):
                    literals.append("!" + clause.get_l().get_name())
                else:
                    return False

            # Sort the list of literals
            literals.sort()
            
            # Return false if duplicate encountered
            if literals and literals in clauses:
                return False

            clauses.append(literals)
    else:
        return False
    
    return True

# Input: george formula, bool to return only list of literals (not pures)
# Output: list of literals or pures
def grabPures(formula, forDPLL=False):
    pures = []
    
    # If formula is just a prop or not
    if isProp(formula) or isNot(formula):
        return [formula]

    # Iterate through clauses and literals of formula, and put all literals in pures list
    for clause in formula.get_args():
        if isOr(clause):
            for literal in clause.get_args():
                pures.append(literal)
        else:
            pures.append(clause)
    
    # Initialize a copy of pures in returnList
    returnList = pures

    # If pures are needed, iterate through an remove any that doesn't have its negation there
    if not forDPLL:
        returnList = []
        for pure in pures:
            if unitNegate(pure) not in pures:
                returnList.append(pure)

    # Initialize an empty list to be propagated and returned
    finalList = []

    # Remove duplicated before returning
    for element in returnList:
        if element not in finalList:
            finalList.append(element)

    return finalList

# Input: george formula
# Output: list of units in the formula
def grabUnits(formula):
    units = []

    # Add any prop or not clauses to the list
    if isProp(formula) or isNot(formula):
        units.append(formula)
    # In an and formula, parse through its clauses and add any props or nots
    elif isAnd(formula):
        for clause in formula.get_args():
            if isProp(clause) or isNot(clause):
                units.append(clause)
    
    return units

# Input: george formula, either a proposition or not
# Output: Negated formula
def unitNegate(formula):
    if isProp(formula):
        return Not(formula)
    else:
        return Prop(formula.get_l().get_name())

def printLiterals(literals):
    return [i.get_name() for i in literals if isProp(i)] + ["!" + i.get_l().get_name() for i in literals if isNot(i)]

# Input: george formula, Boolean valuation and list of units (not required)
# Output: george formula after being applied unit propagation and its corresponding BV
def unitPropagate(formula, BV, units=None):
    # If units not provided, run grabUnits with current formula
    if not units:
        units = grabUnits(formula)

    # Getting BV dictionary
    bvDict = BV.get_bv()

    # Temp is formula to be worked on 
    temp = formula
    nextUnits = units
    returnBV = BV

    # Apply unit propagation as long as units remain
    while nextUnits and not isEmptyFormula(formula) and formula:
        # If prop or not encountered and they're not already in provided BV, add them in
        if isProp(formula) or isNot(formula):
            if isProp(formula) and formula.get_name() not in bvDict:
                returnBV.assignLiteralTrue(Prop(formula.get_name()))
            elif isNot(formula) and formula.get_l().get_name() not in bvDict:
                returnBV.assignLiteralFalse(Prop(formula.get_l().get_name()))

            # Return empty formula with updated BV
            return EmptyFormula(), returnBV

        # Iterate through clauses of formula
        for clause in formula.get_args():
            # removedClause represents a clause that has any negation of units removed from it
            removedClause = clause

            # Looping through units
            for unit in nextUnits:
                # Initializing the negated unit
                # print("Will negate ", unit, " in ", nextUnits)
                negUnit = unitNegate(unit)

                # If prop or not encountered and they're not already in provided BV, add them in
                if isProp(unit) and unit.get_name() not in bvDict:
                    returnBV.assignLiteralTrue(Prop(unit.get_name()))
                elif isNot(unit) and unit.get_l().get_name() not in bvDict:
                    returnBV.assignLiteralFalse(Prop(unit.get_l().get_name()))

                # If contradictory literals detected, return false with original BV
                if negUnit in nextUnits and not isOr(formula):
                    return False, BV

                # If clause is an or and contains a unit
                if (isOr(clause) and unit in clause.get_args()) or clause.__eq__(unit):
                    if temp.__eq__(clause):
                        # Return empty formula if clause is equal to unit
                        return EmptyFormula(), returnBV
                    # Remove the clause
                    temp = temp.remove(clause)
                    break
                # If clause is an or and negated unit is in it
                elif isOr(clause) and negUnit in clause.get_args():
                    # If clause is already a prop or not, return false since it will result in an empty clause
                    if isNot(removedClause) or isProp(removedClause):
                        # return removedClause
                        return False, BV
                    
                    # Remove the negated unit
                    removedClause = removedClause.remove(negUnit)
                    # print(removedClause)

            # If removals were made, update clause in formula with new clause
            if not removedClause.__eq__(clause):
                if isOr(temp):
                    temp = removedClause
                else:
                    temp = temp.replace(clause, removedClause)
        # Find units for formula again, if any
        nextUnits = grabUnits(temp)
        formula = temp

    # Return updated formula and BV
    return temp, returnBV

# Input: george formula, Boolean valuation and list of pures (not required)
# Output: george formula after being applied pure elimination and corresponding BV
def pureEliminate(formula, BV, pures=None):
    # Puting BV dictionary in bvDict
    bvDict = BV.get_bv()

    # Current formula is formula to be iterated over
    curForm = formula
    # Next formula is formula that is actively being manipulated
    nextForm = formula
    # To be returned BV
    returnBV = BV

    # If no list of pures provided, call grabPures on current formula
    if not pures:
        pures = grabPures(formula)

    # Equate curPures to pures since parameters shouldn't be changed
    curPures = pures
    
    # If formula is or, as long as any literals in it aren't contradictory return an Empty formula with updated BV
    if isOr(formula):
        for clause in formula.get_args():
            # Return false with original BV if contradictory literal found
            if unitNegate(clause) in formula.get_args():
                return False, BV
            # Fill in True for props
            elif isProp(clause) and clause.get_name() not in bvDict:
                returnBV.assignLiteralTrue(Prop(clause.get_name()))
            # Fill in False for nots
            elif isNot(clause) and clause.get_l().get_name() not in bvDict:
                returnBV.assignLiteralFalse(Prop(clause.get_l().get_name()))

        # Return empty formula and updated BV
        return EmptyFormula(), returnBV

    # To apply pure elimination as long as possible, continue applying as long as pures exist
    while curPures and not isEmptyFormula(curForm):
        for clause in curForm.get_args():
            for pure in curPures:
                # Assigning BV to props or nots
                if isProp(pure) and pure.get_name() not in bvDict:
                    returnBV.assignLiteralTrue(Prop(pure.get_name()))
                elif isNot(pure) and pure.get_l().get_name() not in bvDict:
                    returnBV.assignLiteralFalse(Prop(pure.get_l().get_name()))

                # If only proposition or not remain, return empty formula
                if nextForm.__eq__(pure):
                    return EmptyFormula(), returnBV
                # If the clause is an or and it contains a pure, remove it
                elif (isOr(clause) and pure in clause.get_args()) or clause.__eq__(pure):
                    nextForm = nextForm.remove(clause)
                    break
        
        # See if formula has any more pures
        curPures = grabPures(nextForm)
        curForm = nextForm

        # If formula is just a prop or not, return empty formula with matching BV
        if isNot(curForm) or isProp(curForm):
            return EmptyFormula(), returnBV

    # Return worked on formula and BV
    return curForm, returnBV

# Input: BV and a george formula
# Output: BV with all its Don't Care literals filled
def fillBV(BV, formula):
    # Return BV is copy of parameter, since parameters shouldn't be modified
    returnBV = BV.copy_bv()
    # Call grab pures to grab all literals in gormula
    literals = grabPures(formula, True)
    # Put dictionary of BV in bvDict
    bvDict = BV.get_bv()

    # Iterate through all literals
    for literal in literals:
        # Add True for prop Don't Cares, which won't be found in BV dictionary
        if isProp(literal) and literal.get_name() not in bvDict:
            returnBV.assignLiteralTrue(Prop(literal.get_name()))
        # Add False for not Don't Cares, which won't be found in BV dictionary either
        elif isNot(literal) and literal.get_l().get_name() not in bvDict:
            returnBV.assignLiteralFalse(Prop(literal.get_l().get_name()))

    # Return BV
    return returnBV

# Input: a george formula
# Output: a pair ("SAT"/"UNSAT"/"NOTINCNF", BV) 
# BV is a boolean valuation that is printed when the formula is SAT
def DPLL(formula):
    # TODO: Implement DPLL function
    # Remember to use your CheckCNF() function first

    # Boolean valuation to be returned
    BV = BooleanValuation()

    # Check validity of CNF, return UNSAT if not valid
    if not CNFCheck(formula):
        return ("NOTINCNF", BV)

    # Return SAT or UNSAT if formula is True or False, respectively
    if isProp(formula) and formula.get_name() in ["True", "False"]:
        return ("SAT", BV) if formula.get_name() == "True" else ("UNSAT", BV)

    # Represents current formula, not necessarily valid yet
    curForm = formula
    # List of previous valid formulas
    prevForms = []

    # List of previous valid BVs
    prevBV = []

    # Represents possible branches to branch on from current formula
    branches = []
    # List of previous valid branches
    prevBranches = []

    # Random branch
    randomBranch = EmptyFormula()

    while True:
        # Apply unit propagation to current formula
        if not isEmptyFormula(randomBranch):
            curForm, BV = unitPropagate(curForm, BV, [randomBranch])
        else:
            curForm, BV = unitPropagate(curForm, BV)

        # Unit propagation returns empty clause, backtrack to last branch
        if not curForm:
            # If no previous formulas or branches to restore, return UNSAT
            if not prevForms or not prevBranches or not prevBV:
                return ("UNSAT", BV)

            # Restore previous valid formula, branch and BV
            curForm = prevForms.pop(0)
            branches = prevBranches.pop(0)
            BV = prevBV.pop(0).copy_bv()
        # Unit propagation produces empty formula, returns SAT
        elif isEmptyFormula(curForm):
            # Updating branches and return
            return ("SAT", fillBV(BV, formula))
        # Current formula still remains, continue to pure elimination
        else:
            # Apply pure elimination to current formula
            curForm, BV = pureEliminate(curForm, BV)

            # Pure elimination produces empty formula, return SAT
            if isEmptyFormula(curForm):
                # Updating branches and return
                return ("SAT", fillBV(BV, formula))
        
            # Grab all literals for new formula, creating new branch
            branches = []
            # Put all literals in formula in temp list
            tempBranches = grabPures(curForm, True)

            # Iterate through literals of temp list to put it and its negation in branches
            for literal in tempBranches:
                if literal not in branches:
                    branches.append(literal)
                if unitNegate(literal) not in branches:
                    branches.append(unitNegate(literal))
                   
        # If no more branching points, try to go to last valid branch point
        if not branches:
            # If no more formulas/branches to go back to, return UNSAT
            if not prevForms and not prevBranches and not prevBV:
                return ("UNSAT", BV)

            # Restore formulas and branches before breaking the loop
            curForm = prevForms.pop(0)
            branches = prevBranches.pop(0)
            BV = prevBV.pop(0)
            break

        # Go to a random literal
        randomBranch = random.choice(branches)
        # Remove that literal so it doesn't get chosen randomly again
        # branches.remove(randomBranch)

        # Saving current formula and branching information
        prevForms.insert(0, curForm)
        prevBranches.insert(0, branches)
        prevBV.insert(0, BV.copy_bv())

# Input: a george formula
# Output: a pair ("SAT"/"UNSAT"/"NOTINCNF", BV) 
# BV is a boolean valuation that is printed when the formula is SAT
# Includes heuristics/optimizations to the the DPLL algorithm
def DPLL_Optimized(formula):

    # TODO: - Copy code from DPLL function
    #       - Modify code to include heuristics/optimizations
    # Remember to use your CheckCNF() function first
    
    # Boolean valuation to be returned
    BV = BooleanValuation()

    # Check validity of CNF, return UNSAT if not valid
    if not CNFCheck(formula):
        return ("NOTINCNF", BV)

    # Return SAT or UNSAT if formula is True or False, respectively
    if isProp(formula) and formula.get_name() in ["True", "False"]:
        return ("SAT", BV) if formula.get_name() == "True" else ("UNSAT", BV)

    # Represents current formula, not necessarily valid yet
    curForm = formula
    # List of previous valid formulas
    prevForms = []

    # List of previous valid BVs
    prevBV = []

    # Represents possible branches to branch on from current formula
    branches = []
    # List of previous valid branches
    prevBranches = []

    # Boolean to ensure unit propagation after selecting random branch doesn't happen twice
    randomBranch = EmptyFormula()
    
    while True:
        if isEmptyFormula(randomBranch):
            # Apply unit propagation to current formula only if random branch hasn't been selected yet
            curForm, BV = unitPropagate(curForm, BV)
        else:
            curForm, BV = unitPropagate(curForm, BV, [randomBranch])

        # Unit propagation returns empty clause, backtrack to last branch
        if not curForm:
            # If no previous formulas or branches to restore, return UNSAT
            if not prevForms or not prevBranches or not prevBV:
                return ("UNSAT", BV)

            # Restore previous valid formula, branch and BV
            curForm = prevForms.pop(0)
            branches = prevBranches.pop(0)
            BV = prevBV.pop(0).copy_bv()
        # Unit propagation produces empty formula, returns SAT
        elif isEmptyFormula(curForm):
            # Updating branches and return
            return ("SAT", fillBV(BV, formula))
        # Current formula still remains, continue to pure elimination
        else:
            # Apply pure elimination to current formula
            curForm, BV = pureEliminate(curForm, BV)

            # Pure elimination produces empty formula, return SAT
            if isEmptyFormula(curForm):
                # Updating branches and return
                return ("SAT", fillBV(BV, formula))
        
            # Grab all literals for new formula, creating new branch
            branches = []
            # Put all literals in formula in temp list
            tempBranches = grabPures(curForm, True)

            # Iterate through literals of temp list to put it and its negation in branches
            for literal in tempBranches:
                if literal not in branches:
                    branches.append(literal)
                if unitNegate(literal) not in branches:
                    branches.append(unitNegate(literal))

        ### OPTIMIZATION #2 ###
        # Loop until valid branching point found
        while True:            
            # If no more branching points, try to go to last valid branch point
            if not branches:
                # If no more formulas/branches to go back to, return UNSAT
                if not prevForms and not prevBranches and not prevBV:
                    return ("UNSAT", BV)

                # Restore formulas and branches before breaking the loop
                curForm = prevForms.pop(0)
                branches = prevBranches.pop(0)
                BV = prevBV.pop(0)
                break
            
            ### OPTIMIZATION #1 ###
            # Go to the first branch, pop it off
            randomBranch = branches.pop(0)
            ### OPTIMIZATION #1 ###

            # Remove and reduce random branch
            tempForm = curForm
            tempBV = BV.copy_bv()
            # Apply unit propagation with the random branch
            curForm, BV = unitPropagate(curForm, BV, [randomBranch])

            # If invalid, choose random branch again
            if not curForm:
                curForm = tempForm
                BV = tempBV
                continue
            # If empty formula is produced, return SAT
            elif isEmptyFormula(curForm):
                # Updating branches and return
                return ("SAT", fillBV(BV, formula))
            # Valid branching point found
            else:
                BV = tempBV
                # Saving current formula and branching information
                prevForms.insert(0, curForm)
                prevBranches.insert(0, branches)
                prevBV.insert(0, BV.copy_bv())
                break 
        ### OPTIMIZATION #2 ###     

#####################################
# The main function of this module  #
# Do not change these lines         #
#####################################

def main(inp,dpll_opt):
    import george.grgio as grgio
    import george.frml as frml

    # NOTE: george will always check if a formula is a valid propositional formula before running DPLL
    
    # converting string (body of inp) to Formula object
    formula = frml.str_to_formula(inp.body)

    if dpll_opt:
        # running DPLL on formula
        (result, BV) = DPLL(formula)
    else:
        (result, BV) = DPLL_Optimized(formula)
    
    if result == "SAT":
        tmpStr = "DPLL -> SAT" + '\n' + '\n' + str(BV)
        return grgio.Feedback(inp.question, inp.part, True, [], [], [tmpStr])
    elif result == "UNSAT":
        return grgio.Feedback(inp.question, inp.part, True, [], [], ['DPLL -> UNSAT'])
    elif result == "NOTINCNF":
        return grgio.Feedback(inp.question, inp.part, False, ['DPLL -> NOT IN CNF'], [], [])

