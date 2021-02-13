import setuptools

setuptools.setup(
	name="cvut",
	version='0.0.1',
	packages=setuptools.find_packages(),
	install_requires=[
		'numpy', 'pycocotools', 'mmcv', 'opencv-python',
	],
	python_requires='>=3.6',
)
