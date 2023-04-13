![Python](https://img.shields.io/static/v1?style=for-the-badge&message=Python&color=3776AB&logo=Python&logoColor=FFFFFF&label=)
![Google Colab](https://img.shields.io/static/v1?style=for-the-badge&message=Google+Colab&color=222222&logo=Google+Colab&logoColor=F9AB00&label=)
![MLflow](https://img.shields.io/static/v1?style=for-the-badge&message=MLflow&color=0194E2&logo=MLflow&logoColor=FFFFFF&label=)


# Summary

The repo tracks experiments for the project "New PLL TRNG".



# Data and Code

Data used in experiments are stored under the `data` directory; sub-directories correspond to card families.
The experiments were done in [this Colab Notebook](src/TRNG_Dependency_Analysis.ipynb).

```
├───📁 data/
│   ├───📁 CvVv12_4/
│   │   └───...
│   ├───📁 S6v11_2/
│   │   └───...
│   ├───📁 SF2v11_11/
│   │   └───...
│   └───📄 data.zip
├───📁 src/
│   └───📄 demo.py
├───📄 .DS_Store
├───📄 .gitattributes
├───📄 README.md
└───📄 TRNG_Dependency_Analysis.ipynb
```



# Analysis

# Links

- [AIS_31_NewDraft](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Certification/Interpretations/AIS_31_Functionality_classes_for_random_number_generators_e.pdf?__blob=publicationFile&v=5)
- [KS08](https://iacr.org/archive/ches2008/51540144/51540144.pdf)