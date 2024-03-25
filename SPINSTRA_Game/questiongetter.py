import pandas as pd

def pathfinder(block):
    '''
    Generates a file path based on integer argument passed in that corresponds to a SPINSTRA block.
    '''
    blocks = ['indoctrination', 'math', 'inorganic_chemistry', 'physics', 'orbital_mechanics', 'electronics_principles', 'linux', 'programming', 'linear_algebra', 'isr_fundamentals']
    return('Data/Questions/' + blocks[block - 1] + '/questions.csv')


block = int(input('Please enter the number of the block that your questions correspond to. '))
questionsdf = pd.DataFrame(pd.read_csv(pathfinder(block)))

while True:
    
    difficulty = int(input('Please enter a difficulty for the question from 0-3. '))
    question = str(input('Please enter your question. '))
    answer = str(input('Please enter the answer to your question. '))
    feedback = str(input('Please enter some feedback to give when the answer given is incorrect (this is to help get it right next time). '))
    incorrect1 = str(input('Please enter an incorrect answer. '))
    incorrect2 = str(input('Please enter an incorrect answer. '))
    incorrect3 = str(input('Please enter an incorrect answer. '))
    cont = input('Would you like to add another question? y/n? ')
    
    questionsdf.loc[len(questionsdf)] = [difficulty, question, answer, feedback, incorrect1, incorrect2, incorrect3]
    
    if cont == 'y':
        continue
    
    else:
        break
    
questionsdf.to_csv(pathfinder(block), sep=',')