Working with FileReferences and FileReferenceLists
==================================================

An uploaded Dataset will have a list of files associated with it, containing at least an HDF5 file containing the data.
With an instance of the :class:`.Dataset` class, we are able to browse and obtain the uploaded files stored in the database.

Obtaining a dataset file list
-----------------------------

If we want to examine which files are associated with a Dataset, we can obtain a list of file paths, sizes and download tokens as follows:

::

    files = dataset.get_full_file_list()

This will return a :class:`~gwdc_python.files.file_reference.FileReferenceList`, which contains :class:`~gwdc_python.files.file_reference.FileReference` instances for all files associated with the dataset:

::

    >>> for file_ref in files:
    ...     print(file_ref)

    FileReference(path=PosixPath('COMPAS_Output/COMPAS_Output.h5'))
    FileReference(path=PosixPath('COMPAS_Output/Run_Details'))

Obtaining the full file list is not always required, hence there is convenient method, :meth:`~.Dataset.get_data_file_list`, provided to only obtain the HDF5 file associated with the dataset.

Saving dataset files
--------------------

There are a couple of ways that we are able to actually obtain the data from desired files.
In general, we recommend streaming the files and saving them straight to disk. This is especially important for large files, or large numbers of files.
Hence, another method, :meth:`~.Dataset.save_data_files`, has been provided to download and save only the HDF5 data file.
For example, we can save this file, by running:

::

    dataset.save_data_files('directory/to/store/files')

which should give output for the download in the form of a progress bar:

::

    100%|██████████████████████████████████████| 1.00G/1.00G [01:40<00:00, 9.94MB/s]
    All 1 files saved!

Obtaining dataset file data
-----------------------

If we truly do just want to obtain the contents of some files, we can also download the files and store them in memory using the paired method :meth:`~.Dataset.get_data_files`.
For example, if we wish to obtain the HDF5 data file so that we can explore the data, we can run:

::

    file_data = dataset.get_data_files()

which returns a list of all the contents of the data files available for download.

.. warning::
    We recommend only using these methods when dealing with small total file sizes, as storing many MB or GB in memory can be detrimental to the performance of your machine.


Filtering files by path
-----------------------

If none of the provided methods return the desired subset of files, the full :class:`~gwdc_python.files.file_reference.FileReferenceList` can be filtered by using the more custom :meth:`~.FileReferenceList.filter_list_by_path` method.
This enables us to pick only the files we want based on the directories, the file name or the file extension.
For example, if we want to find all JSON files in the 'result' directory, we can can run:

::

    files = dataset.get_full_file_list()
    file_list = files.filter_list_by_path(directory='COMPAS_Output', name='Run_Details')

This returns a new :class:`~gwdc_python.files.file_reference.FileReferenceList` with contents like:

::

    >>> for f in file_list:
    ...     print(f)

    FileReference(path=PosixPath('COMPAS_Output/Run_Details'))

We are able to save or obtain the files for this custom :class:`~gwdc_python.files.file_reference.FileReferenceList` using the :meth:`~.GWLandscape.save_files_by_reference` and :meth:`~.GWLandscape.get_files_by_reference` methods.
For example, to save the above :code:`result_json_files`, we run:

::

    gwc.save_files_by_reference(file_list, 'directory/to/store/files')

Note that a :class:`~gwdc_python.files.file_reference.FileReferenceList` object can contain references to files from many different Datasets.
The :meth:`~.GWLandscape.save_files_by_reference` and :meth:`~.GWLandscape.get_files_by_reference` methods are able to handle such cases.
