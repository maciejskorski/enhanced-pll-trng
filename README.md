![Python](https://img.shields.io/static/v1?style=for-the-badge&message=Python&color=3776AB&logo=Python&logoColor=FFFFFF&label=)
![Google Colab](https://img.shields.io/static/v1?style=for-the-badge&message=Google+Colab&color=222222&logo=Google+Colab&logoColor=F9AB00&label=)
![MLflow](https://img.shields.io/static/v1?style=for-the-badge&message=MLflow&color=0194E2&logo=MLflow&logoColor=FFFFFF&label=)


# Enhancing Quality and Security of the PLL-TRNG

## Summary

The repo contains supplementary material (data and code) to reproduce experiments presented in the paper.


## Data and Code

Data used in experiments are stored under the `data` directory; sub-directories correspond to FPGA card families (CV- Cyclone®V, S6 - Spartan™6, SF - SmartFusion®). The experiments were executed on Google Colab and can be reproduced with [this notebook](src/TRNG_Dependency_Analysis.ipynb).
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
│   ├───📄 TRNG_Dependency_Analysis.ipynb
│   └───📄 demo.py
└───📄 README.md
```

## Links

- For random number generator standards, see [AIS-31 NewDraft](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Certification/Interpretations/AIS_31_Functionality_classes_for_random_number_generators_e.pdf?__blob=publicationFile&v=5)
- For more about stochastic models for PLL-based designs, see ["Modern Random Number Generator Design - Case Study on a Secured PLL-based TRNG"](https://www.degruyter.com/document/doi/10.1515/itit-2018-0025/html?lang=en)