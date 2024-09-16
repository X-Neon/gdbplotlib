import setuptools

with open('README.md') as readme:
    long_description = readme.read()

setuptools.setup(
    name='gdbplotlib',
    version='0.3.0',
    author='George Cholerton',
    author_email='gcholerton@gmail.com',
    url='https://github.com/X-Neon/gdbplotlib',
    packages=setuptools.find_packages(),
    install_requires=['numpy', 'matplotlib'],
    python_requires='>=3',
    description='Plotting and exporting of variables from GDB',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['gdb', 'debug'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Debuggers'
    ]
)