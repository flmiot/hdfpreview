import os
import h5py
import numpy as np

class Dataset(object):
    def __init__(self, files):
        self.files = files
        self.keys  = dict()


    def get_filenames(self):
        return [os.path.split(f)[1] for f in self.files]


    def get_data_tree(self):
        for filename in self.files:
            with h5py.File(filename, 'r') as file:
                groups = list(file.values())
                for g in groups:
                    name = g.name
                    g.visititems(lambda n, i : self.fill_dict(name, n, i))

        return self.keys


    def fill_dict(self, group, name, item):
        if isinstance(item, h5py.Group):
            self.add_node(self.keys, item.name)
        elif isinstance(item, h5py.Dataset):
            self.add_entry(self.keys, item.name, item.name)


    def add_node(self, dictionary, path):
        segments = path.split('/')
        if len(segments) == 1:
            dictionary[segments[0]] = dict()
        else:
            key = segments.pop(0)
            if key == '':
                key = segments.pop(0)
            path    = '/'.join(segments)
            if not key in dictionary.keys():
                dictionary[key] = dict()
            self.add_node(dictionary[key], path)


    def add_entry(self, dictionary, path, value):
        segments = path.split('/')
        if len(segments) == 1:
            dictionary[segments[0]] = value
        else:
            key = segments.pop(0)
            if key == '':
                key = segments.pop(0)
            path    = '/'.join(segments)
            if not key in dictionary.keys():
                dictionary[key] = dict()
            self.add_entry(dictionary[key], path, value)


    def getData(self, path):
        with h5py.File(self.files[0], 'r') as file:
            shape = list()
            shape.extend(file[path].shape)
            dtype = file[path].dtype

        for ind, file in enumerate(self.files):
            if ind == 0:
                continue

            with h5py.File(file, 'r') as file:
                shape[0] += file[path].shape[0]

        data = np.empty(shape, dtype)

        index = 0
        for file in self.files:
            with h5py.File(file, 'r') as file:
                d = file[path]
                d.read_direct(data, None, np.s_[index : index + d.shape[0]])
                index += d.shape[0]

        return data
