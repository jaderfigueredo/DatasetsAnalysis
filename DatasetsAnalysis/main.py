import subprocess

# List of libraries to check and install
required_libraries = [
    ('numpy', 'np'),
    ('pandas', 'pd'),
    ('seaborn', 'sns')
]

def install_library(library_name, alias):
    try:
        imported_lib = __import__(library_name)  # Try to import the library
        globals()[alias] = imported_lib  # Assign an alias to the library
        print(f"{library_name} is already installed and aliased as '{alias}'.")
    except ImportError:
        print(f"{library_name} is not installed. Installing...")
        subprocess.call(['pip', 'install', library_name])  # Use pip to install the library
        imported_lib = __import__(library_name)  # Try to import the library again
        globals()[alias] = imported_lib  # Assign an alias to the library
        print(f"{library_name} has been successfully installed and aliased as '{alias}'.")


for library, alias in required_libraries:
    install_library(library, alias)

from CSVNormalizer import CSVNormalizer

class Dataset:
    def __init__(self, datasetPath, numberOfFeatures, hasIndex=True, normalize=True):
        self.datasetPath = datasetPath
        datasetPathSplited = self.datasetPath.split('.')
        fileExtension = datasetPathSplited.pop(-1)
        datasetPathSplited.append('normalized')
        datasetPathSplited.append(fileExtension)
        self.normalizedFilePath = '.'.join(datasetPathSplited)

        

    # It's expected the columns: index, feature1, feature2, ..., featureN, label(class)
    def normalizeCSV(self, hasIndex=True, numberOfFeatures=1):
        normalizer = CSVNormalizer(self.datasetPath)
        indexOfFeature1 = 1 if hasIndex else 0 # = (hasIndex) ? 1 : 0;
        numberOfFeatures = (numberOfFeatures-1)+indexOfFeature1
        normalizer.normalize_columns_between_a_and_z(indexOfFeature1, numberOfFeatures, self.normalizedFilePath)

    
    def preAnalisys(self):
        ds = pd.read_csv(self.normalizedFilePath)
        print('Dados importados\n')

        print('Dimensões: ')
        print('Linhas:\t\t', ds.shape[0])
        print('Colunas:\t', ds.shape[1])

        print('\nAtributos (colunas):')
        print(ds.columns.values)

        print('\nDetalhes:')
        ds.info()

#Definindo um dataset
dataset = Dataset('/home/jader/Mestrado/DatasetsAnalisys/Iris.csv')
dataset.normalizeCSV(hasIndex=True, numberOfFeatures=4)
dataset.preAnalisys()
