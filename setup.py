import setuptools

setuptools.setup(
	name="cvut",
	version='0.0.1',
	packages=setuptools.find_packages(),
	install_requires=[
		'cython', 'numpy', 'opencv-python', 'sklearn', 'pandas',
		'ipython', 'pylint', 'ipympl', 'pyyaml', 'tqdm', 'future',
	],
	python_requires='>=3.6',
)
setuptools.setup(
	name="utils",
	version='0.0.1',
	packages=setuptools.find_packages(),
	python_requires='>=3.6',
)
