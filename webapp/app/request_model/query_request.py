

class QueryRequest():

    def __init__(self, query: dict[str, str]):
        request_args = query or {}
        self.filter_value = request_args.get('filter_value') or ''
        self.page_num = request_args.get('page_num') or 0
        self.page_size = request_args.get('page_size') or 100
        self.sort_active = request_args.get('sort_active') or ''
        self.sort_direction = request_args.get('sort_direction') or ''

        if self.page_num.isdigit():
            self.page_num = int(self.page_num)
        else:
            self.page_num = 0
        
        if self.page_num < 0:
            raise ValueError(f'Invalid page number: {self.page_num}')

        if self.page_size.isdigit():
            self.page_size = int(self.page_size)
        else:
            self.page_size = 100

        if self.page_size < 1:
            raise ValueError(f'Invalid page size: {self.page_size}')
        
        if self.filter_value == 'undefined':
            self.filter_value = ''

        if self.sort_active == 'undefined':
            self.sort_active = ''

        if self.sort_direction == 'undefined':
            self.sort_direction = ''