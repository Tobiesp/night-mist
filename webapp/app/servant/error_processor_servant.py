def process_error(error: str) -> str:
    if error is None:
        return 'An unknown error occurred'
    print(f'Processing Error: {error}')
    if error.find('NOT NULL constraint failed:') != -1:
        tmp = error.split('\n')[0]
        print(f'TMP: {tmp}')
        tmp = tmp.split('NOT NULL constraint failed: ')[1]
        print(f'TMP: {tmp}')
        table = tmp.split('.')[0].replace('_table', '')
        print(f'Table: {table}')
        field = tmp.split('.')[1]
        print(f'Field: {field}')
        return f'Missing required field {field} for {table}'
    return error