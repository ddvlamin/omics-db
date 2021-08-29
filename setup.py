from setuptools import setup, find_namespace_packages

setup(
    name="biostrand-vector-db",
    version="0.0.1",
    description="",
    python_requires=">=3.9",
    packages=find_namespace_packages(include=["biostrand.*"]),
    namespace_packages=["biostrand"],
    include_package_data=False,
    author="biostrand",
    author_email="dieterdevlaminck@biostrand.be",
    zip_safe=False,
    keywords="biostrand",
    extras_require={},
    #cmdclass={
    #    'build_proto_modules': BuildPackageProtos,
    #},
    install_requires=[
        "pymilvus==2.0.0rc4",
        "pymilvus-orm==2.0.0rc4",
        "h5py==3.4.0",
        "scikit-learn==0.24.2"
        "fastapi==0.68.1"
        "uvicorn==0.15.0"
    ]
)

