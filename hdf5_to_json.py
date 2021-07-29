try:
    import numpy as np
    import h5py
    import json
except Exception as e:
    print('SOME LIBRARIES ARE MISSING! PLEASE RUN: pip install -r requirements.txt')
    quit()


class HDF5:
    def __init__(self, filename):
        self.filename = filename


    """ METHOD COMMENT ------------------------------------------------------------------
    Recursive Read method reads the HDF5 file recursively. It will check if the current
    node is a Group or a Dataset. If a Group is detected, it will call itself and will
    check all its members, else if a Dataset is detected it will get all its values and
    attributes.
    --------------------------------------------------------------------------------- """
    def recursive_read(self, data, output={}):
        for key in data:
            if isinstance(data.get(key), h5py.Group):
                output[key] = {}
                output[key] = self.recursive_read(data.get(key), output[key])
            
            elif isinstance(data.get(key), h5py.Dataset):
                output[key] = {}
                output[key]['data'] = list(np.array(data.get(key)).astype(float))

                output[key]['attributes'] = {}
                for attr in data.get(key).attrs.items():
                    try:
                        output[key]['attributes'][attr[0]] = attr[1][0].astype(float)
                    except:
                        output[key]['attributes'][attr[0]] = attr[1][0].astype(str)
                
        return output


    def read_data(self):
        data = {}
        with h5py.File(self.filename, 'r') as hdf:
            data = self.recursive_read(hdf)

        return data
    
    
    def export_json(self, data):
        with open(f'{self.filename}.json', 'w') as f:
            f.write(json.dumps(data))


    def execute(self):
        print('Opening file...')
        
        print('Reading Data...')
        data = self.read_data()
        
        print('Exporting as JSON...')
        self.export_json(data)


def main():
    filename = input('Enter filename [.h5]: ')
    try:
        hdf5 = HDF5(filename)
        hdf5.execute()
    except Exception as e:
        print('Something went wrong:', e)


if __name__ == '__main__':
    main()