# This class reads a csv file without any dependencies

def read_type_chart(filename):
    output = {}
    with open(filename, 'r') as file:
        counter = -1
        for line in file:
            if counter == -1:
                counter += 1
                opponent = line.strip().split(',')
                continue
            effectiveness = {}
            index = [
                'normal','fire','water','electric','grass','ice',
                'fighting','poison','ground','flying','psychic','bug',
                'rock','ghost','dragon','dark','steel','fairy'
            ]
            res = line.strip().split(',')
            for i in range(18):
                effectiveness[index[i]] = res[i]
            output[opponent[counter]] = effectiveness
            counter += 1
    return output

def read_config(filename):
    output = []
    with open(filename, 'r') as file:
        for line in file:
            output.append(line.strip().split(','))
    return output