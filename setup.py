import setuptools

setuptools.setup(
    name="cvut",
    version='0.1.8',
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "video2images=cvut.tools.video2images:main",
            "images2video=cvut.tools.images2video:main",
            "count_coco_imgs=cvut.tools.count_coco_imgs:main",
        ]},
    python_requires='>=3.6',
)
