import os
import pandas as pd

class CSVNormalizer:
    def __init__(self, file_name, separator=','):
        self.file_name = file_name
        self.df = None
        self.separator = separator
        self.load_csv()

    def load_csv(self):
        try:
            self.df = pd.read_csv(self.file_name, sep=self.separator)
        except FileNotFoundError:
            print(f"O arquivo {self.file_name} não foi encontrado.")
            self.df = None
        except Exception as e:
            print(f"Ocorreu um erro durante a leitura do arquivo CSV: {str(e)}")
            self.df = None


    def normalize_and_save_columns(self, columns_to_keep=[], output_file_name=None):
        if self.df is None:
            print("Não é possível normalizar. O DataFrame não foi carregado corretamente.")
            return
        
        #If none columns is especified, all of the columns is kept 
        if columns_to_keep == []:
            columns_to_keep = [i for i in range(len(self.df.columns))]
        
        # If output_file_name is not especified, it will is 'normalized_' concatenated with the current name of the file
        output_file_name = 'normalized_'+self.file_name if output_file_name == None else output_file_name

        try:
            indexColumnName = self.df.columns[0]
            classColumnName = self.df.columns[-1]

            # Identify the columns to keep using your names
            columns_to_normalize = [col for col in self.df.columns if col not in [indexColumnName, classColumnName] and self.df.columns.get_loc(col) in columns_to_keep]
            print('Colunas para normalizar')
            print(columns_to_normalize)

            # Identify the columns to drop (excluding the first and last columns)
            columns_to_drop = [col for col in self.df.columns if col not in [indexColumnName, classColumnName] and self.df.columns.get_loc(col) not in columns_to_keep]
            print('Colunas para remover')
            print(columns_to_drop)

            # Drop the columns to exclude
            self.df = self.df.drop(columns=columns_to_drop)

            # Normalize the specified columns between 0 and 1
            for colName in columns_to_normalize:
                print(colName)
                col = self.df[colName]
                min_value = col.min()
                max_value = col.max()
                if min_value != max_value:
                    try:
                        self.df[colName] = (col - min_value) / (max_value - min_value)
                    except Exception as e:
                        print('Item %s: %s' % (colName, e))

            # Save the normalized DataFrame to a CSV file
            self.df.to_csv(output_file_name, index=False)
            print(f"Arquivo CSV normalizado salvo como {output_file_name}")

        except Exception as e:
            print(f"Ocorreu um erro durante a normalização: {str(e)}")


# Usage example:
if __name__ == "__main__":

    def list_csv_files_in_directory(directory):
        csv_files = [file for file in os.listdir(directory) if file.endswith('.csv')]
        return csv_files

    current_directory = os.getcwd()  # Get the current directory where this code is located
    csv_files = list_csv_files_in_directory(current_directory)

    if csv_files:
        print("CSV files in the directory:")
        for file in csv_files:
            print(file)
            file_name = file
            output_file_name = 'normalized_output.csv'
            columns_to_keep = [1,2,3,4]  # Specify the column indices you want to normalize
            separator = ','  # Specify the separator if needed

            normalizer = CSVNormalizer(file_name, separator)
            normalizer.normalize_and_save_columns()
    else:
        print("No CSV files found in the directory.")


