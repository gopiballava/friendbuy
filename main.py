from memred import MemRed, NoTransactionException
from sys import stdin, exit

def parse_execute_memred(mr: MemRed, line: str):
    line_parts = line.split()
    if len(line_parts) == 0:
        return
    if line_parts[0] == 'SET':
        if len(line_parts) == 3:
            mr.set(line_parts[1], line_parts[2])
    elif line_parts[0] == 'GET':
        if len(line_parts) == 2:
            retv = mr.get(line_parts[1])
            if retv is None:
                return 'NULL'
            return retv
    elif line_parts[0] == 'NUMEQUALTO':
            if len(line_parts) == 2:
                return mr.num_equal_to(line_parts[1])
    elif line_parts[0] == 'UNSET':
        if len(line_parts) == 2:
            mr.unset(line_parts[1])
    elif line_parts[0] == 'BEGIN':
        mr.begin()
    elif line_parts[0] == 'COMMIT':
        try:
            mr.commit()
        except NoTransactionException:
            return 'NO TRANSACTION'
    elif line_parts[0] == 'ROLLBACK':
        try:
            mr.rollback()
        except NoTransactionException:
            return 'NO TRANSACTION'
    elif line_parts[0] == 'END':
        exit(0)

def main():
    mr = MemRed()
    for line in stdin:
        output = parse_execute_memred(mr, line.strip())
        if output:
            print(output)

if __name__ == '__main__':
    main()

