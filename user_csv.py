def read_csv(filename, include_headers=True):
    """
    Reads a CSV file and returns its contents as a 2D list.

    Params:
        filename (str): The name of the CSV file to read.
        include_headers (bool): Whether to include headers in the output.

    Returns:
        list: A 2D list containing the CSV data.
    """
    data = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        
        for i, line in enumerate(lines):
            # Split line by commas and strip whitespace
            row = [float(value) if value.strip().replace('.', '', 1).isdigit() else value.strip() for value in line.split(',')]
            # Include headers conditionally
            if i == 0 and not include_headers:
                continue
            data.append(row)

    return data

def write_csv(filename, data, overwrite=True):
    """
    Writes data to a CSV file.

    Parameters:
        filename (str): The name of the file to write to.
        data (list): A 2D list containing the data to write.
        overwrite (bool): Whether to overwrite or append to the file.
    """
    mode = 'w' if overwrite else 'a'
    with open(filename, mode) as file:
        for row in data:
            line = ','.join(map(str, row)) + '\n'
            file.write(line)
