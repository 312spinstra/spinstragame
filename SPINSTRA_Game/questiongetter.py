import pandas as pd

def pathfinder(block):
    '''
    Generates a file path based on integer argument passed in that corresponds to a SPINSTRA block.
    '''
    blocks = ['indoctrination', 'math', 'inorganic_chemistry', 'physics', 'orbital_mechanics', 'electronics_principles', 'linux', 'programming', 'linear_algebra', 'isr_fundamentals']
    return('Data/Questions/' + blocks[block - 1] + '/questions.csv')

incorrect1 = None
incorrect2 = None
incorrect3 = None

blocks = ['indoctrination', 'math', 'inorganic_chemistry', 'physics', 'orbital_mechanics', 'electronics_principles', 'linux', 'programming', 'linear_algebra', 'isr_fundamentals']
for i, block in enumerate(blocks, 1):
    if i < 10:
        print(f'{i}  |  {block}')
    else:
        print(f'{i} |  {block}')

while True:
    try:
        block = int(input('Please enter the number of the block that your questions correspond to. '))
        if block < 1 or block > 10:
            raise ValueError
        
        else:
            break
        
    except ValueError:
        print('That is not a valid choice.')
        continue
    
questionsdf = pd.DataFrame(pd.read_csv(pathfinder(block), sep=';'))

while True:
    
    kind = input('Please enter \'1\' for multiple choice, \'2\' for short answer/fill in the blank, and \'3\' for True or False ')
    
    if kind != '1' and kind != '2' and kind != '3':
        print('That is not a valid choice.')
        continue
        
        
    while True:
        try:
            difficulty = int(input('Please enter a difficulty for the question from 0-3. '))
            if block < 1 or block > 10:
                raise ValueError
        
            else:
                break
        
        except ValueError:
            print('That is not a valid choice.')
            continue
    
    question = str(input('Please enter your question. '))
    answer = str(input('Please enter the answer to your question. '))
    feedback = str(input('Please enter some feedback to give when the answer given is incorrect (this is to help get it right next time). '))
    
    if kind == '1':
        incorrect1 = str(input('Please enter an incorrect answer. '))
        incorrect2 = str(input('Please enter an incorrect answer. '))
        incorrect3 = str(input('Please enter an incorrect answer. '))
    
    elif kind == '3':
        answer = answer.title()
        if answer == 'True':
            incorrect1 = 'False'
        else:
            incorrect1 = 'True'

    cont = input('Would you like to add another question? y/n? ')
    
    questionsdf.loc[len(questionsdf)] = [difficulty, question, answer, feedback, incorrect1, incorrect2, incorrect3]
    
    
    if cont == 'y':
        continue
    
    else:
        break
    
questionsdf.to_csv(pathfinder(block), sep=';', index=False)