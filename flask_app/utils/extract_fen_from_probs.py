import numpy as np

def fen_from_onehot(one_hot):
    one_hot=np.array(one_hot).reshape(8,8)
    piece_symbols = 'prbnkqPRBNKQ'
    output = ''
    for j in range(8):
        for i in range(8):
            if(one_hot[j][i] == 12):
                output += ' '
            else:
                output += piece_symbols[one_hot[j][i]]
        if(j != 7):
            output += '/'

    for i in range(8, 0, -1):
        output = output.replace(' ' * i, str(i))

    return output

def assign_pieces(one_hot_vectors):
    assigned_pieces = []
    for vector in one_hot_vectors:
        max_index = vector.index(max(vector))
        # Check for duplicates of white king (index 10) or black king (index 4)
        if vector[max_index] == vector[10] or vector[max_index] == vector[4]:
            # Find the indices of all occurrences with maximum value
            max_indices = [i for i, x in enumerate(vector) if x == max(vector)]
            # Find the sorted list of probabilities for the max_indices
            sorted_probs = sorted([vector[i] for i in max_indices], reverse=True)
            # Make sure the sorted list has at least two elements
            if len(sorted_probs) >= 2:
                second_max_value = sorted_probs[1]
                second_max_index = vector.index(second_max_value)
                # Assign the piece with the second-highest probability
                assigned_pieces.append(second_max_index)
            else:
                # If there is only one value in the sorted list, use the max_index
                assigned_pieces.append(max_index)
        else:
            # Assign the piece with the highest probability
            assigned_pieces.append(max_index)
    return assigned_pieces