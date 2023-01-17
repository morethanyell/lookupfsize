import sys, os, csv
from splunklib.searchcommands import \
    dispatch, StreamingCommand, Configuration, Option, validators

@Configuration()
class lookupfsizeCommand(StreamingCommand):

    file_path = Option(
        doc='''
        **Syntax:** **file_path=***<field name that contains the full path of the lookup table>*
        **Description:** The full path of the CSV lookup file.''',
        require=True, validate=validators.Fieldname())

    def stream(self, events):
        
        for event in events:
            
            fpath = event[self.file_path]
            
            if str(fpath).endswith('.csv'):
                try:
                    file_size = os.path.getsize(fpath)    
                    matrix = self.rc_count(fpath)
                    
                    event['lookup_file_size'] = str(file_size)
                    event['lookup_fsiz_unit'] = "bytes"
                    event['lookup_row_count'] = str(matrix[0])
                    event['lookup_col_count'] = str(matrix[1])
                except Exception as e:
                    event['error'] = e
            
                yield event

    @staticmethod
    def rc_count(_file_path):
        
        file_path = _file_path
        row_count = 0
        col_count = 0

        with open(file_path) as file:
            
            csv_reader = csv.reader(file)

            for row in csv_reader:
                row_count += 1
                col_count = max(col_count, len(row))

        return row_count, col_count


dispatch(lookupfsizeCommand, sys.argv, sys.stdin, sys.stdout, __name__)