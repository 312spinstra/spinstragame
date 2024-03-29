import pandas as pd

def pathfinder(block):
    '''
    Generates a file path based on integer argument passed in that corresponds to a SPINSTRA block.
    '''
    blocks = ['indoctrination', 'math', 'inorganic_chemistry', 'physics', 'orbital_mechanics', 'electronics_principles', 'linux', 'programming', 'linear_algebra', 'isr_fundamentals']
    return('Data/Questions/' + blocks[block - 1] + '/questions.csv')

while True:

    # set the incorrect answers as None
    incorrect1 = None
    incorrect2 = None
    incorrect3 = None

    # list the block choices
    blocks = ['indoctrination', 'math', 'inorganic_chemistry', 'physics', 'orbital_mechanics', 'electronics_principles', 'linux', 'programming', 'linear_algebra', 'isr_fundamentals']
    for i, block in enumerate(blocks, 1):
        if i < 10:
            print(f'{i}  |  {block}')
        else:
            print(f'{i} |  {block}')

    # take user input to choose the block and check if thier choice is valid
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
        
    # open the desired block's csv with the file pathfinder
    questionsdf = pd.DataFrame(pd.read_csv(pathfinder(block), sep=';'))
        
    # prompts user for question type and checks if the input is valid
    while True:
        kind = input('Please enter \'1\' for multiple choice, \'2\' for short answer/fill in the blank, and \'3\' for True or False ')
        
        if kind != '1' and kind != '2' and kind != '3':
            print('That is not a valid choice.')
            continue
        else:
            break
        
        
    # prompts user for question difficulty and checks if the input is valid
    while True:
        difficulty = int(input('Please enter a difficulty for the question from 0-3. '))
         
        if difficulty != 0 and difficulty != 1 and difficulty != 2 and difficulty != 3:
            print('That is not a valid choice.')
            continue
        
        break
    
    # prompts user for question, answer, and feedback (required for all question types)
    while True:
        question = str(input('Please enter your question. '))
        if ';' in question:
            print('You may not have a semicolon in your question.')
            continue
        
        break
           
    while True:
        answer = str(input('Please enter the answer to your question. '))
        if ';' in answer:
            print('You may not have a semicolon in your answer.')
            continue
        
        if kind == '3' and answer.title() != 'False' and answer.title() != 'True':
            print(f'Your answer for a True or False must be \'True\' or \'False\', it may not be: \'{answer}\'')
            continue
        
        break
    
    while True:    
        feedback = str(input('Please enter some feedback to give when the answer given is incorrect (this is to help get it right next time). '))
        if ';' in feedback:
            print('You may not have a semicolon in your feedback.')
            continue
        
        break
    
    # prompts user for different info based on question type
    if kind == '1':
        while True:
            incorrect1 = str(input('Please enter an incorrect answer. '))
            if ';' in incorrect1:
                print('You may not have a semicolon in your incorrect answers.')
                continue
            
            break
        
        while True:
            incorrect2 = str(input('Please enter an incorrect answer. '))
            if ';' in incorrect2:
                print('You may not have a semicolon in your incorrect answers.')
                continue
        
            break
        
        while True:
            incorrect3 = str(input('Please enter an incorrect answer. '))
            if ';' in incorrect3:
                print('You may not have a semicolon in your incorrect answers.')
                continue
            
            break
        
    elif kind == '3':
        answer = answer.title()
        if answer == 'True':
            incorrect1 = 'False'
        else:
            incorrect1 = 'True'

    # adds user's question to csv and replaces the old csv
    questionsdf.loc[len(questionsdf)] = [difficulty, question, answer, feedback, incorrect1, incorrect2, incorrect3]
    questionsdf.to_csv(pathfinder(block), sep=';', index=False)
    
    cont = input('Would you like to add another question? y/n? ')
    
    if cont == 'y':
        continue
    
    else:
        break