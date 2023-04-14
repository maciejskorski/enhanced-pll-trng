![Python](https://img.shields.io/static/v1?style=for-the-badge&message=Python&color=3776AB&logo=Python&logoColor=FFFFFF&label=)
![Google Colab](https://img.shields.io/static/v1?style=for-the-badge&message=Google+Colab&color=222222&logo=Google+Colab&logoColor=F9AB00&label=)
![MLflow](https://img.shields.io/static/v1?style=for-the-badge&message=MLflow&color=0194E2&logo=MLflow&logoColor=FFFFFF&label=)


# Enhancing Quality and Security of the PLL-TRNG

## Summary

The repo contains supplementary material (data and code) to reproduce experiments presented in the paper.


## Data and Code

Data used in experiments are stored under the `data` directory. Sub-directories at the first level correspond to FPGA card families (CV- Cyclone®V, S6 - Spartan™6, SF - SmartFusion®, two Spartan devices were tested); sub-directories at the second level correspond to configurations described in the paper (A, B, or C), with one or two PLL outputs as indicated by the suffix (e.g. A_1 vs A_2). The experiments were executed on Google Colab and can be reproduced with [this notebook](src/TRNG_Dependency_Analysis.ipynb).  
```
├───📁 data/
│   ├───📁 CVv12_4/
│   │   ├───📁 A_1/
│   │   │   └───...
│   │   ├───📁 A_2/
│   │   │   └───...
│   │   ├───📁 B_1/
│   │   │   └───...
│   │   ├───📁 B_2/
│   │   │   └───...
│   │   ├───📁 C_1/
│   │   │   └───...
│   │   └───📁 C_2/
│   │       └───...
│   ├───📁 S6v11_2/
│   │   ├───📁 A_1/
│   │   │   └───...
│   │   ├───📁 A_2/
│   │   │   └───...
│   │   ├───📁 B_1/
│   │   │   └───...
│   │   ├───📁 B_2/
│   │   │   └───...
│   │   ├───📁 C_1/
│   │   │   └───...
│   │   └───📁 C_2/
│   │       └───...
│   ├───📁 S6v11_8/
│   │   ├───📁 a1/
│   │   │   └───...
│   │   ├───📁 a2/
│   │   │   └───...
│   │   ├───📁 b1/
│   │   │   └───...
│   │   ├───📁 b2/
│   │   │   └───...
│   │   ├───📁 c1/
│   │   │   └───...
│   │   ├───📁 c2/
│   │   │   └───...
│   │   └───📄 .DS_Store
│   ├───📁 SF2v11_11/
│   │   ├───📁 A_1/
│   │   │   └───...
│   │   ├───📁 A_2/
│   │   │   └───...
│   │   ├───📁 B_1/
│   │   │   └───...
│   │   ├───📁 B_2/
│   │   │   └───...
│   │   ├───📁 C_1/
│   │   │   └───...
│   │   └───📁 C_2/
│   │       └───...
│   └───📄 data.zip
├───📁 src/
│   └───📄 TRNG_Dependency_Analysis.ipynb
└───📄 README.md
```

## Links

- For random number generator standards, see [AIS-31 (New Draft)](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Certification/Interpretations/AIS_31_Functionality_classes_for_random_number_generators_e.pdf?__blob=publicationFile&v=5)
- For more about stochastic models for PLL-based designs, see ["Modern Random Number Generator Design - Case Study on a Secured PLL-based TRNG"](https://www.degruyter.com/document/doi/10.1515/itit-2018-0025/html?lang=en)