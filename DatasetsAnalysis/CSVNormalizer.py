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
    """
    def normalize_columns_between_a_and_z(self, start_column_index, end_column_index, output_file_name):
        if self.df is None:
            print("Não é possível normalizar. O DataFrame não foi carregado corretamente.")
            return

        try:
            # Verifique se os índices fornecidos são válidos
            if (
                start_column_index < 0
                or end_column_index < 0
                or start_column_index >= len(self.df.columns)
                or end_column_index >= len(self.df.columns)
            ):
                print("Índices de coluna fornecidos são inválidos.")
                return

            # Normalize as colunas entre 0 e 1
            for col_index in range(start_column_index, end_column_index + 1):
                col = self.df.iloc[:, col_index]
                min_value = col.min()
                max_value = col.max()
                if min_value != max_value:
                    self.df[self.df.columns[col_index]] = (col - min_value) / (max_value - min_value)

            # Salve o arquivo CSV normalizado
            self.df.to_csv(output_file_name, index=False)
            print(f"Arquivo CSV normalizado salvo como {output_file_name}")

        except Exception as e:
            print(f"Ocorreu um erro durante a normalização: {str(e)}")
    """

    def normalize_and_save_columns(self, columns_to_normalize, output_file_name):
        if self.df is None:
            print("Não é possível normalizar. O DataFrame não foi carregado corretamente.")
            return

        try:
            # Identify the columns to keep using your names
            column_to_keep = [col for col in self.df.columns if self.df.columns.get_loc(col) in columns_to_normalize or 0 < self.df.columns.get_loc(col) and col != self.df.columns[-1]]
            print('Colunas para normalizar')
            print(column_to_keep)

            # Identify the columns to drop (excluding the first and last columns)
            columns_to_drop = [col for col in self.df.columns if col != self.df.columns[0] and col != self.df.columns[-1] and self.df.columns.get_loc(col) not in columns_to_normalize]
            print('Colunas para remover')
            print(columns_to_drop)

            # Drop the columns to exclude
            self.df = self.df.drop(columns=columns_to_drop)

            # Normalize the specified columns between 0 and 1
            for col_index in column_to_keep:
                col = self.df.iloc[:, col_index]
                min_value = col.min()
                max_value = col.max()
                if min_value != max_value:
                    self.df.iloc[:, col_index] = (col - min_value) / (max_value - min_value)

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
            columns_to_normalize = [2,3]  # Specify the column indices you want to normalize
            separator = ','  # Specify the separator if needed

            normalizer = CSVNormalizer(file_name, separator)
            normalizer.normalize_and_save_columns(columns_to_normalize, output_file_name)
    else:
        print("No CSV files found in the directory.")


